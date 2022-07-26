# -*- coding: utf-8 -*-
# @Time    : 2021/10/8
import hmac
import json
import random
import re
import time
from hashlib import md5, sha1
from urllib.parse import quote

import cv2
import execjs
import numpy as np
import requests
from decorator import decorator
from requests.exceptions import ProxyError, HTTPError, Timeout


# 装饰器捕获异常
@decorator
def httpRequestDecorator(func, *args, **kwargs):
    tryCount = 1
    while True:
        try:
            return func(*args, **kwargs)
        # http一般异常处理
        except (ProxyError, ConnectionError, HTTPError, Timeout):
            # print('----Some HttpError----')
            pass
        except Exception as e:
            print(e)
        if tryCount >= 10:
            return "codeError"

        tryCount += 1


@decorator
def funcResultDecorator(func, *args, **kwargs):
    try:
        return func(*args, *kwargs)
    # 捕获codeError
    except ValueError:
        return {"success": False, "msg": "本地API错误"}


# 代理（不能用隧道代理！ d_c0的IP与登录的IP必须一致）
def getProxy():
    return {}


def randomCallbackStr():
    randomList = [str(i) for i in range(0, 9)] + [chr(i) for i in range(97, 123)]
    jsCallback = ""

    for _ in range(7):
        jsCallback += random.choice(randomList)
    jsCallback = f"__JSONP_{jsCallback}_0"

    return jsCallback


