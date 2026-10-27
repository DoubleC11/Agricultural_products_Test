# 农产品信息管理系统接口自动化测试

这是一个基于 `pytest + requests + Allure + PyMySQL` 的接口自动化测试项目。测试数据主要使用 YAML 管理，覆盖用户登录、购物车、订单和完整下单流程，并支持响应数据提取、接口断言、数据库断言以及可选的钉钉通知。

## 功能特性

- 使用 YAML 分离接口信息、测试数据和预期结果。
- 使用 `pytest.mark.parametrize` 驱动数据，减少重复测试代码。
- 支持从接口响应中提取 token、用户 ID、订单 ID 等变量，并在后续请求中复用。
- 支持状态码、包含、相等、不相等和数据库结果断言。
- 支持按业务顺序执行登录、加购、下单、支付等串联场景。
- 使用 Allure 生成可视化测试报告。
- 支持初始化日志和可选的钉钉群机器人通知。

## 技术栈

| 技术 | 用途 |
| --- | --- |
| Python 3.10+ | 项目运行环境 |
| pytest | 测试执行与参数化 |
| pytest-order | 控制测试执行顺序 |
| requests | HTTP 接口请求 |
| PyYAML | 读取 YAML 测试数据 |
| jsonpath-ng | 提取和校验 JSON 响应字段 |
| Allure Pytest | 生成 Allure 测试结果 |
| PyMySQL | 数据库结果校验 |

## 项目结构

```text
.
├── config/
│   ├── base_config.py          # 项目路径与通知开关
│   └── config.ini              # 服务地址和 MySQL 连接配置
├── data/
│   ├── login.yaml              # 登录用例
│   ├── addcard.yaml            # 添加购物车用例
│   ├── getCard.yaml            # 查询购物车用例
│   ├── order.yaml              # 订单用例
│   └── ProductOrderingProcess/
│       └── ProductOrderingProcess.yaml
├── testcase/
│   ├── login/                  # 登录模块
│   ├── cards/                  # 购物车/商品模块
│   ├── order/                  # 订单模块
│   └── Process/                # 下单业务流
├── utils/
│   ├── apiutils.py             # YAML 用例解析与执行
│   ├── assertion_utils.py      # 断言工具
│   ├── send_requests.py        # HTTP 请求封装
│   ├── db_connect/             # MySQL 连接工具
│   ├── handle_data/            # YAML 与配置解析
│   └── logger_utils/           # 日志工具
├── conftest.py                 # pytest 全局 fixture 与会话统计
├── run.py                      # 执行测试并打开 Allure 报告
├── pytest.ini                  # pytest 与 Allure 配置
└── requirements.txt            # Python 依赖
```

## 测试范围

| 测试模块 | 测试内容 | 数据文件 |
| --- | --- | --- |
| 用户登录 | 正常登录、错误密码、用户不存在 | `data/login.yaml` |
| 购物车 | 查询购物车、添加商品 | `data/getCard.yaml`、`data/addcard.yaml` |
| 订单 | 正常下单、非法用户下单 | `data/order.yaml` |
| 下单业务流 | 登录、加购、下单、支付的串联流程 | `data/ProductOrderingProcess/ProductOrderingProcess.yaml` |

## 快速开始

### 1. 准备环境

建议使用 Python 3.10 或更高版本，并在项目根目录创建虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows 用户激活虚拟环境时使用：

```powershell
.venv\Scripts\activate
```

### 2. 配置测试环境

编辑 `config/config.ini`，填入待测服务与 MySQL 信息：

```ini
[Host]
host=http://127.0.0.1:8080

[Mysql]
host=127.0.0.1
port=3306
user=your_mysql_user
password=your_mysql_password
database=your_database
```

`Host.host` 应为完整的协议、域名/IP 和端口，不要以 `/` 结尾。接口路径由 YAML 中的 `baseInfo.url` 提供。

执行测试前，还需要确保：

- 农产品信息管理系统后端已经启动，并且可以通过 `Host.host` 访问。
- 测试账号、商品和购物车数据已经准备完成。
- 如果用例包含 `db` 断言，MySQL 服务可连接且账号具有查询权限。

### 3. 执行测试

运行全部测试：

```bash
pytest
```

也可以使用项目入口：

```bash
python run.py
```

