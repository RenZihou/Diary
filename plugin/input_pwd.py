# -*- coding: utf-8 -*-
# @Author: RZH

"""
this plugin provides a method that replace your password with '*' to protect user's private
"""

from sys import stdout
from msvcrt import getch


def input_pwd(s: str = '', len_: int = 0) -> str:
    """
    get password while replacing the password with '*' on console
    :param s: hint word.
    :param len_: required length of the password.
    :return:
    """
    print(s, end='')
    pwd = list()

    while True:
        ch = getch().decode()
        while ch not in '\r\n':  # typing password
            if ch == '\b':  # backspace
                stdout.write('\b \b')
                pwd.pop()
            else:
                stdout.write('*')
                pwd.append(ch)
            stdout.flush()
            ch = getch().decode()

        if len_ and len_ != len(pwd):
            print('\nPassword not satisfy the length requirement. \nInput again: ', end='')
            pwd.clear()
        else:
            stdout.write('\n')
            break

    return ''.join(pwd)


if __name__ == '__main__':
    pass
