# -*- coding: utf-8 -*-
# @Author: RZH

"""
define the Diary class which is the main part of the project 'Diary'
"""

from datetime import datetime
from src.basicfunctions import get_int
from src.encrypt_decrypt import des


class Diary(object):
    """
    The class of diaries.
    """

    current_file = str()  # the encrypted diary book file
    dates = list()  # a sequence of the dates of all the diaries
    diaries = list()  # a sequence of all the diaries
    __password = '********'  # the password of the file
    saved = True  # a flag to represent if the file is saved
    des = des(__password)
    __slots__ = ('text', 'date')

    def __init__(self, text: list, date: str):
        """
        The initiate method of Diary objects
        :param text: The content of your diary
        :param date: The date of your diary, in form of 'yy-mm-dd'
        """
        self.text = text  # each element (string) in this list is a paragraph
        self.date = date

    def view_page(self):
        """
        print the context of a page of diary.
        :return: self
        """
        print('-' * 20)
        print('DATE: %s' % self.date)
        print('TEXT: ')
        for index, para in enumerate(self.text):
            print('%d: %s' % (index, para))
        print('-' * 20)
        return self

    def edit_page(self):
        """
        Edit a single page in your diary
        :return: self
        """
        print('==== Edit a Paragraph ====')
        print('The previous one: ')
        self.view_page()  # print the previous page.
        print('Choose one paragraph to edit: ')
        index_ = get_int('#: ', range_=range(len(self.text)))  # the paragraph to edit
        self.text[index_] = input('New text: ')  # update the paragraph
        print('==== Paragraph Edited ====')
        return self

    @classmethod
    def new_page(cls):
        """
        add a record.
        :return: cls
        """
        print('==== Add a New Page ====')
        new_date = input('Please input the date (yy-mm-dd): ')
        new_date = str(datetime.now()).split(' ')[0] \
            if new_date.lower() == 'today' else new_date
        new_text = [input('Please input the content: ')]
        if new_date in cls.dates:  # already has a same-date page, then add a paragraph to this page
            cls.diaries[cls.dates.index(new_date)].text += new_text
        else:  # create a new page
            cls.dates.append(new_date)
            cls.diaries.append(Diary(text=new_text, date=new_date))
        cls.saved = False
        print('==== New Page Added ====')
        return cls

    @classmethod
    def content(cls):
        """
        print records in lines.
        :return: The selected Diary object
        """
        for index, each in enumerate(cls.diaries):
            print('%d: %s\t%s......' % (index, each.date, each.text[0][:10]))  # print the abstract
        return cls.diaries[get_int('Choose one page of diary: ', range_=range(len(cls.diaries)))]  # select a page

    @classmethod
    def search(cls, keyword_: str):
        """
        search certain diaries according to a keyword
        :param keyword_: The keyword
        :return: A selected diary
        """
        target = list()  # pages that contain the keyword
        for each in cls.diaries:
            if keyword_ in ''.join(each.text):  # keyword in content
                target.append(each)  # wait fot select
        for index, each in enumerate(target):  # print all the results
            print('%d: %s\t%s......' % (index, each.date, each.text[0][:10]))  # print the abstract
        return target[get_int(
            'Choose one page of diary: ', range_=range(len(target))
            )] if len(target) > 0 else cls.diaries[0]  # select one page

    @classmethod
    def recall(cls, keywords_: list):
        """
        using keywords to recall your memories about certain topics
        :param keywords_: a sequence of keywords
        :return: None
        """
        for each in cls.diaries:
            for keyword_ in keywords_:
                if keyword_ in ''.join(each.text):  # keyword in content
                    each.view_page()
                    break
        return None

    @classmethod
    def del_page(cls):
        """
        delete a record.
        :return: cls
        """
        print('**** WARNING: THIS ACTION CANNOT UNDO ****\n==== Delete a Page ==== ')
        select = cls.content()  # remove the Diary object from Diary.diaries
        if get_int('Delete one paragraph in it (0) or the whole page (1)? ', range_=(0, 1)):
            cls.diaries.remove(select)  # delete the whole page
        else:
            # delete a single paragraph
            select.view_page()
            select.text.remove(
                select.text[get_int('Choose a paragraph to delete: ', range_=range(len(select.text)))]
            )
        print('==== Page Deleted ====')
        cls.saved = False  # flag
        return cls

    @classmethod
    def save(cls):
        """
        save your diary to files/filename.dr
        :return: cls
        """
        cls.diaries = sorted(cls.diaries, key=lambda x: x.date.replace('-', ''))  # sort the diaries in time order

        if not cls.current_file:
            cls.current_file = input('Please name the file (ends in .dr): ')

        content = '#d#'.join(['%s#t#%s' % (each.date, str(each.text)) for each in cls.diaries])
        with open(file=cls.current_file, mode='wb') as f:
            f.write(cls.des.encrypt(content.encode('utf-8')))

        print('==== Diary Saved ====')
        cls.saved = True  # flag
        return cls

    @classmethod
    def load(cls, file_: str, password_: str = __password):
        """
        Import another diary book from local file (which is encrypted). If the file does not exist, create one.
        :param file_: The encrypted file path, should look like: files/filename.dr
        :param password_: The password for new diary book
        :return: cls
        """
        print('==== Import a Diary ====')
        if not cls.saved and input('Save the current file? <y/n> ') == 'y':
            cls.save()  # save the current file
        cls.init()  # initiate the diaries list

        cls.set_password(password_)
        with open(file=file_, mode='rb') as f:
            try:
                content = cls.des.decrypt(f.read()).decode()
            except UnicodeDecodeError:  # some bytes cannot be converted to unicode
                print('**** Wrong Password ****')
                cls.current_file = 'files/Diary_Book_tmp.dr'  # turn to the temp diary book
                return None

        for each in content.split('#d#'):  # separate different dates
            tmp = each.split('#t#')  # separate date and content
            cls.dates.append(tmp[0])
            cls.diaries.append(Diary(text=eval(tmp[1]), date=tmp[0]))  # import a new page

        cls.current_file = file_
        print('==== Diary Imported ====')
        return cls

    @classmethod
    def set_password(cls, p: str):
        """
        Set the password of the diary book.
        :param p: new password
        :return: cls
        """
        cls.__password = p  # set new password
        cls.des = des(cls.__password)
        return cls

    @classmethod
    def init(cls):
        """
        clear all the diaries from Diary.diaries
        :return: cls
        """
        cls.dates = list()
        cls.diaries = list()
        return cls

    @classmethod
    def change_file(cls, new_file: str):
        """
        specify another diary book.
        :param new_file: the new diary book
        :return: cls
        """
        cls.current_file = new_file
        return cls

    @classmethod
    def num_of_pages(cls) -> int:
        """
        return the number of pages, used to refuse view request when there are no diaries
        :return: the number of pages
        """
        return len(cls.diaries)


if __name__ == '__main__':
    pass
