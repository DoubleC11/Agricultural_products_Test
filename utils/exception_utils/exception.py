class AsserterError(Exception):

    """
    文件断言异常
    """
    def __init__(self, message="不支持当前模式"):
        super().__init__(message)