class SlideCrack(object):
    def __init__(self, gap, bg):
        """
        :param gap: 缺口图片
        :param bg: 背景图片
        :param out: 输出图片
        """
        self.gap = gap
        self.bg = bg

    @staticmethod
    def clear_white(img):
        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imdecode(img, -1)

        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y:max_y]
        return img1

    def template_match(self, tpl, target):
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0,0,255)：矩形边框颜色
        # 1：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        # cv2.imwrite(self.out, target)
        return tl[0]

    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def discern(self):
        img1 = self.clear_white(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        back = cv2.imdecode(self.bg, 0)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = self.template_match(slide_pic, back_pic)
        # 输出横坐标, 即 滑块在图片上的位置
        return x


class yidunSlider:
    def __init__(self):
        """
        :param proxy: 代理
        :param rSession: rSession 开启会话 节约Tcp
        :param headers: --
        """
        self.proxy = getProxy()
        self.rSession = requests.Session()
        # 挂上代理
        # self.rSession.proxies = self.proxy
        self.headers = {
            "Host": "c.dun.163.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            "Referer": "https://www.zhihu.com/signin?next=%2F",
        }

    @httpRequestDecorator
    def getSliderImage(self):
        with open("JavaScript/fp.js") as file:
            exj = execjs.compile(file.read())
            fp = exj.call("get_fp")
        with open("Javascript/cb.js") as file:
            exj = execjs.compile(file.read())
            cb = exj.call("getCb")

        jsCallback = randomCallbackStr()
        url = f"https://c.dun.163.com/api/v2/get?referer=https%3A%2F%2Fwww.zhihu.com%2Fsignin&zoneId=CN31&id=ffccaa537da544269b4c9c1dc84dcb73&fp={fp}&version=2.15.2&cb={quote(cb)}&callback={jsCallback}"

        response = self.rSession.get(url, headers=self.headers)
        response = json.loads(response.text.replace(jsCallback, "")[1:-2])

        if response["msg"] == "ok":
            data = response["data"]
            background = data["bg"][0]
            slider = data["front"][0]
            token = data["token"]
            # print(background,slider)
            return background, slider, token, fp

    @httpRequestDecorator
    def sliderDistance(self, backgroundUrl, sliderUrl):
        a = self.rSession.get(backgroundUrl).content
        b = self.rSession.get(sliderUrl).content

        backgroundImage = np.asarray(bytearray(a), dtype="uint8")
        sliderImage = np.asarray(bytearray(b), dtype="uint8")

        slideCrack = SlideCrack(backgroundImage, sliderImage)
        distance = slideCrack.discern()

        return distance

    def randomTrajectory(self, distance, token, fp):

        moveCount = random.choice(range(30, 50))
        stepLength = int(distance / moveCount)
        xStart = 4
        yStart = random.choice([-1, 0, 1])
        startTime = random.choice(range(50, 100))
        Jackpot = distance - stepLength * moveCount
        Jackpot += 1

        trajectoryList = []
        with open("JavaScript/encryptionTrajectory.js", encoding="utf-8") as file:
            exj = execjs.compile(file.read())
            for _ in range(moveCount):
                step = ",".join([str(xStart), str(yStart), str(startTime)])
                # 第一步
                if _ == 0:
                    encryptionTrajectory = exj.call("encryptionTrajectory", token, step)
                    trajectoryList.append(encryptionTrajectory)

                randomStep = random.choice(range(stepLength))
                Jackpot += stepLength - randomStep

                if Jackpot > 10:
                    luckStep = random.choice(range(10))
                else:
                    luckStep = random.choice(range(Jackpot))

                if random.choice(range(1, 20)) == 1:
                    yStart -= 1
                startTime += random.choice(range(5, 15))
                xStart += randomStep + luckStep
                Jackpot -= luckStep

                encryptionTrajectory = exj.call("encryptionTrajectory", token, step)
                trajectoryList.append(encryptionTrajectory)

        with open("JavaScript/cb.js") as file1:
            exj1 = execjs.compile(file1.read())
            trajectoryList = ":".join(trajectoryList)
            trajectory = exj1.call("B", trajectoryList)
            cb = exj1.call("getCb")

            with open("JavaScript/encryptionTrajectory.js", encoding="utf-8") as file2:
                exj2 = execjs.compile(file2.read())
                trajectoryList = ":".join(trajectoryList)
                r = exj1.call("B", exj2.call("n", token, str((distance) / 320 * 100)))
                ext = exj1.call("B", exj2.call("n", token, f"1,{len(trajectoryList)}"))

        data = {"d": trajectory, "m": "", "p": r, "ext": ext}
        jsCallback = randomCallbackStr()

        url = f"https://c.dun.163.com/api/v2/check?referer=https%3A%2F%2Fwww.zhihu.com%2Fsignin&zoneId=CN31&id=ffccaa537da544269b4c9c1dc84dcb73&token={token}&acToken={token}&data={quote(json.dumps(data), safe='')}&width=320&type=2&version=2.14.4&cb={quote(cb, safe='')}&callback={jsCallback}"

        response = requests.get(url, headers=self.headers)

        data = json.loads(response.text.replace(jsCallback, "")[1:-2])["data"]
        if data["result"]:
            return data["validate"]

    @funcResultDecorator
    def passSlider(self):
        backgroundUrl, sliderUrl, token, fp = self.getSliderImage()
        distance = self.sliderDistance(backgroundUrl, sliderUrl)
        # print(distance)
        validate = self.randomTrajectory(distance, token, fp)
        return fp, validate


class zhihuLogin:
    def __init__(self, fp, validate):
        """
        :param fp: 滑块中用的的fingerprint
        :param validate: 易盾滑块绕过返回的凭证
        :param proxy: 代理
        :param rSession: rSession 开启会话 节约Tcp 保存知乎后端的set-cookies
        :param headers: --
        """
        self.fp = fp
        self.validate = validate

        self.proxy = getProxy()
        self.rSession = requests.Session()
        # 挂上代理
        # self.rSession.proxies = self.proxy

    @httpRequestDecorator
    def getD_c0(self):
        url = "http://www.zhihu.com/explore"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            "Cookie": ""
        }

        response = requests.get(url, headers=headers)
        d_c0 = "".join(re.findall('d_c0="(.*)";', response.headers["set-cookie"]))

        if d_c0 == "":
            raise HTTPError("没有d_c0")
        return d_c0.replace(" ", "")

    @staticmethod
    def getX_ZSE_96(text):
        encryptedText = md5(text.encode("utf-8")).hexdigest()
        with open(r"Javascript/x86.js") as file:
            exj = execjs.compile(file.read())
            x86 = exj.call("Luob", encryptedText).replace("9Tuw", "")
            return "2.0_" + x86

    @httpRequestDecorator
    def preposition(self):
        url = "https://www.zhihu.com/api/v3/oauth/captcha/v2?type=captcha_sign_in"

        headers = {
            "authority": "www.zhihu.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        }

        self.rSession.get(url, headers=headers)

    @httpRequestDecorator
    def getCaptchaTicketV2(self):
        with open("JavaScript/verificationCodeEncryption.js", encoding="utf-8") as file:
            exj = execjs.compile(file.read())
            ticket = exj.call("verificationCodeEncryption", self.validate, self.fp)
        body = "ticket=" + quote(json.dumps({"validate": ticket}), safe="")

        d_c0 = self.getD_c0()
        self.preposition()

        text = f'101_3_2.0+/api/v3/oauth/captcha/v2+"{d_c0}"+{body}'
        x_zse_96 = self.getX_ZSE_96(text)
        url = "https://www.zhihu.com/api/v3/oauth/captcha/v2"
        payload = body
        headers = {
            "authority": "www.zhihu.com",
            "x-zse-93": "101_3_2.0",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            "content-type": "application/x-www-form-urlencoded",
            "x-zse-96": x_zse_96,
            "referer": "https://www.zhihu.com/signin?next=%2Fsettings%2Faccount",
        }

        jar = requests.cookies.RequestsCookieJar()
        jar.set("d_c0", d_c0)
        self.rSession.cookies.update(jar)

        response = self.rSession.put(url, headers=headers, data=payload)
        if response.json()["success"]:
            return True
        else:
            return False

    @httpRequestDecorator
    def login(self, phoneNumber, password):
        self.getCaptchaTicketV2()
        timeStamp = time.time()
        timeStamp = str(int(timeStamp * 1000))
        text = f"passwordc3cef7c66a1843f8b3a9e6a1e3160e20com.zhihu.web{timeStamp}"
        signature = hmac.new(
            "d1b964811afb40118a12068ff74a12f4".encode("utf-8"),
            text.encode("utf-8"),
            sha1,
        ).hexdigest()

        encryptedDict = {
            "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
            "grant_type": "password",
            "timestamp": timeStamp,
            "source": "com.zhihu.web",
            "signature": signature,
            "username": f"%2B86{phoneNumber}",
            "password": f"{password}",
            "captcha": "",
            "utm_source": "",
            "ref_source": "other_https://www.zhihu.com/signin?next=%2F",
        }

        encryptedText = ""

        for key, value in encryptedDict.items():
            encryptedText += key + "=" + value + "&"

        encryptedText = encryptedText[:-1]

        with open("JavaScript/loginEncrypt.js", encoding="utf-8") as file:
            exj = execjs.compile(file.read())
            encryptedText = exj.call("loginEncrypt", encryptedText)

        encryptedText = encryptedText[:-4]

        url = "https://www.zhihu.com/api/v3/oauth/sign_in"

        payload = encryptedText
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
            "content-type": "application/x-www-form-urlencoded",
            "x-zse-83": "3_2.0",
        }

        response = self.rSession.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()


if __name__ == "__main__":
    ydSlider = yidunSlider()
    while True:
        fp, validate = ydSlider.passSlider()
        zhLogin = zhihuLogin(fp, validate)
        flag, ckData = zhLogin.login("15574973835", "weilaike7")
        print("login success")
        print(ckData['cookie'])
        break
