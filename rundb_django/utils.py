'''
Created on Apr 22, 2010

@author: mazurov
'''

def bit_count(int_type):
    count = 0
    while(int_type):
        int_type &= int_type - 1
        count += 1
    return(count)
