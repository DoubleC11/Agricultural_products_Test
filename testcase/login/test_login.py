import pytest

from utils.handle_data.yaml_handler import read_yaml, write_yaml
from utils.handle_data.configParse import ConfigParse
from utils.send_requests import Send_Requests
from utils.apiutils import RequesrsBase

conf = ConfigParse()



class TestLogin:
    @pytest.mark.order(1)
    @pytest.mark.parametrize("data", read_yaml("./data/login.yaml"))
    def test_login_demo1(self, data,re_client):
        re_client.excute_test_cases(data)

