# # from django.test import TestCase
# #
# # # Create your tests here.
#
# from cryptography.fernet import Fernet
# from django.conf import settings
#
# # Функция для генерации ключа шифрования
# def generate_encryption_key():
#     key = Fernet.generate_key()
#     return key
#
# # Функция для получения ключа шифрования пользователя
# def get_user_encryption_key(user):
#     # Здесь можно реализовать вашу логику получения ключа шифрования для конкретного пользователя
#     # В этом примере мы возвращаем ключ из атрибута `encryption_key` модели пользователя
#     return user.encryption_key
#
# # Функция для шифрования данных
# def encrypt_data(key, data):
#     f = Fernet(key)
#     encrypted_data = f.encrypt(data.encode())
#     return encrypted_data
#
# # Функция для расшифровки данных
# def decrypt_data(key, encrypted_data):
#     f = Fernet(key)
#     decrypted_data = f.decrypt(encrypted_data).decode()
#     return decrypted_data
#
# # Пример использования:
#
# # Генерация ключа шифрования
# encryption_key = generate_encryption_key()
#
# # Шифрование данных
# data = "Hello, World!"
# encrypted_data = encrypt_data(encryption_key, data)
#
# # Расшифровка данных
# decrypted_data = decrypt_data(encryption_key, encrypted_data)
#
# # Вывод результатов
# print(f"Original Data:", data)
# print(f"Encrypted Data: {encrypted_data}")
# print(f"Decrypted Data:", decrypted_data)
