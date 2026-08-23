import pytest

from utils.handle_data.yaml_handler import read_yaml, write_yaml
from utils.handle_data.configParse import ConfigParse
from utils.send_requests import Send_Requests
from utils.apiutils import RequesrsBase

conf = ConfigParse()
r = RequesrsBase()


class TestCard:
    """
    获取商品
    """
    @pytest.mark.parametrize("data", read_yaml("./data/getCard.yaml"))
    def test_get_card(self, data, re_client):
        re_client.excute_test_cases(data)

    """
    添加商品
    """
    @pytest.mark.parametrize("data", read_yaml("./data/addcard.yaml"))
    def test_add_card(self, data, re_client):
        re_client.excute_test_cases(data)
