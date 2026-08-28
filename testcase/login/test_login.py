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
    @pytest.mark.parametrize("baseInfo,test_case", read_yaml("./data/login.yaml"))
    def test_login(self, baseInfo, test_case, re_client):
        allure.dynamic.title(test_case['case_name'])
        re_client.excute_test_cases(baseInfo, test_case)
