import base64
from typing import Union

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

BytesLike = Union[bytes, bytearray]


class RSAManager:
    def __init__(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def load_private_key(self):
        with open(self.private_key_path, "rb") as f:
            return RSA.import_key(f.read())

    def load_public_key(self):
        with open(self.public_key_path, "rb") as f:
            return RSA.import_key(f.read())

    def encrypt_aes_key_with_rsa(self, aes_key: BytesLike, public_key) -> str:
        cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        enc = cipher.encrypt(bytes(aes_key))
        return base64.b64encode(enc).decode("utf-8")

    def decrypt_aes_key_with_rsa(self, encrypted_aes_key_b64: str, private_key) -> bytes:
        enc = base64.b64decode(encrypted_aes_key_b64)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        return cipher.decrypt(enc)

    def sign_data(self, original_data: BytesLike, private_key) -> str:
        h = SHA256.new(bytes(original_data))
        sig = pkcs1_15.new(private_key).sign(h)
        return base64.b64encode(sig).decode("utf-8")

    def verify_signature(self, original_data: BytesLike, signature_b64: str, public_key) -> bool:
        try:
            sig = base64.b64decode(signature_b64)
            h = SHA256.new(bytes(original_data))
            pkcs1_15.new(public_key).verify(h, sig)
            return True
        except (ValueError, TypeError):
            return False


if __name__ == "__main__":
    mgr = RSAManager()
    priv = mgr.load_private_key()
    pub = mgr.load_public_key()

    aes_key = b"A" * 32
    enc = mgr.encrypt_aes_key_with_rsa(aes_key, pub)
    dec = mgr.decrypt_aes_key_with_rsa(enc, priv)
    print("[+] Encapsulation OK:", dec == aes_key)

    data_asli = b"Ini data asli sebelum dienkripsi"
    sig = mgr.sign_data(data_asli, priv)
    ok = mgr.verify_signature(data_asli, sig, pub)
    print("[+] Signature valid:", ok)
