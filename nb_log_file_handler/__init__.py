import typing
import logging
from .rotate_file_writter import OsFileWritter


class BothDayAndSizeRotatingFileHandler(logging.Handler):
    """
    自己从头开发的按照时间和大小切割
    """

    def __init__(self, file_name: typing.Optional[str], log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000,
                 back_count=10):
        super().__init__()
        self.os_file_writter = OsFileWritter(file_name=file_name, log_path=log_path, max_bytes=max_bytes,
                                             back_count=back_count)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.os_file_writter.write_2_file(msg + '\n')


NbLogFileHandler = BothDayAndSizeRotatingFileHandler