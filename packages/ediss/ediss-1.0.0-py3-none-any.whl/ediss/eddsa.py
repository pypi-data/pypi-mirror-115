from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import hashes
from . import Error

__all__ = ['ObjectFinalized', 'EdsSigner', 'EdsVerifier']

class ObjectFinalized(Error):
    'Signer / verifier already finalized.'
    def __init__(self, object_name: str) -> None:
        'Initializes a new instance.'
        self.objectName = object_name
        super().__init__('{} already finalized.'.format(object_name))

class EdsSigner:
    'A edwards-curve digital signature signer.'
    def __init__(self, key: ed25519.Ed25519PrivateKey, data: bytes=b'') -> None:
        'Initializes with private key. For internal use only.'
        self._key = key
        self._hash = hashes.Hash(hashes.SHA384())
        self._hash.update(data)
    def _check(self) -> None:
        'Checks the validity of this signer.'
        if self._hash is None:
            raise ObjectFinalized
    def update(self, data: bytes) -> None:
        'Updates the internal hash.'
        self._check()
        self._hash.update(data)
    def finalize(self) -> bytes:
        'Signs the provided data.'
        self._check()
        signature = self._key.sign(self._hash.finalize())
        self._hash = None
        return signature

class EdsVerifier:
    'A edwards-curve digital signature verifier.'
    def __init__(self, key: ed25519.Ed25519PublicKey, data: bytes=b'') -> None:
        'Initializes with public key. For internal use only.'
        self._key = key
        self._hash = hashes.Hash(hashes.SHA384())
        self._hash.update(data)
    def _check(self) -> None:
        'Checks the validity of this signer.'
        if self._hash is None:
            raise ObjectFinalized
    def update(self, data: bytes) -> None:
        'Updates the internal hash.'
        self._check()
        self._hash.update(data)
    def finalize(self, signature: bytes) -> bool:
        'Verifies the provided data with provided signature.'
        self._check()
        try:
            self._key.verify(signature, self._hash.finalize())
            return True
        except InvalidSignature:
            return False
        finally:
            self._hash = None