# 本脚本由作者原创开发
# 作者联系信息：
#   QQ：1509377931 或 617219367
# 免责提醒：
#   - 本脚本完全开源，无任何加密。
#   - 所有请求均在本地执行，未包含外部加密操作。
# 提示：哥们我都免费了，你还删注释脸都不要了
#   - 脚本免费分享，请尊重作者劳动成果，保留注释内容。

import os
import time
import requests
import json
import urllib
import hashlib
import warnings
import qrcode
import qrcode_terminal  # 导入 qrcode-terminal

from urllib3.exceptions import InsecureRequestWarning

# 禁用警告
warnings.simplefilter('ignore', InsecureRequestWarning)

# API 签名函数
def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
    """为请求参数进行 API 签名"""
    params.update({'appkey': appkey})
    params = dict(sorted(params.items()))  # 重排序参数 key
    query = urllib.parse.urlencode(params)  # 序列化参数
    sign = hashlib.md5((query + appsec).encode()).hexdigest()  # 计算 API 签名
    params.update({'sign': sign})
    return params

# 获取二维码并返回扫码链接
def get_qrcode():
    """获取二维码并返回扫码链接"""
    response = requests.post(
        'https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code',
        params=tvsign({'local_id': '0', 'ts': int(time.time())}),
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
    ).json()

    if response['code'] != 0:
        raise Exception(f"获取二维码失败: {response.get('message', '未知错误')}")

    print(f"[INFO] 二维码链接: {response['data']['url']}")
    return response['data']['url'], response['data']['auth_code']

# 轮询扫码结果
def poll_qrcode(auth_code):
    """轮询扫码结果"""
    while True:
        response = requests.post(
            'https://passport.bilibili.com/x/passport-tv-login/qrcode/poll',
            params=tvsign({'auth_code': auth_code, 'local_id': '0', 'ts': int(time.time())}),
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            }
        ).json()

        if response['code'] == 0:
            # 登录成功
            print("[INFO] 登录成功！")
            return response['data']
        elif response['code'] == 86039:
            # 二维码未扫描，继续等待
            print("[INFO] 二维码未扫描，继续等待...")
            time.sleep(5)
        elif response['code'] == 86038:
            # 二维码已失效，重新获取
            print("[INFO] 二维码已失效，请重新获取二维码")
            return None
        else:
            # 其他错误码，抛出异常
            print(f"[ERROR] 二维码登录错误，错误码: {response['code']}")
            raise Exception(f"二维码登录错误，错误码: {response['code']}")

# 在终端显示二维码
def show_qrcode(qr_url):
    """使用 qrcode-terminal 库在终端显示二维码"""
    def generate_qrcode(data):
        qr = qrcode.QRCode(
            version=1,  # 使用较小的二维码版本
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误纠正级别
            box_size=1,  # 增加 box_size 来减少二维码的拉伸
            border=1,    # 边框大小
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

    generate_qrcode(qr_url)  # 生成二维码

# 登录并获取 Cookie
def login_and_get_cookie():
    """进行二维码登录并获取登录信息"""
    print("[INFO] ------------------ 获取二维码开始 ------------------")
    print("正在获取二维码，请稍候...")
    qr_url, auth_code = get_qrcode()

    # 在终端显示二维码
    show_qrcode(qr_url)

    print("\n[INFO] 请扫描二维码进行登录...")

    # 轮询二维码扫描状态
    login_data = poll_qrcode(auth_code)

    print("[INFO] ------------------ 登录状态 ------------------")
    if not login_data:
        print("[INFO] 登录失败")
        print("[INFO] ------------------ 任务结束 ------------------")
        return None

    # 登录成功时简化输出
    print(f"[INFO] 登录成功!")
    #作者QQ：1509377931
    # 获取有效期并返回 cookie 信息
    expires_in = login_data.get('expires_in')
    if expires_in:
        print(
            f"[INFO] 登录成功，有效期至: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + expires_in))}")

    # 只在失败时显示详细的 cookie 信息
    cookie_info = login_data.get('cookie_info', {})
    cookies = cookie_info.get('cookies', [])
    bili_jct = None
    SESSDATA = None

    # 遍历 cookies 列表，提取 bili_jct 和 SESSDATA
    for cookie in cookies:
        if cookie['name'] == 'bili_jct':
            bili_jct = cookie['value']
        elif cookie['name'] == 'SESSDATA':
            SESSDATA = cookie['value']

    if not bili_jct or not SESSDATA:
        print("[ERROR] 未能成功获取 bili_jct 或 SESSDATA")
        print(f"[INFO] 登录数据: {json.dumps(login_data, indent=2)}")
        raise Exception("登录信息缺失，未能成功获取 bili_jct 或 SESSDATA")

    return bili_jct, SESSDATA

# 使用登录后获取的 cookie 进行后续请求
def make_request(bili_jct, SESSDATA):
    """使用登录后获取的 cookie 进行后续请求"""
    url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/set"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Referer": "https://message.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/615.3.12.10.2 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "Origin": "https://message.bilibili.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Fetch-Mode": "cors",
        "Host": "api.vc.bilibili.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "empty",
        "Cookie": f"SESSDATA={SESSDATA}; bili_jct={bili_jct}",
    }

    data = {
        "keys_reply": "1",
        "csrf_token": bili_jct,
        "csrf": bili_jct,
    }

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("code") == 0:
                print("[INFO] 自动回复开启成功")
            else:
                print(f"[ERROR] 请求失败，返回的错误：{response_json.get('msg', '未知错误')}")
        else:
            print(f"[ERROR] 请求失败，HTTP 状态码: {response.status_code}")
            print(f"[ERROR] 响应内容: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求发生异常: {e}")

# 主函数
def main():
    try:
        # 登录并获取 cookie
        cookie_info = login_and_get_cookie()
        if cookie_info:
            bili_jct, SESSDATA = cookie_info
            # 使用登录信息发送请求
            make_request(bili_jct, SESSDATA)
        else:
            print("[ERROR] 登录失败，无法获取登录信息。")
    except Exception as e:
        print(f"[ERROR] 发生错误: {e}")

# 确保这个文件作为主程序执行
if __name__ == "__main__":
    main()
