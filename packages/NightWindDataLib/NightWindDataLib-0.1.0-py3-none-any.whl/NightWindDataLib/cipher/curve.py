import numpy as np
import random


def CurvedPath(content):
    n = 1
    new_list = []

    for sub in content:
        if n % 2 != 0:
            sub = sub[::-1]

        new_list.append(sub)
        n += 1

    return np.array(new_list)


class CurveCipher:
    def __init__(self):
        self.ciphertext = ""
        self.col = random.randint(3, 6)
        self.cipher_array = None

    def RowNumber(self, lens):
        row = lens % self.col

        if row != 0:
            lens += self.col - row

        row = int(lens / self.col)
        return lens, row, self.col

    def FillTable(self, content):
        length = len(content)
        lens, row, col = self.RowNumber(length)

        if lens - length != 0:
            content += (lens - length) * " "

        plain_array = np.array(list(content))
        plain_array = plain_array.reshape(row, col)

        return plain_array

    def PrintCipher(self, content):
        self.cipher_array = CurvedPath(self.FillTable(content))

        for i in np.nditer(self.cipher_array):
            self.ciphertext += str(i)

        print(self.ciphertext)


if __name__ == "__main__":
    plaintext = input("请输入要加密的文字：")
    curve = CurveCipher()

    curve.PrintCipher(plaintext)
    print(f"密钥：{curve.col}")
