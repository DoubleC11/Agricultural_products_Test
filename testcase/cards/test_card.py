import pytest
import allure
from utils.handle_data.yaml_handler import read_yaml, write_yaml
from utils.handle_data.configParse import ConfigParse
from utils.send_requests import Send_Requests
from utils.apiutils import RequesrsBase

conf = ConfigParse()
r = RequesrsBase()


@allure.feature('商品模块')
class TestCard:
    """
    获取商品
    """

    @pytest.mark.order(1)
    @pytest.mark.parametrize("baseInfo,test_case", read_yaml("./data/getCard.yaml"))
    def test_get_card(self, baseInfo,test_case, re_client):
        allure.dynamic.title(test_case['case_name'])
        re_client.excute_test_cases(baseInfo, test_case)

    """
    添加商品
    """

    @pytest.mark.order(2)
    @pytest.mark.parametrize("baseInfo,test_case", read_yaml("./data/addcard.yaml"))
    def test_add_card(self, baseInfo,test_case, re_client):
        allure.dynamic.title(test_case['case_name'])
        re_client.excute_test_cases(baseInfo, test_case)