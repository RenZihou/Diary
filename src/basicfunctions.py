# -*- coding: utf-8 -*-
# @Author: RZH

""" This python file contains some basic functions that might be called by other files. """


def get_int(text: str, range_: [list, tuple] = None) -> int:
    """
    This function will convert the input to an integer and return.
    if the input is not an integer, ask the user to input again.
    :param text: a string, the text you want to print.
    :param range_: a list, the allowable range of the integer. if no other claim, then take the set of integers.
    :return: an integer.
    """
    while True:
        i = input(text)
        try:  # check whether the input can be convert to an integer.
            int(i)
        except ValueError:  # convert failed. back to the input function and restart.
            print('Please input an integer.')
        else:  # convert successfully. return as an integer.
            if range_ is None:  # no extra restrict on the integer, return directly.
                return int(i)
            else:  # has a restrict on the integer, decide if the input is satisfying the restrict.
                if not(int(i) in range_):  # restrict not met.
                    print('Please input again because your input is illegal.')
                else:  # restrict satisfied.
                    return int(i)


def timer(func: callable) -> callable:
    """
    use as a decorator, calculate the time taken by a running function.
    :param func: the function whose running time will be printed.
    :return: a function with a durance feedback.
    """
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)  # run the actual function
        end_time = time.time()
        durance = end_time - start_time
        print('The function "%s" took %f seconds.' % (func.__name__, durance))
        return result
    return wrapper


def print_list(li: [list, tuple]) -> None:
    """
    print the elements in a list line by line.
    :param li: the list you want to print.
    :return: None.
    """
    for each in li:
        if isinstance(each, dict):
            for key, value in each.items():
                print('{}: {}'.format(key, value))
        else:
            print(each)
    return None


def param_type_check_e(*ty: type, **argv: type) -> callable:
    """
    Use as a decorator, to check the parameters of a function. Raise exception when the check result is false
    :param ty: VAR_POSITIONAL
    :param argv: VAR_KEYWORD
    :return: a function with check result.
    """
    def check(t):  # t: type
        return lambda x: isinstance(x, t)  # the actual check function

    ty = map(check, ty)  # VAR_POSITIONAL
    argv = dict((i, check(argv[i])) for i in argv)  # VAR_KEYWORD

    def wrapper(func):
        def deal(*func_x, **func_y):
            if ty:  # not None
                x_list = [a for a in func_x]  # the parameters need to check
                for ty_check in ty:
                    if not ty_check(next(iter(x_list))):  # result is False
                        raise TypeError("Wrong type exists in parameters.")
            if argv:  # not None
                y_dict = dict((i, func_y[i]) for i in func_y)  # the parameters need to check
                for k in argv.keys():
                    if not argv[k](y_dict.get(k)):  # # argv[k] is a lambda function, result is False
                        raise TypeError("Wrong type exists in parameters.")
            return func(*func_x, **func_y)  # run the original function
        return deal
    return wrapper


def param_type_check_p(*ty: type, **argv: type) -> callable:
    """
    Use as a decorator, to check the parameters of a function. Print out the results.
    :param ty: VAR_POSITIONAL
    :param argv: VAR_KEYWORD
    :return: a function with check result.
    """
    def check(t):  # t: type
        return lambda x: isinstance(x, t)  # the actual check function

    ty = map(check, ty)  # VAR_POSITIONAL
    argv = dict((i, check(argv[i])) for i in argv)  # VAR_KEYWORD

    def wrapper(func):
        def deal(*func_x, **func_y):
            if ty:  # not None
                x_list = [a for a in func_x]  # the parameters need to check
                result = [ty_check(next(iter(x_list))) for ty_check in ty]
                print('position param check result: ', result)  # list
            if argv:  # not None
                y_dict = dict((i, func_y[i]) for i in func_y)  # the parameters need to check
                result = {}
                for k in argv.keys():
                    result[k] = argv[k](y_dict.get(k))  # argv[k] is a lambda function
                print('keyword param check result: ', result)  # dictionary
            return func(*func_x, **func_y)  # run the original function
        return deal
    return wrapper


if __name__ == '__main__':
    # li = [1, 2, 3]
    # print_list(li)
    pass
