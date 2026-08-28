import json
from collections import Counter
import pytest
import requests
from utils.send_requests import Send_Requests
from utils.handle_data.yaml_handler import remove_yaml
from utils.apiutils import RequesrsBase
import time

@pytest.fixture(autouse=True, scope='session')
def re_client():
    r = RequesrsBase()
    yield r


@pytest.fixture(autouse=True, scope='session')
def clear_extreact_yaml():
    print("-" * 10 + "清理数据" + "-" * 10)
    remove_yaml()


@pytest.fixture(autouse=True)
def print_Info():
    print("-" * 10 + "开始测试" + "-" * 10)
    yield
    print("-" * 10 + "测试结束" + "-" * 10)




# 全局变量，用于在会话开始时记录数据
_session_start_time = None
_collected_count = 0

def pytest_sessionstart(session):
    """会话开始时记录开始时间和收集到的用例总数"""
    global _session_start_time, _collected_count
    _session_start_time = time.monotonic()
    # session.items 包含了所有收集到的测试用例（Item 对象）
    _collected_count = len(session.items)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """自定义测试结果汇总输出"""
    global _session_start_time, _collected_count

    # 1. 从 terminalreporter.stats 获取各状态报告列表，统计数量
    stats = terminalreporter.stats
    passed = len(stats.get('passed', []))
    failed = len(stats.get('failed', []))
    error = len(stats.get('error', []))
    skipped = len(stats.get('skipped', []))
    # （可选）如果需要 xfailed/xpassed 等，可以继续添加

    # 2. 执行用例数（您的定义：通过+失败+报错，不含跳过）
    executed = passed + failed + error

    # 3. 收集的用例总数（来自 sessionstart 记录）
    collected = _collected_count

    # 4. 总用时（来自 sessionstart 记录的开始时间）
    duration = time.monotonic() - _session_start_time if _session_start_time else 0.0

    # 5. 计算成功率
    rate = (passed / executed * 100) if executed else 0.0

    # 6. 输出结果（保持您原来的格式）
    terminalreporter.write_sep("-", "用例统计")
    terminalreporter.write_line(f"收集用例: {collected}")
    terminalreporter.write_line(f"执行用例: {executed}")
    terminalreporter.write_line(f"通过: {passed}  失败: {failed}  报错: {error}  跳过: {skipped}")
    terminalreporter.write_line(f"成功率: {rate:.2f}%")
    terminalreporter.write_line(f"总用时: {duration:.2f} 秒")
