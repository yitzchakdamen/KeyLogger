from cryptography.fernet import Fernet

class EncryptionKey:

    KEY_FILE = "key.key"  # קובץ שבו שמור המפתח

    @staticmethod
    def generate_or_load_key():
        """
        אם יש קובץ עם מפתח – טוען אותו. אחרת – יוצר ושומר מפתח חדש.
        """
        try:
            with open(EncryptionKey.KEY_FILE, "rb") as key_file:
                key = key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(EncryptionKey.KEY_FILE, "wb") as key_file:
                key_file.write(key)
        return key


class Encryptor:
    key = EncryptionKey.generate_or_load_key()  # טוען את המפתח לזיכרון
    cipher = Fernet(key)

    @staticmethod
    def encrypt_text(text: str) -> str:
        encrypted = Encryptor.cipher.encrypt(text.encode())
        return encrypted.decode()

    @staticmethod
    def decrypt_text(encrypted_text: str) -> str:
        decrypted = Encryptor.cipher.decrypt(encrypted_text.encode())
        return decrypted.decode()


if __name__ == '__main__':
    encryptor = Encryptor()
    text = "Hello, World!"
    encrypted = encryptor.encrypt_text(text)
    print("Encrypted:", encrypted)
    decrypted = encryptor.decrypt_text(encrypted)
    print("Decrypted:", decrypted)


