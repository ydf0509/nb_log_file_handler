

import multiprocessing
import logging
import time
from nb_log_file_handler import NbLogFileHandler

logger = logging.getLogger('hello')

fh = NbLogFileHandler(file_name='xx3.log',log_path='./',max_bytes=1000*1000,back_count=3)

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