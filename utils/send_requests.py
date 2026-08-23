from asyncio import timeout

import requests
from utils.handle_data.yaml_handler import read_yaml,write_yaml

class Send_Requests:
    def __init__(self):
        self.client = requests.Session()
        self.response = None

    def __send_request(self, **kwargs):
        try:
            self.response = self.client.request(**kwargs)
        except requests.exceptions.ConnectionError:
            print("Connection Error 连接失败！！！")
        except requests.exceptions.Timeout:
            print("Timeout Error 连接超时！！！")
        except requests.exceptions.RequestException:
            print("Request Error 请求错误！！！")
        return self.response

    def execute_api_request(self, api_name, url, method, header, case_name, cookie=None, file=None, **kwargs):
        """
        :param api_name:
        :param url:
        :param method:
        :param header:
        :param case_name:
        :param cookie:
        :param file:
        :param kwargs:
        :return:
        """
        res = self.__send_request(url=url, method=method, headers=header, cookies=cookie, files=file, timeout=10,
                                verify=False, **kwargs)

        return res


if __name__ == "__main__":
    send_request = Send_Requests()
    data=read_yaml('./../data/login.yaml')[0]
    api_name=data["baseInfo"]["api_name"]
    url="http://127.0.0.1:8080"+data['baseInfo']["url"]
    method=data['baseInfo']["method"]
    header=data['baseInfo']["header"]
    json_d=data['testCase'][0]["data"]
    case_name=data['testCase'][0]["case_name"]
    r = send_request.execute_api_request(api_name=api_name,url=url,method=method,header=header,json=json_d,case_name=case_name)
    print(r.text)
    r=r.json()
    write_yaml({"token":r["data"]["token"]})
