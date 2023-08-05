import json
import re
import socket
import ssl
from base64 import b64decode, b64encode
from typing import Tuple

from todus3.errors import AuthenticationError, EndOfStreamError
from todus3.util import generate_token

_BUFFERSIZE = 1024 * 1024


def _get_socket() -> ssl.SSLSocket:
    socket_ = socket.socket(socket.AF_INET)
    socket_.settimeout(15)
    ssl_socket = ssl.wrap_socket(socket_, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssl_socket.connect(("im.todus.cu", 1756))
    ssl_socket.send(
        b"<stream:stream xmlns='jc' o='im.todus.cu' xmlns:stream='x1' v='1.0'>"
    )
    return ssl_socket


def _negociate_start(
    response: str, ssl_socket: ssl.SSLSocket, authstr: bytes, sid: str
) -> bool:
    if response.startswith(
        "<?xml version='1.0'?><stream:stream i='"
    ) and response.endswith("xmlns:stream='x1' f='im.todus.cu' xmlns='jc'>"):
        return True

    data: bytes = b""
    auth_stream: str = (
        "<stream:features>"
        "<es xmlns='x2'><e>PLAIN</e><e>X-OAUTH2</e></es>"
        "<register xmlns='http://jabber.org/features/iq-register'/>"
        "</stream:features>"
    )
    if response == auth_stream:
        data = b"<ah xmlns='ah:ns' e='PLAIN'>" + authstr + b"</ah>"
        ssl_socket.send(data)
        return True

    if response == "<ok xmlns='x2'/>":
        data = b"<stream:stream xmlns='jc' o='im.todus.cu' xmlns:stream='x1' v='1.0'>"
        ssl_socket.send(data)
        return True

    if "<stream:features><b1 xmlns='x4'/>" in response:
        data = f"<iq i='{sid}-1' t='set'><b1 xmlns='x4'></b1></iq>".encode("utf-8")
        ssl_socket.send(data)
        return True

    return False


def _parse_token(token: str) -> Tuple[str, bytes]:
    assert token, "Invalid Token 'None'"
    phone = json.loads(b64decode(token.split(".")[1]).decode())["username"]
    authstr = b64encode((chr(0) + phone + chr(0) + token).encode("utf-8"))
    return phone, authstr


def reserve_url(token: str, filesize: int) -> Tuple[str, str]:
    """Reserve file URL to upload.

    Returns a tuple with upload and download URLs.
    """
    data: bytes = b""
    phone, authstr = _parse_token(token)
    sid = generate_token(5)
    ssl_socket = _get_socket()

    while True:
        response = ssl_socket.recv(_BUFFERSIZE).decode()
        if _negociate_start(response, ssl_socket, authstr, sid):
            continue

        if f"t='result' i='{sid}-1'>" in response:
            data = b"<en xmlns='x7' u='true' max='300'/>"
            ssl_socket.send(data)
            # Data type voice
            data = (
                f"<iq i='{sid}-3' t='get'>"
                f"<query xmlns='todus:purl' type='1' persistent='false'"
                f" size='{filesize}' room=''></query>"
                "</iq>"
            ).encode("utf-8")
            ssl_socket.send(data)
            continue

        if response.startswith("<ed u='true' max='300'"):
            data = f"<p i='{sid}-4'></p>".encode("utf-8")
            ssl_socket.send(data)
            continue

        if response.startswith(f"<iq o='{phone}@im.todus.cu"):
            match = re.match(r".*put='(.*)' get='(.*)' stat.*", response)
            assert match, f"Unexpected response: {response}"
            up_url = match.group(1).replace("amp;", "")
            down_url = match.group(2)
            return (up_url, down_url)

        if "<not-authorized/>" in response:
            raise AuthenticationError()

        if not response:
            raise EndOfStreamError()


def get_real_url(token: str, url: str) -> str:
    """Get authenticated URL."""
    data: bytes = b""
    authstr = _parse_token(token)[1]
    sid = generate_token(5)
    ssl_socket = _get_socket()

    while True:
        response = ssl_socket.recv(_BUFFERSIZE).decode()
        if _negociate_start(response, ssl_socket, authstr, sid):
            continue

        if f"t='result' i='{sid}-1'>" in response:
            data = (
                f"<iq i='{sid}-2' t='get'>"
                f"<query xmlns='todus:gurl' url='{url}'></query>"
                "</iq>"
            ).encode("utf-8")
            ssl_socket.send(data)
            continue

        if f"t='result' i='{sid}-2'>" in response and "status='200'" in response:
            match = re.match(".*du='(.*)' stat.*", response)
            assert match, f"Unexpected response: {response}"
            return match.group(1).replace("amp;", "")

        if "<not-authorized/>" in response:
            raise AuthenticationError()

        if not response:
            raise EndOfStreamError()
