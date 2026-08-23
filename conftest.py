import json

import pytest
import requests
from utils.send_requests import Send_Requests
from utils.handle_data.yaml_handler import remove_yaml
from utils.apiutils import RequesrsBase

@pytest.fixture(autouse=True, scope='session')
def re_client():
    r = RequesrsBase()
    yield r


@pytest.fixture(autouse=True, scope='session')
def clear_extreact_yaml():
    print("-" * 10 + "清理数据" + "-" * 10)
    remove_yaml()


@pytest.fixture(autouse=True)
def print_Info():
    print("-" * 10 + "开始测试" + "-" * 10)
    yield
    print("-" * 10 + "测试结束" + "-" * 10)
