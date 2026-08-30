# import logging
# import os
# import sys
# import time
# from logging.handlers import RotatingFileHandler
# from config.base_config import File_PATH
#
# logs_path = File_PATH['log']
# if not os.path.exists(logs_path):  # 文件不存在就创建
#     os.mkdir(logs_path)
#
# log_file_name = logs_path + r'/test.{}.log'.format(time.strftime('%Y%m%d', time.localtime()))
#
#
#
# class HandlerLogs:
#     @classmethod
#     def output_logs(cls):
#         logger = logging.getLogger(__name__)
#         #防止重复打印日志
#         if not logger.handlers:
#             logger.setLevel(logging.DEBUG)
#
#             #日志格式
#             logging_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#             #把日志信息输出到控制台
#             sh=logging.StreamHandler()
#             sh.setLevel(logging.DEBUG)
#             sh.setFormatter(logging_format)
#             logger.addHandler(sh)
#
#             #把日志输出到文件
#             fh=RotatingFileHandler(filename=log_file_name,mode='a',maxBytes=1024*1024*100,backupCount=1,encoding='utf-8')
#             fh.setLevel(logging.DEBUG)
#             fh.setFormatter(logging_format)
#             logger.addHandler(fh)
#
#         return logger
#
# h=HandlerLogs.output_logs()
# if __name__ == '__main__':
#     r=HandlerLogs()
#     logger = r.output_logs()
#     logger.info('this is info')
#     logger.error('this is info')
#     logger.critical('this is critical')
#     logger.debug('this is debug')
#     logger.warning('this is warning')
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
from config.base_config import File_PATH

logs_path = File_PATH['log']
if not os.path.exists(logs_path):
    os.mkdir(logs_path)
log_file_name = logs_path + r'/test.{}.log'.format(time.strftime('%Y%m%d', time.localtime()))

# 自定义颜色格式器（ANSI 转义序列）
class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: green + "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s" + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class HandlerLogs:
    @classmethod
    def output_logs(cls):
        logger = logging.getLogger(__name__)  # 修正为 __name__
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            # 文件格式（无颜色）
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s')

            # 控制台格式（带颜色）
            console_formatter = ColorFormatter()

            # 控制台 Handler
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(console_formatter)
            logger.addHandler(sh)

            # 文件 Handler（轮转）
            fh = RotatingFileHandler(filename=log_file_name, mode='a',
                                     maxBytes=1024*1024*100, backupCount=1, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(file_formatter)
            logger.addHandler(fh)

        return logger
h=HandlerLogs.output_logs()


