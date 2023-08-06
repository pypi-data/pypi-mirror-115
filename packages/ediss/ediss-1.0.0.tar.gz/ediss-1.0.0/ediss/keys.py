from typing import Optional
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf import pbkdf2, concatkdf
from cryptography.hazmat.primitives import serialization, keywrap, hashes
from . import Error
from .utils import cached_method
import os
import json

__all__ = [
    'UnexpectedPasswordPresence', 'AbsentRemoteKey', 'RemoteKeyExists', 'InvalidExportLength'
    'EdsPrivateKey', 'EdsPublicKey', 'EdsLocalKeyPair', 'EdsRemoteKeyPair', 'generate']

class UnexpectedPasswordPresence(Error):
    'Password should / should not be present.'
    def __init__(self, should_present: bool) -> None:
        'Initializes with expected password presence.'
        self.shouldPresent = should_present
        super().__init__('Password {} be present.'.format('should' if should_present else 'should not'))

class AbsentRemoteKey(Error):
    'Remote key is absent.'
    def __init__(self) -> None:
        'Initializes a new instance.'
        super().__init__('Remote key is absent.')

class RemoteKeyExists(Error):
    'Remote key already exists.'
    def __init__(self) -> None:
        'Initializes a new instance.'
        super().__init__('Remote key already exists.')

class InvalidExportLength(Error):
    'The binary export byte length is invalid.'
    def __init__(self) -> None:
        'Initializes a new instance.'
        super().__init__('export should be 64 or 96 bytes.')

class EdsPrivateKey:
    'Represents a edwards-curve private key.'
    def __init__(self, 
        x25519_private_key: x25519.X25519PrivateKey, 
        ed25519_private_key: ed25519.Ed25519PrivateKey) -> None:
        'Initializes with private keys. For internal use only.'
        self._x25519Key = x25519_private_key
        self._ed25519Key = ed25519_private_key
    def exportKey(self, password: Optional[bytes]=None) -> dict:
        'Exports the key as mapping. If password is provided, wraps the key with it.'
        key1 = self._x25519Key.private_bytes(
            serialization.Encoding.Raw, 
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption()
        )
        key2 = self._ed25519Key.private_bytes(
            serialization.Encoding.Raw, 
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption()
        )
        if password is not None:
            salt = os.urandom(16)
            wrap_key = pbkdf2.PBKDF2HMAC(hashes.SHA512(), 16, salt, 1000).derive(password)
            key1 = keywrap.aes_key_wrap(wrap_key, key1)
            key2 = keywrap.aes_key_wrap(wrap_key, key2)
            return { 'salt': salt, 'x25519': key1, 'ed25519': key2 }
        return { 'salt': None, 'x25519': key1, 'ed25519': key2 }
    def exportJson(self, password: Optional[bytes]=None) -> str:
        'Exports the key as json. Binary data will be encoded with base64.'
        def encode_bytes(b):
            if isinstance(b, bytes):
                return b.hex()
            raise TypeError('object of type {} is not serializable'.format(b.__class__.__name__))
        export = self.exportKey(password)
        return json.dumps(export, default=encode_bytes)
    def exportBinary(self, password: Optional[bytes]=None) -> bytes:
        'Export the key as bytes.'
        data = self.exportKey(password)
        return (data['salt'] or b'') + data['x25519'] + data['ed25519']
    @staticmethod
    def importKey(data: dict, password: Optional[bytes]=None) -> 'EdsPrivateKey':
        'Imports key from exported mapping.'
        key1 = data['x25519']
        key2 = data['ed25519']
        salt = data['salt']
        if salt is None:
            if password is not None: raise UnexpectedPasswordPresence(False)
            return EdsPrivateKey(
                x25519.X25519PrivateKey.from_private_bytes(key1),
                ed25519.Ed25519PrivateKey.from_private_bytes(key2)
            )
        else:
            if password is None: raise UnexpectedPasswordPresence(True)
            wrap_key = pbkdf2.PBKDF2HMAC(hashes.SHA512(), 16, salt, 1000).derive(password)
            return EdsPrivateKey(
                x25519.X25519PrivateKey.from_private_bytes(keywrap.aes_key_unwrap(wrap_key, key1)),
                ed25519.Ed25519PrivateKey.from_private_bytes(keywrap.aes_key_unwrap(wrap_key, key2))
            )
    @staticmethod
    def importJson(data: str, password: Optional[bytes]=None) -> 'EdsPrivateKey':
        'Imports key from json string.'
        data = json.loads(data)
        data['x25519'] = bytes.fromhex(data['x25519'])
        data['ed25519'] = bytes.fromhex(data['ed25519'])
        if data['salt']:
            data['salt'] = bytes.fromhex(data['salt'])
        return EdsPrivateKey.importKey(data, password)
    @staticmethod
    def importBinary(data: bytes, password: Optional[bytes]=None) -> 'EdsPrivateKey':
        'Imports key from msgpack string.'
        if len(data) == 64:
            salt, x25519, ed25519 = None, data[:32], data[32:]
        elif len(data) == 96:
            salt, x25519, ed25519 = data[:16], data[16:56], data[56:]
        else:
            raise InvalidExportLength
        return EdsPrivateKey.importKey({
            'salt': salt,
            'x25519': x25519,
            'ed25519': ed25519
        }, password)
    @property
    @cached_method
    def publicKey(self) -> 'EdsPublicKey':
        'Returns the corresponding public key.'
        return EdsPublicKey(
            self._x25519Key.public_key(),
            self._ed25519Key.public_key()
        )

