from enum import IntEnum
from typing import Any
from cryptography.hazmat.primitives import hmac, hashes
from cryptography import exceptions
from . import EdsScheme, Error
import socket

__all__ = ['PacketDropped', 'PatchMethod', 'SocketPatch']

class PacketDropped(Error):
    'Packet is invalid due to security reasons.'

class PatchMethod(IntEnum):
    'The method for patching.'
    # use shared secret to calculate message authentication code.
    PmHmac = 0
    # prepends signature of each chunk of message.
    PmSign = 1
    # encrypts the whole channel.
    PmCiph = 2
    # encrypts and signs the message.
    PmFull = 3

class SocketPatch:
    'A patch that enables socket to negotiate its secret and secures the connection.'
    def __init__(self, sock: socket.socket, pmethod: PatchMethod) -> None:
        'Initializes with inner socket.'
        self._socket = sock
        self._scheme = EdsScheme.generate()
        self._method = pmethod
    def __getattr__(self, name: str) -> Any:
        'Gets attribute from the inner socket.'
        return getattr(self._socket, name)
    def __setattr__(self, name: str, value: Any) -> None:
        'Sets attribute to the inner socket.'
        setattr(self._socket, name, value)
    def __delattr__(self, name: str) -> None:
        'Deletes attribute from the inner socket.'
        delattr(self._socket, name)
    def negotiate(self, first: bool) -> None:
        'Negotiates the key with peer.'
        if first:
            self._socket.send(self._scheme.publicKey.exportBinary())
            self._scheme.receiveBinary(self._socket.recv(1024))
        else:
            self._scheme.receiveBinary(self._socket.recv(1024))
            self._socket.send(self._scheme.publicKey.exportBinary())
    def send(self, b: bytes) -> None:
        'Processes and sends the data.'
        if self._method == PatchMethod.PmHmac:
            mac = hmac.HMAC(self._scheme.sharedSecret, hashes.SHA256())
            mac.update(b)
            b = mac.finalize() + b
        elif self._method == PatchMethod.PmSign:
            b = self._scheme.sign(b) + b
        elif self._method == PatchMethod.PmCiph:
            b = self._scheme.encrypt(b)
        elif self._method == PatchMethod.PmFull:
            b = self._scheme.sign(b) + self._scheme.encrypt(b)
        self._socket.send(b)
    def recv(self, n: int) -> bytes:
        'Receives and processes the data.'
        b = self._socket.recv(n)
        if self._method == PatchMethod.PmHmac:
            mac = hmac.HMAC(self._scheme.sharedSecret, hashes.SHA256())
            tag, b = b[:32], b[32:]
            mac.update(b)
            try:
                mac.verify(tag)
            except exceptions.InvalidSignature:
                raise PacketDropped
        elif self._method == PatchMethod.PmSign:
            sig, b = b[:64], b[64:]
            if not self._scheme.verify(b, sig):
                raise PacketDropped
        elif self._method == PatchMethod.PmCiph:
            try:
                b = self._scheme.decrypt(b)
            except exceptions.InvalidTag:
                raise PacketDropped
        elif self._method == PatchMethod.PmFull:
            sig, b = b[:32], b[32:]
            if not self._scheme.verify(b, sig):
                raise PacketDropped
            try:
                b = self._scheme.decrypt(b)
            except exceptions.InvalidTag:
                raise PacketDropped
        return b