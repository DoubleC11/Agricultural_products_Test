import urllib, base64
import hmac, hashlib, time, logging, requests


def send_custom_robot_group_message(access_token, secret, msg, at_user_ids=None, at_mobiles=None, is_at_all=False):
    """
    发送钉钉自定义机器人群消息
    :param access_token: 机器人webhook的access_token
    :param secret: 机器人安全设置的加签secret
    :param msg: 消息内容
    :param at_user_ids: @的用户ID列表
    :param at_mobiles: @的手机号列表
    :param is_at_all: 是否@所有人
    :return: 钉钉API响应
    """
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}&timestamp={timestamp}&sign={sign}'

    body = {
        "at": {
            "isAtAll": str(is_at_all).lower(),
            "atUserIds": at_user_ids or [],
            "atMobiles": at_mobiles or []
        },
        "text": {
            "content": msg
        },
        "msgtype": "text"
    }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, json=body, headers=headers)
    logging.info("钉钉自定义机器人群消息响应：%s", resp.text)
    return resp.json()


if __name__ == '__main__':
    DINGTALK_WEBHOOK = "4ab1fddffdf947bc6fe632ee1988c618d84b53246cb8484e8852a906c3565791"
    DINGTALK_SECRET = "SEC1d9ab9542807e9b0feb45a42fac2ffddde105393e534b6ea10e13bdf977a7df2"  # 如果机器人开启了
    print(send_custom_robot_group_message(access_token=DINGTALK_WEBHOOK, secret=DINGTALK_SECRET, msg="你好"))
