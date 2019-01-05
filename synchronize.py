# -*- coding: utf-8 -*-
# @Author: RZH

"""
main part of the project: synchronize.py
synchronize files in the current folder to the mail box or reverse.
"""

from datetime import datetime
from send_email import send
from receive_email import receive
from basicfunctions import get_int


def guide(password: str) -> None:
    """
    main function. calls other functions.
    :param password: the authorization code of the mail.
    :return: None
    """
    while True:
        print('=' * 50)
        print(
            'Choose a function from:\n'
            '0. Set password\n'
            '1. Synchronize to the mail box\n'
            '2. Synchronize from the mail box\n'
            '3. Quit'
        )
        mode = get_int('#: ', range_=[0, 1, 2, 3])
        print('=' * 50)

        if mode == 0:  # set password
            print('=' * 19 + 'Set Password' + '=' * 19)
            print('-------- E-Mail Address: renzihou2012@163.com --------')
            password = input('Please input your authorization code: ')
            print('---- Password Set ----')
            print('=' * 50)

        elif mode == 1:  # synchronize to the mail box
            print('=' * 11 + 'Synchronize to the mail box' + '=' * 12)
            files = [i.strip() for i in input('Please input file name (use "," to connect): ').split(',')]
            for each in files:
                try:
                    open(each, 'rb')
                except FileNotFoundError:
                    print('---- Error: File "%s" does not exist ----' % each)
                else:
                    send(password, each, note_=input('Extra note for "%s": ' % each))
            print('=' * 50)

        elif mode == 2:  # synchronize from the mail box
            print('=' * 10 + 'Synchronize from the mail box' + '=' * 11)
            while True:
                date = input('Check the mails after date (yy-mm-dd-hh-mm): ')
                try:
                    datetime.strptime(date, '%Y-%m-%d-%H-%M')
                except ValueError:
                    print('---- Error: Format not match ----')
                else:
                    break

            mails = receive(password, required_date_=date)

            if len(mails) == 0:  # no files to synchronize
                print('---- No files to synchronize ----')
            else:
                print('--------')
                for n, each in enumerate(mails):  # select a file to synchronize
                    print('%d: %s\t%s\t// %s' % (n, each.r_date, each.name, each.note))
                print('--------')

                indexes = [i.strip() for i in input('Synchronize #: ').split(',')]
                for each in indexes:
                    mails[int(each)].update()
                    print('---- "%s" has been synchronized from the mail box ----' % mails[int(each)].name)
            print('=' * 50)

        elif mode == 3:  # quit
            break

    return None


if __name__ == '__main__':
    print('-------- E-Mail Address: renzihou2012@163.com --------')
    guide(input('Please input your authorization code: '))