class EdsPublicKey:
    'Represents a edwards-curve public key.'
    def __init__(self,
        x25519_public_key: x25519.X25519PublicKey,
        ed25519_public_key: ed25519.Ed25519PublicKey) -> None:
        'Initializes with public keys.'
        self._x25519Key = x25519_public_key
        self._ed25519Key = ed25519_public_key
    def exportKey(self, password: Optional[bytes]=None) -> dict:
        'Exports the key as mapping. If password is provided, wraps the key with it.'
        key1 = self._x25519Key.public_bytes(
            serialization.Encoding.Raw, 
            serialization.PublicFormat.Raw
        )
        key2 = self._ed25519Key.public_bytes(
            serialization.Encoding.Raw, 
            serialization.PublicFormat.Raw
        )
        if password is not None:
            salt = os.urandom(16)
            wrap_key = pbkdf2.PBKDF2HMAC(hashes.SHA512(), 16, salt, 1000).derive(password)
            key1 = keywrap.aes_key_wrap(wrap_key, key1)
            key2 = keywrap.aes_key_wrap(wrap_key, key2)
            return { 'salt': salt, 'x25519': key1, 'ed25519': key2 }
        return { 'salt': None, 'x25519': key1, 'ed25519': key2 }
    def exportJson(self, password: Optional[bytes]=None) -> str:
        'Exports the key as json. Binary data will be encoded with base64.'
        def encode_bytes(b):
            if isinstance(b, bytes):
                return b.hex()
            raise TypeError('object of type {} is not serializable'.format(b.__class__.__name__))
        export = self.exportKey(password)
        return json.dumps(export, default=encode_bytes)
    def exportBinary(self, password: Optional[bytes]=None) -> bytes:
        'Export the key as bytes.'
        data = self.exportKey(password)
        return (data['salt'] or b'') + data['x25519'] + data['ed25519']
    @staticmethod
    def importKey(data: dict, password: Optional[bytes]=None) -> 'EdsPublicKey':
        'Imports key from exported mapping.'
        key1 = data['x25519']
        key2 = data['ed25519']
        salt = data['salt']
        if salt is None:
            if password is not None: raise UnexpectedPasswordPresence(False)
            return EdsPublicKey(
                x25519.X25519PublicKey.from_public_bytes(key1),
                ed25519.Ed25519PublicKey.from_public_bytes(key2)
            )
        else:
            if password is None: raise UnexpectedPasswordPresence(True)
            wrap_key = pbkdf2.PBKDF2HMAC(hashes.SHA512(), 16, salt, 1000).derive(password)
            return EdsPublicKey(
                x25519.X25519PublicKey.from_public_bytes(keywrap.aes_key_unwrap(wrap_key, key1)),
                ed25519.Ed25519PublicKey.from_public_bytes(keywrap.aes_key_unwrap(wrap_key, key2))
            )
    @staticmethod
    def importJson(data: str, password: Optional[bytes]=None) -> 'EdsPublicKey':
        'Imports key from json string.'
        data = json.loads(data)
        data['x25519'] = bytes.fromhex(data['x25519'])
        data['ed25519'] = bytes.fromhex(data['ed25519'])
        if data['salt']:
            data['salt'] = bytes.fromhex(data['salt'])
        return EdsPublicKey.importKey(data, password)
    @staticmethod
    def importBinary(data: bytes, password: Optional[bytes]=None) -> 'EdsPublicKey':
        'Imports key from msgpack string.'
        if len(data) == 64:
            salt, x25519, ed25519 = None, data[:32], data[32:]
        elif len(data) == 96:
            salt, x25519, ed25519 = data[:16], data[16:56], data[56:]
        else:
            raise InvalidExportLength
        return EdsPublicKey.importKey({
            'salt': salt,
            'x25519': x25519,
            'ed25519': ed25519
        }, password)

