import configparser
from config.base_config import File_PATH


class ConfigParse:
    """
    解析ini文件配置
    """
    def __init__(self, file_name=File_PATH['ini']):
        self.config = configparser.ConfigParser()
        self.file_path = file_name
        self.read_config()

    def read_config(self):
        self.config.read(self.file_path)

    def get_value(self, section, option):
        try:
            return self.config[section][option]
        except Exception as e:
            print(f"解析异常，{e}")


if __name__ == '__main__':
    config = ConfigParse()
    print(config.get_value('Mysql', 'host'))
    