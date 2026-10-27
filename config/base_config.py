import os
import sys

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

File_PATH={
    'extract':os.path.join(DIR_PATH,'extract.yaml'),
    'ini':os.path.join(DIR_PATH,'config','config.ini'),
    'log':os.path.join(DIR_PATH,'logs'),
}

is_dingding=False #是否推送钉钉 默认False
is_all=False #是否全部推送
DINGTALK_WEBHOOK = ""
DINGTALK_SECRET = ""
