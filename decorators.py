import os


def log_message(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        path = r"tmp/decorator_logs.txt"
        result = func(*args, **kwargs)
        with open(path, mode='a') as file:
            file.write(result)
        return result

    return wrapper


@log_message
def a_function_that_returns_a_string():
    return "A string"


@log_message
def a_function_that_returns_a_string_with_newline(s):
    return "{}\n".format(s)


@log_message
def a_function_that_returns_another_string(string=""):
    return "Another string"


a_function_that_returns_a_string()

a_function_that_returns_a_string_with_newline('hello')

a_function_that_returns_another_string('hi')
