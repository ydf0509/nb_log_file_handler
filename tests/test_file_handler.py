

import multiprocessing
import logging
import time

logger = logging.getLogger('hello')

fh = logging.FileHandler('xx1.log')

logger.addHandler(fh)
# logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



def f():
    for i in range(10000):
        logger.info(f'{i}aaaaa'*20)

if __name__ == '__main__':
    t1 = time.time()
    ps = []
    for  j in range(10):
        p = multiprocessing.Process(target=f)
        ps.append(p)
        p.start()
    for p in ps:
        p.join()
    print(time.time()-t1)