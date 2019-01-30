# -*- coding: utf-8 -*-
# @Author: RZH

"""
define the object des, used to encrypt or decrypt your diary
"""

import pyDes


def des(key):
    return pyDes.des(key, pyDes.CBC, '********', pad=None, padmode=pyDes.PAD_PKCS5)
