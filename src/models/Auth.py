from passlib.hash import pbkdf2_sha256 as sha256

class AuthModel():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)