# -*- coding:utf-8 -*-
# @Author: RZH

import pyDes


# encrypt
def encrypt_file(f: str, key: str, iv: str) -> None:
    """
    generate an encrypted file end up with '.des' in the original folder.
    :param f: the file path.
    :param key: an 8-bytes password. using to encrypt.
    :param iv: an 8-bytes initial value. using to encrypt.
    :return: no return. just encrypt the file.
    """
    des = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    with open(f, 'rb') as f1:
        data = f1.read()
        c = des.encrypt(data)
        with open(f+'.des', 'wb') as f2:
                f2.write(c)
                f2.close()
        f1.close()
    return None


# decrypt
def decrypt_file(f: str, key: str, iv: str) -> None:
    """
    generate a decrypted file in the original folder.
    :param f: the encrypted file path.
    :param key: the 8-bytes password. using to decrypt.
    :param iv: the 8-bytes initial value. using to decrypt.
    :return: no return.
    """
    des = pyDes.des(key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    with open(f, 'rb') as f1:
        data = f1.read()
        c = des.decrypt(data)
        with open(f.replace('.des', ''), 'wb') as f2:
                f2.write(c)
                f2.close()
        f1.close()
    return None


if __name__ == '__main__':
    my_file = input('please input the file path: ')
    if my_file[-4:] == '.des':
        print('decrypt file...')
        my_key = str(input('please input the 8-bytes password: '))
        my_iv = str(input('please input the 8-bytes initial value: '))
        decrypt_file(my_file, my_key, my_iv)
    else:
        print('encrypt file...')
        my_key = str(input('please input new 8-bytes password: '))
        my_iv = str(input('please input new 8-bytes initial value: '))
        encrypt_file(my_file, my_key, my_iv)
