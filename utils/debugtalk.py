import random

from utils.handle_data.yaml_handler import read_extract_yaml


class DebugTalk:
    def __init__(self):
        pass

    def is_string_int(self, s):
        try:
            int(s)
            return True
        except (ValueError, TypeError):
            return False

    def get_extract_data(self, node_name, out_format=None):
        """首先判断out_format是否为空
        当为str类型 获取下级的值
        为数字类型
        0:随机读取
        -1:读取全部 返回字符串
        -2：读取全部 返回列表
        其他值就正常读取
        """
        if out_format is None:
            return read_extract_yaml(node_name)
        if self.is_string_int(out_format):
            try:
                data = read_extract_yaml(node_name)
                dict_data = {
                    0: random.choice(data),
                    -1: ",".join([str(_) for _ in data]),
                    -2: data
                }
                if out_format in dict_data:
                    return dict_data[out_format]
                if out_format >= len(data) + 1:
                    return None
                return data[out_format - 1]
            except Exception as e:
                print("出现报错了 ",e)
        else:
            return read_extract_yaml(node_name, out_format)


if __name__ == '__main__':
    d = DebugTalk()
    data=d.get_extract_data("token")
    print(data) 
    # print(data,type(data))
    # print(d.is_string_int("foods"))
