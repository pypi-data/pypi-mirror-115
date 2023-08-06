import string
import random


def coPrime(a, b):
    smaller = min(a, b)

    for i in range(smaller, 1, -1):
        if a % i == 0 and b % i == 0:
            return False

    return True


def modInverse(K, N):
    for i in range(1, N):
        if K * i % N == 1:
            return i

    return None


class Multiplication:
    def __init__(self):
        self.letter = string.ascii_lowercase
        self.ciphertext = ""
        self.decrypt_content = ""
        self.keys = []

    def encrypt(self, content, K2=0):
        length = len(self.letter)

        for i in range(2, length - 1):
            if coPrime(i, length):
                self.keys.append(i)

        K1 = random.choice(self.keys)

        for char in content:
            if char in self.letter:
                M_index = self.letter.index(char)
                C_index = (M_index * K1 + K2) % length
                cipher_char = self.letter[C_index]
                self.ciphertext += cipher_char
            else:
                self.ciphertext += char

        return self.ciphertext, K1, K2

    def decrypt(self, content, K1, K2=0):
        length = len(self.letter)
        key_inverse = modInverse(K1, length)

        for char in content:
            if char in self.letter:
                C_index = self.letter.index(char)
                M_index = (C_index - K2) * key_inverse % length
                decrypt_char = self.letter[M_index]
                self.decrypt_content += decrypt_char
            else:
                self.decrypt_content += char

        return self.decrypt_content, key_inverse


if __name__ == '__main__':
    plaintext = input("请输入要加密的文字：")
    multi = Multiplication()

    cipher, key1, key2 = multi.encrypt(plaintext,
                                       K2=random.randint(0, len(multi.letter)))
    print(f"明文：{plaintext}")
    print(f"密文：{cipher}")
    print(f"密钥：{key1}, {key2}")

    print("——————————分割线——————————")

    decrypted, key = multi.decrypt(cipher, key1, key2)
    print(f"密文：{cipher}")
    print(f"密钥：{key}")
    print(f"明文：{decrypted}")
