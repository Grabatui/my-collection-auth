from binascii import hexlify
from hashlib import sha256, pbkdf2_hmac

from app.core.domain.common import ConvertSourceTokenInterface, EncodePasswordInterface


class EncodePasswordAction(EncodePasswordInterface):
    def __init__(self, salt: str):
        self.salt = salt

    def run(self, decodedPassword: str) -> str:
        encodedPassword = pbkdf2_hmac(
            'sha256',
            decodedPassword.encode('utf-8'),
            self.salt.encode('utf-8'),
            100000
        )

        return hexlify(encodedPassword).decode('utf-8')


class ConvertSourceTokenAction(ConvertSourceTokenInterface):
    def run(self, raw_token: str) -> str:
        return sha256(raw_token.encode('utf-8')).hexdigest()
