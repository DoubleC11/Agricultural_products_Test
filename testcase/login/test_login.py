import allure
import pytest

from utils.handle_data.yaml_handler import read_yaml, write_yaml
from utils.handle_data.configParse import ConfigParse
from utils.send_requests import Send_Requests
from utils.apiutils import RequesrsBase

conf = ConfigParse()


@allure.feature('登陆模块')
class TestLogin:
    @pytest.mark.order(0)
    @allure.issue(url="https:baidu.com")
    @pytest.mark.parametrize("data", read_yaml("./data/login.yaml"))
    def test_login(self, data,re_client):
        allure.dynamic.title(data[1]['case_name'])

        re_client.excute_test_cases(data[0], data[1])
