class Error(Exception):
    'General base class for all errors.'

from typing import Optional
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from .keys import EdsLocalKeyPair, EdsRemoteKeyPair, generate, EdsPrivateKey
from .cipher import * 
from .eddsa import EdsSigner, EdsVerifier

__all__ = ['LocalScheme', 'EdsScheme', 'Error']

class LocalScheme(EdsLocalKeyPair):
    'Represents a local edwards-curve scheme.'
    def getSigner(self) -> EdsSigner:
        'Gets a signer for data signature.'
        return EdsSigner(self._private._ed25519Key)
    def sign(self, data: bytes) -> bytes:
        'Signs the data with edwards-curve public key.'
        return EdsSigner(self._private._ed25519Key, data).finalize()
    def getVerifier(self) -> EdsVerifier:
        'Gets a verifier for data verification.'
        return EdsVerifier(self._public._ed25519Key)
    def verify(self, data: bytes, signature: bytes) -> bool:
        'Verifies the data with edwards-curve public key.'
        return EdsVerifier(self._public._ed25519Key, data).finalize(signature)
    def encrypt(self, data: bytes) -> bytes:
        'Encrypts the data with exchanged secret.'
        skey = derive_ephemeral_private(self._public._x25519Key)
        return skey.info + encrypt(skey.key, data)
    def decrypt(self, data: bytes) -> bytes:
        'Decrypts the data with exchanged secret.'
        try:
            eph_bytes, salt, data = data[:32], data[32:48], data[48:]
            ephemeral = X25519PublicKey.from_public_bytes(eph_bytes)
            skey = derive_ephemeral_public(self._private._x25519Key, salt, ephemeral)
            return decrypt(skey.key, data)
        except MalformedCiphertext: raise
        except Exception:
            raise MalformedCiphertext
    @staticmethod
    def generate() -> 'LocalScheme':
        'Constructs a local scheme with generated keys.'
        return LocalScheme(generate())

class EdsScheme(EdsRemoteKeyPair):
    'Represents a private-public-remote edwards-curve scheme.'
    def getSigner(self) -> EdsSigner:
        'Gets a signer for data signature.'
        return EdsSigner(self._private._ed25519Key)
    def sign(self, data: bytes) -> bytes:
        'Signs the data with edwards-curve public key.'
        return EdsSigner(self._private._ed25519Key, data).finalize()
    def getVerifier(self) -> EdsVerifier:
        'Gets a verifier for data verification.'
        self._check(True)
        return EdsVerifier(self._remote._ed25519Key)
    def verify(self, data: bytes, signature: bytes) -> bool:
        'Verifies the data with edwards-curve public key.'
        self._check(True)
        return EdsVerifier(self._remote._ed25519Key, data).finalize(signature)
    def encrypt(self, data: bytes) -> bytes:
        'Encrypts the data with exchanged secret.'
        self._check(True)
        skey = derive_ephemeral_private(self._remote._x25519Key)
        return skey.info + encrypt(skey.key, data)
    def decrypt(self, data: bytes) -> bytes:
        'Decrypts the data with exchanged secret.'
        try:
            eph_bytes, salt, data = data[:32], data[32:48], data[48:]
            ephemeral = X25519PublicKey.from_public_bytes(eph_bytes)
            skey = derive_ephemeral_public(self._private._x25519Key, salt, ephemeral)
            return decrypt(skey.key, data)
        except MalformedCiphertext: raise
        except Exception:
            raise MalformedCiphertext
    @staticmethod
    def generate() -> 'EdsScheme':
        'Constructs a local scheme with generated keys.'
        return EdsScheme(generate())
    @staticmethod
    def fromPrivateKey(data: dict, password: Optional[bytes]=None) -> 'LocalScheme':
        'Constructs local scheme from private key export.'
        return LocalScheme(EdsPrivateKey.importKey(data, password))
    @staticmethod
    def fromPrivateJson(data: str, password: Optional[bytes]=None) -> 'LocalScheme':
        'Constructs local scheme from json private key.'
        return LocalScheme(EdsPrivateKey.importJson(data, password))
    @staticmethod
    def fromPrivateBinary(data: bytes, password: Optional[bytes]=None) -> 'LocalScheme':
        'Constructs local scheme from binary private key.'
        return LocalScheme(EdsPrivateKey.importBinary(data, password))