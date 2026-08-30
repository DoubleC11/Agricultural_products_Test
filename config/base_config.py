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
DINGTALK_WEBHOOK = "4ab1fddffdf947bc6fe632ee1988c618d84b53246cb8484e8852a906c3565791"
DINGTALK_SECRET = "SEC1d9ab9542807e9b0feb45a42fac2ffddde105393e534b6ea10e13bdf977a7df2"