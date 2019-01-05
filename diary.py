# -*- coding: utf-8 -*-
# @Author: RZH

"""
Your private diary book.
"""

from os import path, remove
from datetime import datetime
from basicfunctions import get_int
from encrypt_decrypt import encrypt_file, decrypt_file  # safety module
from send_email import send  # sync module
from receive_email import receive  # sync module


class Diary(object):
    """
    The class of diaries.
    """

    current_file = str()  # the encrypted diary book file
    dates = list()  # a sequence of the dates of all the diaries
    diaries = list()  # a sequence of all the diaries
    __password = str()  # the password of the file
    saved = True  # a flag to represent if the file is saved
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
        Search certain diaries according to a keyword
        :param keyword_: The keyword
        :return: A selected diary
        """
        target = list()  # pages that contain the keyword
        for each in cls.diaries:
            if keyword_ in ''.join(each.text):  # keyword in content
                target.append(each)  # wait fot select
        for index, each in enumerate(target):  # print all the results
            print('%d: %s\t%s......' % (index, each.date, each.text[0][:10]))  # print the abstract
        return target[get_int('Choose one page of diary: ', range_=range(len(target)))]  # select one page

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
        cls.diaries.remove(cls.content())  # remove the Diary object from Diary.diaries
        print('==== Page Deleted ====')
        cls.saved = False  # flag
        return cls

    @classmethod
    def save(cls):
        """
        save records to the file 'matters.txt'
        :return: cls
        """
        if not cls.current_file:
            cls.current_file = input('Please name the file (end in .txt.des): ')

        with open(file=cls.current_file.replace('.des', ''), mode='w', encoding='utf-8') as f:
            for each in cls.diaries:
                f.write('%s#t#%s\n' % (each.date, str(each.text)))  # write the records
        encrypt_file(cls.current_file.replace('.des', ''), cls.__password, '********')  # encrypt the file
        remove(cls.current_file.replace('.des', ''))  # delete the unencrypted file
        
        print('==== Diary Saved ====')
        cls.saved = True  # flag
        return cls

    @classmethod
    def load(cls, file_: str):
        """
        Import another diary book from local file (which is encrypted). If the file does not exist, create one.
        :param file_: The encrypted file.
        :return: cls
        """
        if path.exists(cls.current_file.replace('.des', '')):
            remove(cls.current_file.replace('.des', ''))  # delete the previous unencrypted file

        if path.exists(file_):  # the file exists, then load it
            print('==== Import a Diary ====')
            if not cls.saved and input('Save the current file? <y/n> ') == 'y':
                if not cls.current_file:  # then create a new diary book
                    cls.current_file = input('Please name the current file (end in .txt.des): ')
                cls.save()  # save the current file
            cls.init()  # initiate the diaries list

            decrypt_file(file_, cls.__password, '********')  # decrypt the file
            with open(file=file_.replace('.des', ''), mode='r', encoding='utf-8') as f:
                while True:
                    tmp = f.readline().split('#t#')  # convert the line into a tuple
                    if len(tmp) == 1:  # end of the file, tmp == ['']
                        break
                    else:
                        cls.dates.append(tmp[0])
                        cls.diaries.append(Diary(text=eval(tmp[1]), date=tmp[0]))  # import a new page
            print('==== Diary Imported ====')
        else:  # the file does not exist, then create one
            cls.change_file(file_).save().init()  # save the current one and initiate the diaries list.
        cls.current_file = file_
        return cls

    @classmethod
    def set_password(cls):
        """
        Set the password of the diary book.
        :return: cls
        """
        cls.__password = input('New password: ')  # set new password
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


def main():
    """
    help the user to call different functions in the class 'Matter'
    :return: None
    """
    quit_flag = False

    def quit_():
        """
        End the program
        :return: None
        """
        nonlocal quit_flag
        if not Diary.saved and input('Not saved. Save? <y/n>') == 'y':  # save the file
            Diary.save()
        if path.exists(Diary.current_file.replace('.des', '')):
            remove(Diary.current_file.replace('.des', ''))  # delete the unencrypted file
        quit_flag = True  # flag
        return None

    def view_():
        """
        view the details of a page
        :return: None
        """
        print('==== View Details ====')
        if get_int('Choose mode:\n1. Select date\n2. Search keyword\n#: ', range_=(1, 2)) == 1:  # select mode
            Diary.content().view_page()  # ergodic all the pages
        else:
            keyword = input('Please input the keyword here: ')
            Diary.search(keyword).view_page()  # select those with specified keyword in it
        print('======================')
        return None

    def edit_():
        """
        Edit one page in your diary book.
        :return: None
        """
        Diary.content().edit_page()
        return None

    def sync_():
        """
        Synchronize the local book to the mailbox or in reverse.
        :return: None
        """
        print('==== Synchronize ====')
        Diary.save()  # save the file
        key = input('Please input your authorization code: ')  # login your email
        if get_int('Choose mode:\n1. Sync to the mailbox\n2. Sync from the mailbox\n#: ', range_=(1, 2)) == 1:
            send(key, Diary.current_file, note_='Diary_Sync')  # send the current file to your mailbox
        else:
            for each in receive(key, input('Specify date (yy-mm-dd-hh-mm): ')):
                if each.note == 'Diary_Sync' and each.name == Diary.current_file:  # is a diary file
                    each.update()  # save the file to local
                    print('---- Synchronized "%s" successfully ----' % each.name)
                    Diary.load(Diary.current_file)
                    break
        print('=====================')
        return None

    def import_():
        """
        Import another diary book from local.
        :return: None
        """
        Diary.load(input('Import your diary book: '))
        return None

    def recall_():
        """
        Recall your memories on certain topics
        :return: None
        """
        keywords = input('Please input the keywords of certain topic, use ", " to connect: ')
        Diary.recall([each.strip() for each in keywords.split(',')])
        return None

    funcs = [
        quit_, Diary.new_page, view_, Diary.del_page, edit_,
        Diary.save, sync_, import_, Diary.set_password, recall_]  # functions to execute later

    while True:
        print('=' * 50)

        print(
            'Choose a function from:\n'
            '1. Add a new page\n'
            '2. View a page\n'
            '3. Delete a page\n'
            '4. Edit a page\n'
            '5. Save the file\n'
            '6. Synchronize\n'
            '7. Import another book\n'
            '8. Set password\n'
            '9. Recall\n'
            '0. Quit')
        mode = get_int('#: ', range_=range(10))
        print('=' * 50)

        funcs[mode]()  # call the functions defined in line 296
        if quit_flag:  # quit the program
            return None


if __name__ == '__main__':
    Diary.set_password()
    Diary.load(input('Import your diary book: '))
    main()
    pass
