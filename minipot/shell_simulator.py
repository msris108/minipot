import os
import random


def get_random_string(length):
    letters = ['1', 'F', '0x', '2', 'b', '^', '$', 'a', 'c', 'e', '%', ';', '/bin']
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def run(cmd):
    my_cmd = os.popen(cmd).read()
    return my_cmd[:len(cmd)//2] + get_random_string(random.randint(5, 25))

