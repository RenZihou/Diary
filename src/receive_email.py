# -*- coding: utf-8 -*-
# @Author: RZH

"""
part of the project: synchronize.py
receive email. (synchronize from the mail box to local)
"""

from datetime import datetime
import poplib
from email.header import decode_header
from email.parser import Parser


class Mails(object):
    """
    a class of selected mails (whose subject is 'Synchronize').
    """
    __slots__ = ['name', 'r_date', 'data', 'note']

    def __init__(self, name_: str, r_date_: str, data_: bytes, note_: str):
        """
        :param name_: file name
        :param r_date_: a string in form of 'yy-mm-dd-hh-mm'. the receive date
        :param data_: the attachment
        :param note_: extra note
        """
        self.name = name_
        self.r_date = r_date_
        self.data = data_
        self.note = note_

    def update(self):
        """
        write to local file.
        :return: None
        """
        with open(self.name, 'wb') as f:
            f.write(self.data)
        return None


mails = []


def decode_str(s) -> str:  # decode the header
    """
    decode the binary code from internet to utf-8 which can be recognized.
    :param s: the binary string
    :return: the utf-8 string
    """
    print(type(s))
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def receive(
        password_: str, required_date_: str,
        host_: str = 'pop.163.com', user_: str = ''  TODO: finish your own info.
) -> list:
    """
    traversal the mails and download the attachments
    which are satisfied with requirement.
    :param host_: mail host
    :param user_: user
    :param password_: the authorization code
    :param required_date_: In form of 'yy-mm-dd-hh-mm'.
    only receive the mails later than this date
    :return: a list of objects
    """
    # login
    try:
        pop_conn = poplib.POP3(host_)
        pop_conn.user(user_)
        pop_conn.pass_(password_)
    except Exception as e:
        print('---- Error: %s ----' % str(e)[str(e).find('ERR') + 4:-1])
    else:
        num = len(pop_conn.list()[1])  # count of mails

        # traversal each mail
        for i in range(num, 0, -1):
            lines = pop_conn.retr(i)[1]
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # the original content of the mail
            r_date = lines[20].decode('utf-8')[6:]
            # line 20: the beginning of the content which is the receive date.
            name = lines[21].decode('utf-8')[11:]
            # line 21: the name of the attachment.
            note = lines[22].decode('utf-8')[6:]
            # line 22: the name of the attachment.
            msg = Parser().parsestr(msg_content)  # the mail

            receive_date = datetime.strptime(
                msg.get("Date")[5:21], '%d %b %Y %H:%M'
            )
            date_ = datetime.strptime(required_date_, '%Y-%m-%d-%H-%M')
            if receive_date < date_:
                # stop when the receive date is earlier than the required date.
                break

            subject = decode_str(msg.get('subject', ''))
            if subject == 'Synchronize':
                for part in msg.walk():
                    filename = part.get_filename()  # get attachments
                    if filename:  # attachment exists
                        data = part.get_payload(decode=True)
                        mails.append(Mails(
                            name_=name, r_date_=r_date, data_=data, note_=note
                        ))

        pop_conn.quit()
    return mails


if __name__ == '__main__':
    print(receive(
        password_=input('authorization code: '), required_date_='2020-1-1-0-0'
    ))
