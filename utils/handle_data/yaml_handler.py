import os
import random

import yaml
import config.base_config as config

file_path = config.File_PATH["extract"]


def read_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("文件未找到")
    except Exception as e:
        print(f"出现其他问题 {e}")


def write_yaml(value):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass  # 文件没有存在就创建
    try:
        with open(file=file_path, mode="a", encoding="utf-8") as f:
            if isinstance(value, dict):
                f.write(yaml.dump(value, allow_unicode=True))
            else:
                print("数据需要字典格式！！！")
    except Exception as e:
        print('写入出现问题 ', e)


def remove_yaml():
    with open(file_path, "w", encoding="utf-8") as f:
        f.truncate() #清空数据


def read_extract_yaml(node_name, syb_node_name=None):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
            if syb_node_name is None:
                return yaml_data.get(node_name, None)
            else:
                return yaml_data.get(node_name, {}).get(syb_node_name, {})
    except Exception as e:
        print(f"出现错误 原因{e}")


if __name__ == "__main__":
    a = read_yaml("../../data/login.yaml")
    for x in a:
         print(x)
    # # print(write_yaml({'cb': 123}))
    # # remove_yaml()
    # a=read_extract_yaml("foods")
    # print(a)
    # # print(random.choice(a))
    # # print(read_extract_yaml("foods"),type(read_extract_yaml("foods")))
