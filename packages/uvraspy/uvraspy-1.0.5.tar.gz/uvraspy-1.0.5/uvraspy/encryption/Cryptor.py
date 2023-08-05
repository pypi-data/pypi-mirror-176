import hashlib
import os
import random

from Crypto.Cipher import AES


class Cryptor:
    prohibitednames = [
        "",
    ]
    prohibitedpasswords = [
        "",
        "1234",
        "password",
        "123456",
        "12345678",
        "12345",
        "123456789",
        "qwerty",
        "111111",
        "1234567",
        "0*",

    ]
    names = [
        "Berlin",
        "Hamburg",
        "München",
        "Köln",
        "Frankfurt",
        "Essen",
        "Dortmund",
        "Stuttgart",
        "Düsseldorf",
        "Bremen",
        "Hannover",
        "Duisburg",
        "Nürnberg",
        "Leipzig",
        "Dresden",
        "Wuppertal",
        "Bielefeld",
        "Bonn",
        "Mannheim",
        "Karlsruhe",
        "Wiesbaden",
        "Münster",
        "Augsburg",
        "Ulm",
        "Aachen",
        "Krefeld",
        "Halle",
        "Kiel",
        "Magdeburg",
        "Oberhausen",
        "Lübeck",
        "Freiburg",
        "Erfurt",
        "Kassel",
        "Rostock",
        "Mecklenburg-Vorpommern",
        "Mainz",
        "Saarbrücken",
        "Mülheim",
        "Osnabrück",
        "Oldenburg"
    ]

    def __init__(self):
        self.salt = None
        self.key = None
        self.name = None
        self.BS = AES.block_size
        # initialize the crypto
        # check if PSWD file exists
        if not os.path.isfile('PSWD'):
            print('PSWD file does not exist')

            # create PSWD file
            with open('PSWD', 'wb') as f:
                # generate secure hash from pre-defined password
                # sha256 is not secure enough, we need to use pbkdf2_hmac

                # salt should be a string of 16 bytes containing 0
                self.salt = b'0' * 32
                # hash password
                self.key = self.hash(b"22222")

                # easter egg time:
                # choose a random name from the list
                self.name = self.names[random.randint(0, len(self.names) - 1)]
                # write salt and key to file
                f.write(self.salt + self.key + self.name.encode())

                # change permissions so only the owner can read and write
                os.chmod('PSWD', 0o600)

        # read salt and key from file and use the hash to encrypt the message
        with open('PSWD', 'rb') as f:
            # read the salt that is 32 bytes long
            self.salt = f.read(32)
            # read the key that is also 32 bytes long
            self.key = f.read(32)
            # read the name
            self.name = f.read().decode()

    def hash(self, password):
        # hash the password using pbkdf2_hmac
        print(password)
        return hashlib.pbkdf2_hmac('sha256', password, self.salt, 1000)

    def encrypt(self, message):
        # encrypt the message using cbc mode

        _raw = message.encode() if type(message) == str else message
        cipher = AES.new(self.key, AES.MODE_GCM, mac_len=16)
        ciphertext, tag = cipher.encrypt_and_digest(_raw)
        return ciphertext, tag, cipher.nonce

    def decrypt(self, ciphertext, tag, nonce):
        # decrypt the message
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce, mac_len=16)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag) if tag is not None else cipher.decrypt(ciphertext)
        return plaintext

    def updatekey(self, key):
        # update the key
        self.key = key

        # also update the PSWD file
        with open('PSWD', 'wb') as f:
            f.truncate(0)
            f.write(self.salt + self.key + self.name.encode())

    def updateName(self, name):
        self.name = name
        if name in self.prohibitednames:
            raise Exception("Name is prohibited")
        with open('PSWD', 'wb') as f:
            f.truncate(0)
            f.write(self.salt + self.key + self.name.encode())
            print("Name updated")


cryptor = Cryptor()