class EdsLocalKeyPair:
    'Represents a private-public key pair.'
    def __init__(self, private_key: EdsPrivateKey) -> None:
        'Initializes key pair with private key.'
        self._private = private_key
        self._public = private_key.publicKey
    @property
    def privateKey(self) -> EdsPrivateKey:
        'The private component of this pair.'
        return self._private
    @property
    def publicKey(self) -> EdsPublicKey:
        'The public component of this pair.'
        return self._public
    @property
    @cached_method
    def publicDigest(self) -> bytes:
        'Returns the fingerprint of the public keys.'
        export = self._public.exportKey()
        key = export['x25519'] + export['ed25519']
        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(key)
        return hasher.finalize()

class EdsRemoteKeyPair(EdsLocalKeyPair):
    'Represents a private-public-remote key pair.'
    def __init__(self, private_key: EdsPrivateKey) -> None:
        'Initializes key pair with local private key.'
        super().__init__(private_key)
        self._remote = None
    def _check(self, should: bool) -> None:
        'Checks the remote key presence.'
        if should and self._remote is None:
            raise AbsentRemoteKey
        elif not should and self._remote is not None:
            raise RemoteKeyExists
    @property
    def remoteKey(self) -> Optional[EdsPublicKey]:
        'The remote component of this pair. Might be absent.'
        return self._remote
    def receiveKey(self, data: dict, password: Optional[bytes]=None) -> None:
        'Received remote key export mapping.'
        self._check(False)
        self._remote = EdsPublicKey.importKey(data, password)
    def receiveJson(self, data: str, password: Optional[bytes]=None) -> None:
        'Received remote key export json.'
        self._check(False)
        self._remote = EdsPublicKey.importJson(data, password)
    def receiveBinary(self, data: bytes, password: Optional[bytes]=None) -> None:
        'Received remote key export msgpack.'
        self._check(False)
        self._remote = EdsPublicKey.importBinary(data, password)
    def receiveRaw(self, public_key: EdsPublicKey) -> None:
        'Received raw remote key.'
        self._check(False)
        self._remote = public_key
    @property
    @cached_method
    def remoteDigest(self) -> bytes:
        'Returns the fingerprint of the remote keys.'
        self._check(True)
        export = self._remote.exportKey()
        key = export['x25519'] + export['ed25519']
        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(key)
        return hasher.finalize()
    @property
    @cached_method
    def sharedSecret(self) -> bytes:
        'Computes the shared secret of the keys.'
        self._check(True)
        secret = self._private._x25519Key.exchange(self._remote._x25519Key)
        ckdf = concatkdf.ConcatKDFHash(hashes.SHA512(), 32, None)
        return ckdf.derive(secret)

def generate() -> EdsPrivateKey:
    'Generates a edwards-curve private key.'
    return EdsPrivateKey(
        x25519.X25519PrivateKey.generate(), 
        ed25519.Ed25519PrivateKey.generate()
    )
