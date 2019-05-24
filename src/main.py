# -*- coding: utf-8 -*-
# @Author: RZH

"""
define the main function of project 'Diary'
"""

from os import listdir
from os.path import exists
from configparser import ConfigParser  # read and write ini files
from src.diary import Diary
from src.basicfunctions import get_int
from src.send_email import send
from src.receive_email import receive
from plugin.input_pwd import input_pwd as in_pwd


def main():
    """
    help the user to call different functions in the class 'Diary'
    :return: None
    """
    quit_flag = False
    config = ConfigParser()

    def input_pwd(s, len_=0):
        if hide_pwd:
            return in_pwd(s=s, len_=len_)
        else:
            return input(s)

    def quit_():
        """
        End the program
        :return: None
        """
        nonlocal quit_flag, config

        if not Diary.saved and input('Not saved. Save? <y/n>') == 'y':  # save the file
            Diary.save()

        config['DEFAULT']['diary_book'] = Diary.current_file
        config['DEFAULT']['hide_pwd'] = str(hide_pwd)
        with open('files/config.ini', 'w') as cf:
            config.write(cf)  # write the configuration file, including the default diary book.

        quit_flag = True  # flag
        return None

    def view_():
        """
        view the details of a page
        :return: None
        """
        print('==== View Details ====')
        if Diary.num_of_pages() == 0:
            print('You have no diaries now.')
            return None
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
        key = input_pwd('Please input your authorization code: ')  # login your email
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
        _ = 1
        diaries = []
        for each in listdir('files'):
            if each[-3:] == '.dr':  # is diary file
                print('%d: %s' % (_, each))
                diaries.append(each)
                _ += 1

        index = get_int('Import (input the #, if you want to create a new one, input 0): ', range_=range(_+1))
        if index == 0:  # create a new book
            filename = 'files/' + input('Name your new diary book (.dr): ')
            Diary.change_file(filename).set_password(input_pwd('New password: ', len_=8)).init()
        else:  # import the selected one
            new_password = input_pwd('Password for %s: ' % diaries[index-1], len_=8)
            Diary.load('files/' + diaries[index-1], password_=new_password)
        return None

    def recall_():
        """
        Recall your memories on certain topics
        :return: None
        """
        keywords = input('Please input the keywords of certain topic, use ", " to connect: ')
        Diary.recall([each.strip() for each in keywords.split(',')])
        return None

    def settings_():
        """
        Settings for the diary book.
        Including:
        * whether hide the password while typing it.
        :return: None
        """
        nonlocal hide_pwd
        index = get_int(
            'Settings:\n'
            '1. Password typing\n'
            '0. Quit\n'
            '#: ', range_=(0, 1)
        )
        if index == 1:
            hide_pwd = True if get_int('Whether hide password while typing (0 or 1): ', range_=(0, 1)) else False
        return None

    funcs = [
        quit_, Diary.new_page, view_, Diary.del_page, edit_,
        Diary.save, sync_, import_, Diary.set_password, recall_, settings_]  # functions to execute later

    if exists('files/config.ini'):
        config.read('files/config.ini')
        file = config['DEFAULT']['diary_book']
        hide_pwd = eval(config['DEFAULT']['hide_pwd'])
        Diary.load(
            file_=file,
            password_=input_pwd('Password for %s: ' % file.replace('files/', '').replace('.dr', ''), len_=8))
    else:
        import_()

    while True:
        print('=' * 50)

        print(
            'Current diary book: %s\n'
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
            '10. Settings\n'
            '0. Quit' % Diary.current_file.replace('files/', '').replace('.dr', ''))
        mode = get_int('#: ', range_=range(11))
        print('=' * 50)

        funcs[mode]()  # call the functions defined in line 144
        if quit_flag:  # quit the program
            return None


if __name__ == '__main__':
    main()
