from cryptography import exceptions
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf import hkdf
from cryptography.hazmat.primitives.ciphers import aead
from . import Error
from .utils import cached_method
import os

__all__ = [
    'encrypt', 'decrypt', 'SymmetricKey', 'MalformedCiphertext',
    'derive_ephemeral_private', 'derive_ephemeral_public']

class MalformedCiphertext(Error):
    'Cipher text is invalid.'

def encrypt(key: bytes, data: bytes) -> bytes:
    'Encrypts the data with specific key.'
    cipher = aead.AESGCM(key)
    nonce = os.urandom(16)
    enciphered = cipher.encrypt(nonce, data, None)
    return nonce + enciphered

def decrypt(key: bytes, data: bytes) -> bytes:
    'Decrypts the data with specific key.'
    cipher = aead.AESGCM(key)
    nonce, enciphered = data[:16], data[16:]
    try:
        return cipher.decrypt(nonce, enciphered, None)
    except exceptions.InvalidTag:
        raise MalformedCiphertext

class SymmetricKey:
    'Represents a symmetric key used for encrypting.'
    def __init__(self, key: bytes, salt: bytes, ephemeral: x25519.X25519PublicKey) -> None:
        'Initializes with key, salt and ephemeral key. For internal use only.'
        self._key = key
        self._salt = salt
        self._ephemeral = ephemeral
    @property
    def key(self) -> bytes:
        'The key in bytes.'
        return self._key
    @property
    @cached_method
    def info(self) -> bytes:
        'The information about this key.'
        return self._ephemeral.public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw
        ) + self._salt
    @staticmethod
    def fromInfo(key: bytes, info: bytes) -> 'SymmetricKey':
        'Constructs an instance from key and information.'
        pbytes, salt = info[:32], info[32:]
        return SymmetricKey(key, salt, x25519.X25519PublicKey.from_public_bytes(pbytes))

def derive_ephemeral_private(key: x25519.X25519PublicKey) -> SymmetricKey:
    'Derives a symmetric key from public key via ephemeral keys.'
    ephemeral = x25519.X25519PrivateKey.generate()
    secret = ephemeral.exchange(key)
    salt = os.urandom(16)
    key = hkdf.HKDF(hashes.SHA512(), 32, salt, None).derive(secret)
    return SymmetricKey(key, salt, ephemeral.public_key())

def derive_ephemeral_public(key: x25519.X25519PrivateKey, salt: bytes, ephemeral: x25519.X25519PublicKey) -> SymmetricKey:
    'Derives a symmetric key from private and ephemeral keys.'
    secret = key.exchange(ephemeral)
    key = hkdf.HKDF(hashes.SHA512(), 32, salt, None).derive(secret)
    return SymmetricKey(key, salt, ephemeral)