`python run.py` 会执行测试、复制 `environment.xml` 到 Allure 结果目录，并调用 `allure serve` 打开报告。使用该方式前需要单独安装 [Allure Commandline](https://allurereport.org/docs/install/)。

只运行某个模块：

```bash
pytest testcase/login/test_login.py
pytest testcase/cards/test_card.py
pytest testcase/order/test_order.py
pytest testcase/Process/test_forwardprocess.py
```

按用例名称筛选：

```bash
pytest -k "用户正常登陆"
```

## YAML 用例说明

每个 YAML 文件由 `baseInfo` 和 `testCase` 两部分组成：

```yaml
- baseInfo:
    api_name: 用户登陆
    url: /api/user/login
    method: post
    header:
      Content-Type: application/json
  testCase:
    - case_name: 用户正常登陆校验
      json:
        username: admin
        password: 123456
      validation:
        - code: 200
        - contain:
            msg: 成
        - eq:
            msg: 成功
      extract:
        token: $.data.token
```

- `baseInfo`：接口名称、路径、请求方法和请求头。
- `testCase`：一条或多条测试用例。
- `json`、`data`、`params`：传给 `requests` 的请求参数。
- `extract`：使用 JSONPath 从响应中提取变量，并写入 `extract.yaml`。
- `validation`：断言规则列表。

后续用例可以通过 `${get_extract_data(token)}` 使用已提取的变量。例如：

```yaml
header:
  token: ${get_extract_data(token)}
```

## 断言类型

| 断言键 | 作用 | 示例 |
| --- | --- | --- |
| `code` | 校验 HTTP 状态码 | `- code: 200` |
| `contain` | 校验 JSONPath 对应结果是否包含预期文本 | `- contain: { "msg": "成功" }` |
| `eq` | 校验字段值是否相等 | `- eq: { "msg": "成功" }` |
| `ne` | 校验字段值是否不相等 | `- ne: { "msg": "失败" }` |
| `db` | 校验 SQL 查询是否至少返回一条数据 | `- db: "select * from \`order\` where user_id=21"` |

所有断言全部通过时测试才会通过。失败的断言会记录到 Allure 结果，并由 `pytest` 汇总。

## 执行顺序

用例通过 `pytest-order` 的 `order` 标记组织：

- 登录：`order(0)`
- 查询购物车：`order(1)`
- 添加购物车：`order(2)`
- 订单和完整业务流：`order(-1)`

完整业务流依赖登录、加购、下单和支付之间的数据传递，执行前应确保测试数据可重复使用，避免上一次运行产生的数据影响下一次运行。

## 测试报告与日志

运行 `pytest` 后，Allure 原始结果默认生成到：

```text
reports/allure-results/
```

生成并打开 HTML 报告：

```bash
allure serve reports/allure-results
```

日志默认写入 `logs/`，响应提取变量写入项目根目录的 `extract.yaml`。这两个位置以及 `reports/` 都属于本地运行生成内容，不应提交到 Git。

如需启用钉钉通知，可在 `config/base_config.py` 中将 `is_dingding` 设置为 `True`，并配置机器人 Webhook 和 Secret。当前项目直接读取该文件中的配置，建议后续改为通过环境变量或本地未跟踪配置文件注入真实凭据，不要将数据库密码、token、Webhook 或 Secret 直接提交到仓库。

## 常见问题

### 请求失败或连接超时

检查 `config/config.ini` 中的 `Host.host` 是否可以访问，并确认被测服务已启动。代码中的请求超时时间为 10 秒。

### 数据库断言失败

确认 MySQL 连接参数正确、数据库服务可访问，并检查 SQL 查询条件是否与本次测试生成的数据一致。

### 提示找不到 `allure` 命令

`allure-pytest` 只负责生成原始结果，查看报告还需要安装 Allure Commandline，并将其加入 `PATH`。

### 后续用例读取不到 token

先执行登录用例，确认 `extract.yaml` 中已生成 `token`。同时检查 YAML 中的 JSONPath 表达式是否与实际响应结构一致。

## 安全说明

- 不要提交真实的数据库密码、用户 token、钉钉 Webhook 或签名 Secret。
- 若凭据曾进入 Git 历史，应轮换凭据，而不只是删除当前文件中的文本。
- 建议为自动化测试使用独立的测试账号和最小权限数据库账号。
