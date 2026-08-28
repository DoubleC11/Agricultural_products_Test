import json
from utils.exception_utils.exception import AsserterError
from jsonpath_ng.ext import parse
from utils.db_connect.mysqlconnect import MysqlConnect
import allure


class AssertionUtils:
    def __init__(self):
        pass

    """ # 断言标识码 0 表示成功 其他表示失败
    状态码断言
    包含断言
    相等断言
    不相等断言
    数据库断言
    """

    @classmethod  # 状态码断言
    def statuscode_assert_equal(cls, expect_result, status_code) -> int:
        """
        :param expect_result:  yaml文件的code预期状态码
        :param status_code:  接口实际状态码
        :return:
        """
        failure_count = 0  # 断言标识码 0 表示成功 其他表示失败
        if expect_result == status_code:
            print(f"断言通过 接口实际返回状态码【{expect_result}】==【{status_code}】")
            allure.attach(f"断言通过 接口实际返回状态码【{expect_result}】==【{status_code}】", '状态码断言通过',
                          attachment_type=allure.attachment_type.TEXT)
        else:
            print(f"断言失败 接口实际返回状态码{expect_result}!={status_code}")
            allure.attach(f"断言失败 接口实际返回状态码【{expect_result}】!=【{status_code}】", '状态码断言失败',
                          attachment_type=allure.attachment_type.TEXT)
            failure_count += 1
        return failure_count

    @classmethod  # 包含断言
    def contain_assert(cls, expect_result, response_data) -> int:
        """
        :param expect_result: 预期结果 dict
        :param response_data:
        :return:
        """
        failure_count = 0  # 断言标识码 0 表示成功 其他表示失败
        response_data = response_data if isinstance(response_data, dict) else response_data.json()
        for assert_key, assert_value in expect_result.items():
            expr = parse(assert_key)
            titles = [m.value for m in expr.find(response_data)]
            assert_value = assert_value if isinstance(assert_value, str) else str(assert_value)
            if titles:
                response_str = ''.join(titles)
                if assert_value in response_str:
                    print(f"断言通过 预期结果【{assert_value}】包含在实际结果")
                    allure.attach(f"断言通过 预期结果【{assert_value}】包含在实际结果", "包含断言通过",
                                  attachment_type=allure.attachment_type.TEXT)

                else:
                    print(f"断言失败 预期结果【{assert_value}】不包含在实际结果】")
                    allure.attach(f"断言失败 预期结果【{assert_value}】不包含在实际结果】", '包含断言失败',
                                  attachment_type=allure.attachment_type.TEXT)

                    failure_count += 1
        return failure_count

    @classmethod  # 相等断言
    def eq_assert_equal(self, expect_result, response) -> int:
        failure_count = 0  # 断言标识码 0 表示成功 其他表示失败
        response = response if isinstance(response, dict) else response.json()
        if isinstance(expect_result, dict):
            common_key = expect_result.keys() & response.keys()
            if common_key:
                common_key = list(common_key)[0]
                new_response_data = {common_key: response[common_key]}
                if expect_result == new_response_data:
                    print(f"断言通过 预期结果【{expect_result}】等于 实际结果【{new_response_data}】")
                    allure.attach(f"断言通过 预期结果【{expect_result}】等于 实际结果【{new_response_data}】",
                                  '相等断言通过',
                                  attachment_type=allure.attachment_type.TEXT)

                else:
                    print(f"断言失败 预期结果【{expect_result}】不等于 实际结果【{new_response_data}】")
                    allure.attach(f"断言失败 预期结果【{expect_result}】不等于 实际结果【{new_response_data}】",
                                  '相等断言失败',
                                  attachment_type=allure.attachment_type.TEXT)

                    failure_count += 1
            else:
                print("请检查eq是否存在")
                failure_count += 1
        else:
            print("请确保是字典格式")
            failure_count += 1
        return failure_count

    @classmethod  # 不相等断言
    def ne_assert_equal(self, expect_result, response) -> int:
        failure_count = 0  # 断言标识码 0 表示成功 其他表示失败
        response = response if isinstance(response, dict) else response.json()
        if isinstance(expect_result, dict):
            common_key = expect_result.keys() & response.keys()
            if common_key:
                common_key = list(common_key)[0]
                new_response_data = {common_key: response[common_key]}
                if expect_result != new_response_data:
                    print(f"断言通过 预期结果【{expect_result}】不等于 实际结果【{new_response_data}】")
                    allure.attach(f"断言通过 预期结果【{expect_result}】不等于 实际结果【{new_response_data}】",
                                  '不相等断言通过',
                                  attachment_type=allure.attachment_type.TEXT)

                else:
                    print(f"断言失败 预期结果【{expect_result}】等于 实际结果【{new_response_data}】")
                    allure.attach(f"断言失败 预期结果【{expect_result}】等于 实际结果【{new_response_data}】",
                                  '不相等断言失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
            else:
                print("请检查eq是否存在")
                failure_count += 1
        else:
            print("请确保是字典格式")
            failure_count += 1
        return failure_count

    @classmethod  # 数据库断言
    def database_assert(self, expect_result, status_code=None) -> int:
        """
        :param expect_result: sql语句
        :param status_code: 状态码不填
        :return:
        """
        failure_count = 0

        conn = MysqlConnect()
        db_data = conn.query(expect_result)

        if db_data:
            allure.attach(f"断言通过 查询结果存在",
                          '数据库断言通过',
                          attachment_type=allure.attachment_type.TEXT)
            print('数据库断言通过')

        else:
            print('数据库断言失败 请检查数据库是否存在该数据')
            allure.attach(f"断言失败 查询结果不存在",
                          '数据库断言失败',
                          attachment_type=allure.attachment_type.TEXT)
            failure_count += 1
        return failure_count

    def assert_main(self, expect_result, response_data, status_code):
        failure_count = 0
        assert_methods = {
            'code': self.statuscode_assert_equal,
            'contain': self.contain_assert,
            'eq': self.eq_assert_equal,
            'ne': self.ne_assert_equal,
            'db': self.database_assert
        }
        for assert_extract in expect_result:
            for key, value in assert_extract.items():
                methods = assert_methods.get(key)
                if methods:
                    if key == 'code':
                        results = methods(value, status_code)
                    elif key == 'contain':
                        results = methods(value, response_data)
                    elif key == 'eq':
                        results = methods(value, response_data)
                    elif key == 'ne':
                        results = methods(value, response_data)
                    elif key == 'db':
                        results = methods(value, status_code)
                    else:
                        results = 0
                    failure_count += results
                else:
                    # print(f"不支持当前断言模式{methods} ")
                    raise AsserterError(f"不支持当前断言模式{key}!!!")

        assert failure_count == 0, "测试失败"
        print("-" * 30 + "断言通过" + "-" * 30)
