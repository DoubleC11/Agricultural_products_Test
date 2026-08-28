import allure
import pytest

from utils.handle_data.yaml_handler import read_yaml
from utils.handle_data.configParse import ConfigParse

conf = ConfigParse()


@allure.feature('下单业务模块')
class TestforwardProcess:
    @pytest.mark.order(-1)
    @pytest.mark.parametrize("data", read_yaml("./data/ProductOrderingProcess/ProductOrderingProcess.yaml"))
    def test_forward_process(self, data, re_client):
        baseInfo=data["baseInfo"]
        testCase=data["testCase"][0]
        allure.dynamic.title(testCase['case_name'])
        re_client.excute_test_cases(baseInfo,testCase )
