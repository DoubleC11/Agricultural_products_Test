import pytest
from utils.handle_data.yaml_handler import read_yaml


class TestDemo1:
    @pytest.mark.api
    def test_demo1(self):
        # r=auto_login.json()
        print("测试demo1")

    @pytest.mark.parametrize("data", [("admin", "123"), ("cc", "1"), ("aa", "908")])
    def test_demo2(self, data):
        # r=auto_login.json()
        assert len(data[1]) > 0

    n = 9

    # @pytest.mark.api
    @pytest.mark.skipif(n != 9, reason="不符合条件")
    def test_demo3(self):
        # r=auto_login.json()
        print("测试demo3")

    # @pytest.mark.parametrize("data", read_yaml("../data/login.yaml"))
    def test_demo4(self):
        print("测试4")


if __name__ == "__main__":
    a = read_yaml("data/login.yaml")
    for x in a:
        print(x)
