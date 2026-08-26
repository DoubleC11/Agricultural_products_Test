import allure
import pytest

from utils.handle_data.yaml_handler import read_yaml
from utils.handle_data.configParse import ConfigParse


conf = ConfigParse()


@allure.feature('订单模块')
class TestOrder:
    @pytest.mark.order(-1)
    @pytest.mark.parametrize("data", read_yaml("./data/order.yaml"))
    def test_create_order(self, data,re_client):
        allure.dynamic.title(data[1]['case_name'])
        re_client.excute_test_cases(data[0],data[1])

