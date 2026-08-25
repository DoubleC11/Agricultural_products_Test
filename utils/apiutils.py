import json
import re
from http.client import responses
from utils.handle_data.yaml_handler import read_yaml, write_yaml
from utils.debugtalk import DebugTalk
from utils.handle_data.configParse import ConfigParse
from utils.send_requests import Send_Requests
from utils.assertion_utils import AssertionUtils
import json
from jsonpath_ng.ext import parse


class RequesrsBase:

    def __init__(self):
        self.conf = ConfigParse()
        self.r = Send_Requests()
        self.assertion = AssertionUtils()

    def parse_and_replace_vaules(self, vaules):
        yml_data_str = vaules if isinstance(vaules, str) else json.dumps(vaules, ensure_ascii=False)
        # print("解析之前 ", yml_data_str)
        for _ in range(yml_data_str.count("${")):
            if "${" in yml_data_str and "}" in yml_data_str:
                start_index = yml_data_str.index("${")
                end_index = yml_data_str.index("}", start_index)
                func = yml_data_str[start_index:end_index + 1]
                # 使用正则表达式提取函数名和参数
                matchs = re.match(r'\$\{(\w+)\((.*?)\)\}', func)
                if matchs:
                    fun_name = matchs.group(1)
                    fun_value = matchs.group(2)
                    fun_value = fun_value.split(",") if fun_value else []
                    extract_data = getattr(DebugTalk(), fun_name)(*fun_value)
                    yml_data_str = re.sub(re.escape(func), str(extract_data), yml_data_str)
        try:
            datas = json.loads(yml_data_str)
        except json.JSONDecodeError:
            datas = yml_data_str

        return datas

    def excute_test_cases(self, api_info):
        """
         规范yaml接口信息  执行接口 提取结果以及断言操作
        :param api_info:   yaml的接口信息
        :return:
        """
        try:
            conf_host = self.conf.get_value("Host", "host")
            url = conf_host + api_info["baseInfo"]["url"]
            api_name = api_info["baseInfo"]["api_name"]
            method = api_info["baseInfo"]["method"]
            header = api_info["baseInfo"]["header"]
            for testcase in api_info["testCase"]:
                case_name = testcase.pop('case_name')
                validation = self.parse_and_replace_vaules(testcase.pop('validation'))
                extract = testcase.pop('extract', None)
                extract_lists = testcase.pop('extract_lists', None)
                for res_d, res_values in testcase.items():
                    if res_d in ['json', 'data', 'params']:
                        datas = self.parse_and_replace_vaules(res_values)
                        testcase[res_d] = datas
                responses = self.r.execute_api_request(api_name=api_name, method=method, url=url, header=header,
                                                       case_name=case_name, **testcase)
                res_status, res_text = responses.status_code, responses.text
                print(f"接口响应状态码 【{res_status}】")
                print(f"接口响应数据 {res_text}")
                if extract is not None:  # 提取数据
                    self.extract_data(extract, responses)
                if extract_lists is not None:
                    self.extract_data(extract_lists, responses)
                """
                断言
                validation 预期结果
                responses 响应数据 可以是response类型 也可以是dict类型
                res_status 状态码
                """
                self.assertion.assert_main(validation, responses, res_status)
        except Exception as e:
            print("出现未知异常!!! ", e)
            raise e

    def extract_data(self, extract, response_data):  # 提取响应数据
        try:
            for key, val in extract.items():
                if '$' in val: #jsonpath提取
                    expr = parse(val)
                    titles = [m.value for m in expr.find(response_data.json())]
                    if titles:
                        if len(titles) == 1:
                            write_yaml({key: titles[0]})
                        else:
                            write_yaml({key: titles})
                        print(f"成功提取数据【{key}】")
                    else:
                        print("未提取到数据")
        except json.decoder.JSONDecodeError:
            print("json解析错误 请检查yaml文件extract表达式是否正确")
        except Exception as e:
            print(f"出现错误：{e}")


if __name__ == "__main__":
    datas = read_yaml("../data/login.yaml")[0]
    r = RequesrsBase()
    data = r.parse_and_replace_vaules(datas)
    r.excute_test_cases(data)
