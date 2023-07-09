# nb_log_file_handler

multi process safe log file handler,both time and size rotate，benchmark fast than concurrent_log_handler 100 times


nb_log_file_handler 是多进程安全切割，同时按时间和大小切割的FileHandler


## 安装

pip install nb_log_file_handler

## 1、nb_log_file_handler使用方式：

代码如下，和filehandler用法相同，导入 NbLogFileHandler

```python
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
```


## 2、各种按文件/时间大小切割的fileHander对比，

为了测试多进程按文件大小切割安全的复现，所以所有maxBytes按照1000*1000字节，即1M进行切割。


### 2.1、对比logging内置的 logging.handlers.RotatingFileHandler

logging.handlers.RotatingFileHandler 多进程按大小切割完全不可行，切割时候疯狂报错

```python

import multiprocessing
import logging.handlers
import time

logger = logging.getLogger('hello')

fh = logging.handlers.RotatingFileHandler('xx4.log',maxBytes=1000*1000,backupCount=3)

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
```

这个代码使用 文件handler选择原生自带的 logging.handlers.RotatingFileHandler
会疯狂报错，因为进程a在达到大小切割改名日志文件时候，进程b并不知情，报错如下：
```
PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。: 'D:\\codes\\nb_log_file_handler\\tests_nb_log_file_handler\\xx4.log' -> 'D:\\codes\\nb_log_file_handler\\tests_nb_log_file_handler\\xx4.log.1'
```

所以一般多进程写入同一个日志文件，并支持切割，那么久不能使用logging自带的RotatingFileHandler，要使用第三方包的filehandler。

### 2.2、对比小有名气的多进程切割安全的三方包 concurrent_log_handler

from concurrent_log_handler import ConcurrentRotatingFileHandler

```python


import multiprocessing
import logging
import time
from concurrent_log_handler import ConcurrentRotatingFileHandler

logger = logging.getLogger('hello')

fh = ConcurrentRotatingFileHandler('xx2.log',maxBytes=1000*1000,backupCount=3)

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
```

concurrent_log_handler这个包在windows上性能无法忍受，10进程写入10000次需要263秒，性能惨不忍睹。这个包在linux上性能还可以接受。

### 2.3、 nb_log_file_handler.NbLogFileHandler 按时间和大小多进程安全切割，性能远远的暴击 concurrent_log_handler

```python


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
```

nb_log_file_handler.NbLogFileHandler 10进程写入10000次只需要1.3秒，nb_log_file_handler 性能远远的暴击三方包 concurrent_log_handler