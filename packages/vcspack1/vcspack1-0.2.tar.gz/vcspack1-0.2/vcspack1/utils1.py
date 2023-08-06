'''
This module has utilities1 for the arithmetic functions.
The parameters are of variable length.
'''

__author__ = 'vinay'
__version__ = "alpha_1"


def myvsum(*args):
    '''
    function which takes in variable count of numbers
    and returns their sum
    '''
    s = 0
    for n in args:
        s = s + n
    return s     
    
def myvproduct(*args):
    '''
    function which takes in variable count of numbers
    and returns their product
    '''
    p = 1
    for n in args:
        p = p * n
    return p

if __name__  == '__main__':
    s = myvsum(1,2,3,4,5,6,7)
    print(s)
    p = myvproduct(1,2,3,4,5,6,7)
    print(p)