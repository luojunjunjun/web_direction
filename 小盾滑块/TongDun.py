# -*- coding:utf-8 -*-
# Time : 2022/7/20 9:31
import json
import random
import time
from hashlib import md5
from io import BytesIO
from string import ascii_letters, digits
from urllib.parse import quote

import execjs
import requests
from PIL import Image
from decorator import decorator
from requests.exceptions import ProxyError, ConnectionError, HTTPError, Timeout

from SlideCrack import SlideCrack

'''
存在的问题：
1、滑块识别率不高
2、轨迹有点问题，不清楚是哪里 我猜测是 mouse_start_x，mouse_start_y 的偏移？
'''


@decorator
def http_retry(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        # 一般Http异常处理
        except (ProxyError, ConnectionError, HTTPError, Timeout) as e:
            pass
        except Exception as e:
            print(e)


# 最好是挂上代理
def get_proxy():
    return {}


class TongDunSlide:
    def __init__(self):
        self.http_client = requests.session()
        self.partner = 'aopengjy'
        self.app_name = 'aopengOESjx_web'
        # self.partner = 'hsyuntai'
        # self.app_name = 'hsyuntai_h5'
        self.token_id = f'{self.partner}-{int(time.time() * 1000)}-{"".join(random.sample((ascii_letters[:6] + digits) * 1000, 13))}'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://learn.open.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://learn.open.com.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.black_box = self.get_black_box()

    def get_captcha_token(self):
        url = f'http://learn.open.com.cn/Account/CaptchaToken?bust={int(time.time())}'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Content-Length': '0',
            'Cookie': '',
            'Origin': 'http://learn.open.com.cn',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://learn.open.com.cn/account/TLogin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = self.http_client.get(url, headers=headers, proxies=get_proxy())

        return response.json()['data']

    def base_n(self, num, b):
        return ((num == 0) and "0") or \
               (self.base_n(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

    def get_black_box(self):
        i = '^^'.join([str(x) for x in [
            int(time.time() * 1000),
            "Win32",
            304,
            1920,
            md5(random.randint(1, 99999999).__str__().encode()).hexdigest(),
            "-",
            480,
            "http%3A%2F%2Flearn.open.com.cn%2Faccount%2FTLogin",
            1920,
            "zh-CN,en,en-GB,en-US",
            "1",
            1920,
            1,
            "-",
            "ABeRZOkFWjbGmBTmdUSIY7NqUenBbjO3+2iXPOevLSDCGEsNQwc8D4GQshPUDNXRILIvrThfeEdb42Lgh7Q4FQ==",
            "functiongetParameter(){[nativecode]}",
            "-",
            "-",
            self.base_n(int(time.time() * 1000), 32)
        ]])
        j = '^^'.join([str(x) for x in [
            "zh-CN",
            "-",
            "-",
            f"{md5(random.randint(1, 99999999).__str__().encode()).hexdigest()}|01100100000111000011110011010010000011001010110001111111111011111",
            1080,
            1080,
            "-",
            "-",
            "Google Inc. (Intel)-&-ANGLE (Intel, Intel(R) UHD Graphics 770 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "[object Window]",
            "-",
            "-",
            self.base_n(int(time.time() * 1000), 32)
        ]])
        k = '^^'.join([str(x) for x in [
            "-",
            md5(random.randint(1, 99999999).__str__().encode()).hexdigest(),
            "-",
            "-",
            "Netscape",
            "11110",
            "280204",
            "-",
            1080,
            24,
            "48000_2_1_0_2_explicit_speakers",
            "0",
            "-",
            "-",
            "-",
            self.base_n(int(time.time() * 1000), 32)
        ]])
        l = '^^'.join([str(x) for x in [
            "-",
            1920,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49",
            md5(random.randint(1, 99999999).__str__().encode()).hexdigest(),
            "-",
            1080,
            "-",
            1920,
            "Mozilla",
            f"{md5(random.randint(1, 99999999).__str__().encode()).hexdigest()}|{md5(random.randint(1, 99999999).__str__().encode()).hexdigest()}",
            "Webkit-Chrome",
            "functiongetoffsetHeight(){[nativecode]}",
            md5(random.randint(1, 99999999).__str__().encode()).hexdigest(),
            self.base_n(int(time.time() * 1000), 32)
        ]])
        o = '^^'.join([str(x) for x in [
            "Failed to construct 'WebSocket': The URL 'itsgonnafail' is invalid.",
            "MOZ8b0s0-1658050368065-ef468c66611ed824410076",
            "functiontoDataURL(){[nativecode]}",
            "function(){[nativecode]}",
            "-",
            24,
            "-",
            "functiontoString(){[nativecode]}",
            "-",
            33,
            "-",
            24,
            "1",
            "[objectPluginArray]",
            "functioncreateAnalyser(){[nativecode]}",
            "-",
            "-",
            "-",
            "-",
            self.base_n(int(time.time() * 1000), 32)
        ]])
        f = '^^'.join([str(x) for x in [
            '1',
            '0',
            '0',
            '0',
            '0',
            '0'
        ]])

        ct = f'{random.randint(1000, 100000)}'

        # 固定
        v = '8nz+Qmys4G/jQb+Ug+CTXTluMaJz45qb+0swimDDtiexGj8IouOTVWXcFdsjO+00'
        e = 'f+ZhAI9xfXtHNNQzpuMufObh+n+gRYeW7ySf3KzCjm4mdK49j52wG2NXC6YjECBSGWmPfsjGCYeYYLFIVAk4IrCkB/dIg+oMqmU74MK+Amg='

        t_13 = int(time.time() * 1000)
        idf = f'{t_13}-{random.randint(1000000, 9999999)}'

        url = "https://fp.tongdun.net/web3_8/profile.json"

        with open('JavaScript/fm.js', encoding='utf-8') as file:
            exj = execjs.compile(file.read())

        idf = exj.call('OoQO0Q', idf)
        i = exj.call('QoOOO0', i, idf[:24])
        j = exj.call('QoOOO0', j, idf[:24])
        k = exj.call('QoOOO0', k, idf[:24])
        l = exj.call('QoOOO0', l, idf[:24])
        o = exj.call('QoOOO0', o, idf[:24])
        f = exj.call('QoOOO0', f, idf[:24])
        w = exj.call('QoOOO0', v, idf[:24])
        ct = exj.call('QoOOO0', ct, idf[:24])
        idf = exj.call('getEncryptedPassword', idf)
        _callback = f'_{t_13}_{random.randint(1000, 100000)}'
        url_params = {
            'partner': self.partner,
            'app_name': self.app_name,
            'token_id': self.token_id,
            'i': i,
            'j': j,
            'k': k,
            'l': l,
            'o': o,
            'f': f,
            'e': e,
            'v': v,
            'idf': idf,
            'w': w,
            'ct': ct,
            '_callback': _callback,
        }

        h = '?'
        for key, value in url_params.items():
            h += key + '=' + value + "&"
        h = h[:-1]

        h = exj.call('oQO0Q0.hash128', h)

        url_params['h'] = h

        response = self.http_client.get(url, headers=self.headers, params=url_params, proxies=get_proxy())

        return json.loads(response.text.replace(_callback, '')[1:-1])

    @http_retry
    def get_two_image(self):
        # 会根据ip蹦点选 所以出现的不是滑块就一直更换 captcha_token
        captcha_token = self.get_captcha_token()

        url = f'https://sphinx.tongdun.net/sphinx/captcha/v1?partnerCode={self.partner}&appName={self.app_name}&sessionId={self.token_id}'

        payload = f"captchaToken={captcha_token}&blackBox={self.black_box['result']['tokenId']}"

        response = self.http_client.post(url, headers=self.headers, data=payload, proxies=get_proxy())

        result = response.json()
        # return result['validateCodeObj']
        if result['failMes'] == '成功' and result['validateCodeObj']['imageType'] == '1':
            return result['validateCodeObj']
        else:
            # print(result)
            raise Timeout("非滑块 - - 重试")

    @staticmethod
    def reduction_bg(bg_offset, bg_content):
        bytes_stream = BytesIO(bg_content)
        img = Image.open(bytes_stream)
        arr = [[], []]
        for i in range(2):
            for j in range(8):
                part_img = img.crop((j * 40, i * 90, (j + 1) * 40, (i + 1) * 90))
                arr[i].append(part_img)
        # 以下是拼凑图片部分
        counter = 0
        arr_recv = [[], []]
        for i in arr_recv:
            for j in range(8):
                i.append([])

        for i in range(16):
            num = int(bg_offset[counter], 16)
            if num < 8:
                if counter >= 8:
                    arr_recv[0][num] = arr[1][counter - 8]
                else:
                    arr_recv[0][num] = arr[0][counter]
            else:
                if counter >= 8:
                    arr_recv[1][num - 8] = arr[1][counter - 8]
                else:
                    arr_recv[1][num - 8] = arr[0][counter]
            counter += 1
        to_image = Image.new('RGB', (320, 180))

        for i in arr_recv:
            for j in i:
                to_image.paste(j, (
                    i.index(j) * 40, arr_recv.index(i) * 90, (i.index(j) + 1) * 40, (arr_recv.index(i) + 1) * 90))

        to_image.save('bb.jpg')
        to_image_arr = BytesIO()
        to_image.save(to_image_arr, format='JPEG')
        to_image_arr = to_image_arr.getvalue()

        return to_image_arr

    @staticmethod
    def get_track(distance, start_x, start_y):
        track_list = []

        t_13 = int(time.time() * 1000)

        while True:
            move_time = random.randint(10, 20)
            t_13 += move_time

            if len(track_list) < 5:
                track_list.append({
                    'type': 1
                    , 'time': t_13
                    , 'Action': ''
                    , 'op_x': start_x + random.choice([31, 32, 33, 24, 25, 26, 27, 38, 39])
                    , 'op_y': start_y + random.choice([31, 32, 33, 24, 25, 26, 27, 38, 39])
                })
            elif len(track_list) == 5:
                track_list.append({
                    'type': 1
                    , 'time': t_13
                    , 'Action': 12
                    , 'op_x': start_x - random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
                    , 'op_y': start_y - random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
                })
                track_list.append({
                    'type': 2
                    , 'time': t_13
                    , 'Action': ''
                    , 'op_x': start_x
                    , 'op_y': start_y
                })

            elif distance > 0:
                x_move_distance = random.choice([1, 1, 1, 1, 1, 2, 2, 3])
                y_move_distance = random.choice([0, 0, 0, 0, 0, 0, 1, -1])

                distance -= x_move_distance
                start_x += x_move_distance
                start_y += y_move_distance
                track_list.append({
                    'type': 1
                    , 'time': t_13
                    , 'Action': ''
                    , 'op_x': start_x
                    , 'op_y': start_y
                })
            elif distance <= 0:
                track_list.append({
                    'type': 3
                    , 'time': t_13
                    , 'Action': 13
                    , 'op_x': start_x + distance
                    , 'op_y': start_y + distance
                })
                break

        for _ in range(5):
            move_time = random.randint(10, 20)
            t_13 += move_time
            track_list.append({
                'type': 1
                , 'time': t_13
                , 'Action': ''
                , 'op_x': start_x - random.choice([1, -2, 3, -4, 5, -6, 7, -8, 9])
                , 'op_y': start_y - random.choice([1, -2, 3, -4, 5, -6, 7, -8, 9])
            })
        return track_list

    def verification(self):
        image_info = self.get_two_image()
        print(image_info)
        original_bg_content = self.http_client.get('https://static.tongdun.net' + image_info['slideBgi'],
                                                   headers=self.headers).content
        slide_content = self.http_client.get('https://static.tongdun.net' + image_info['slideImage'],
                                             headers=self.headers).content

        reduction_bg_content = self.reduction_bg(image_info['bgImageSplitSequence'], original_bg_content)

        with open('1.png', 'wb') as file:
            file.write(slide_content)
        with open('bb.jpg', 'wb') as file:
            file.write(reduction_bg_content)

        distance = SlideCrack(bg=reduction_bg_content, gap=slide_content).discern()
        print(distance)
        t_13 = int(time.time() * 1000) - random.randint(1000, 9999)
        mouse_start_x = random.randint(808, 812)
        mouse_start_y = random.randint(600, 609)
        # mouse_start_x = 800
        # mouse_start_y = 603
        # distance -= mouse_start_x - 800
        print(distance, mouse_start_x, mouse_start_y)
        track = self.get_track(distance, mouse_start_x, mouse_start_y)

        # 'm8,g9,ne,hd,nh,gj,m8,cv,1,0,l5s7syji'
        mouse_start = f'm8,g9,ne,hd,{self.base_n(mouse_start_x, 36)},{self.base_n(mouse_start_y, 36)},m8' \
                      f',{self.base_n(375 + image_info["slideY"], 36)},1,0,{self.base_n(t_13, 36)}'
        mouse_info = mouse_start + "%"

        for _ in track:
            # w2vn6,1,10j,bd|
            case = ''
            case += self.base_n(_['time'] - t_13, 36) + ","
            case += self.base_n(_['type'], 36) + ","
            case += self.base_n(_['op_x'], 36) + ","
            if _['Action']:
                case += self.base_n(_['op_y'], 36) + ','
                case += self.base_n(int(_['Action']), 36) + "|"
            else:
                case += self.base_n(_['op_y'], 36) + "|"
            mouse_info += case
        a = 'https://sphinx.tongdun.net/sphinx/validatecode/v1'
        b = {
            "requestType": 3,
            "validateCodeObj": json.dumps(image_info, separators=(',', ':'), ensure_ascii=False),
            "userAnswer": f"{distance}|10|{int(time.time() * 1000)}",
            "mouseInfo": mouse_info,
            "usedTime": random.randint(4000, 16000),
            "blackBox": self.black_box['result']['tokenId']
        }
        print(b)
        with open('JavaScript/tdCaptcha.js', encoding='utf-8') as file:
            exj = execjs.compile(file.read())

        n_p, p1, p2 = exj.call("get_n_p", a, b, self.token_id)
        url = f"https://sphinx.tongdun.net/sphinx/validatecode/v1?p1={quote(p1)}&p2={quote(p2)}"
        payload = ''
        for key, value in n_p.items():
            payload += f'{key}={str(value)}&'
        payload = payload[:-1]
        print(payload)

        response = self.http_client.post(url, headers=self.headers, data=payload)
        # 出validateToken 就是成功
        print(response.json().get("validateToken"))
        print(response.json())


if __name__ == '__main__':
    td = TongDunSlide()
    td.verification()
