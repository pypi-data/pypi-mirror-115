#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2017 "Allotey Immanuel Adotey"<imma.adt@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.


from logging import Logger, FileHandler, StreamHandler
import logging
import inspect
import time


MAX_LOG_FILES = 15
def purge_file(fn):
    with open(fn, 'w+'):
        pass

formatter = logging.Formatter('[%(asctime)s] p%(process)s %(levelname)s %(message)s','%m-%d %H:%M:%S')
file_logger = Logger(__name__)
file_logger.setLevel(logging.DEBUG)
time_start = time.time()
"""
{str(time_start)[-4:-1:]}
"""
# file_name = f'logs/logfile.txt'
# purge_file(file_name)
# file_handler = FileHandler(file_name)
# file_handler.setFormatter(formatter)
# file_logger.addHandler(file_handler)

stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
file_logger.addHandler(stream_handler)




def directLog(*args, level='D'):
    msg = '    '.join([str(i) for i in args])
    frame = inspect.currentframe()
    frame_info = inspect.getframeinfo(frame.f_back)
    pathname = frame_info.filename
    lineno = frame_info.lineno
    msg = f'{pathname}:{lineno} - '+msg
    if level == 'I':
        file_logger.info(msg)
    elif level == 'W':
        file_logger.warn(msg)
    elif level == 'E':
        file_logger.error(msg)
    elif level == 'C':
        file_logger.critical(msg)
    else:
        file_logger.debug(msg)

# directLog('Purging file: ', str(file_name))
# directLog("Log file created at :", f'"{file_name}"')

if __name__ == '__main__':
    directLog("Running main logger file.")
    directLog('Log end.')