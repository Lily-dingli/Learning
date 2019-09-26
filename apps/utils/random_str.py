#-*-coding:utf-8-*-
import string
from random import choice
def generate_random(random_length,type):
    '''
    随机字符串生成函数
    :param random_length:
    :param type:
    :return:
    '''
    if type==0:
        random_seed=string.digits
    elif type==1:
        random_seed=string.digits+string.ascii_letters
    elif type==2:
        random_seed=string.digits+string.ascii_letters+string.punctuation
    random_str=[]
    while (len(random_str)<random_length):
        random_str.append(choice(random_seed))
    return ''.join(random_str)
if __name__ == '__main__':
    print(generate_random(4,1))