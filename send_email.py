# -*- coding: utf-8 -*-
# @Author: RZH

"""
part of the project: synchronize.py
send email. (synchronize from local to the mail box)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send(password_: str, file_: str, note_=None) -> bool:
    """
    :param password_: the authorization code.
    :param file_: the file (path) to send.
    :param note_: extra notification.
    :return: a bool value to show if sent successfully.
    """
    sender_ = 'renzihou2012@163.com'
    receiver_ = 'renzihou2012@163.com'

    content = 'Date: %s\nFile name: %s\nNote: %s' % (datetime.now(), file_, note_)
    text = MIMEText(content)

    attachment = MIMEApplication(open(file_, 'rb').read())
    attachment.add_header('Content-Disposition', 'attachment', filename=file_)

    m = MIMEMultipart()
    m.attach(text)
    m.attach(attachment)

    m['Subject'] = 'Synchronize'

    try:  # login and send
        print('---- Synchronizing "%s" to the mail box... ----' % file_)
        url = 'https://smtp.163.com'
        server = smtplib.SMTP(url[url.find('//')+2:])
        server.login(sender_, password_)
        server.sendmail(sender_, receiver_, m.as_string())
        server.quit()
        print('---- Synchronized "%s" successfully ----' % file_)
        return True
    except Exception as e:
        print('---- %s ----' % str(e)[str(e).find('b') + 2:-2])
        return False


if __name__ == '__main__':
    send(password_=input('authorization code: '), file_='matters.txt')
