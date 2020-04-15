'''
Testing multithreading
'''
import random
import time
import processify


@processify
def task_to_do(i=0):
    '''
    Sleeps for a random number of seconds then prints output
    '''
    time.sleep(random.randrange(2, 10))
    if i % 4 == 0:
        raise Exception("Failed to do the thing")
    print('Done')


for t in range(4):
    task_to_do(t)
