import os
import re
from transitions.extensions import GraphMachine

from flask import Flask, request, abort
from flask import jsonify,  send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from flask import render_template, jsonify, send_from_directory

import configparser

import random

from urllib import request
from urllib.parse import urlencode
import requests

import json

config = configparser.ConfigParser()
config.read('config.ini')

handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

app = Flask(__name__, static_url_path='/image')

to_user = 'U1aba4f467e2c0ae46c21b2aeea79b519'

tt = ["我真的是太笨了。」\n「怎麼啦？」\n「除了喜歡你，其它什麼都做不好。", "「你有個缺點。」\n「什麼？」\n「缺點我。」", "「你單身多久了？」\n「一年多了。」\n「對不起，讓你等了這麼久。」",
      "「我覺得我好花心。」\n「為什麼？」\n「因為你的每個樣子我都喜歡。」",
      "過去有人曾對我說，「一個人愛上小溪，是因為沒有見過大海。」\n而如今我終於可以說，「我已見過銀河，但我仍只愛你一顆星。」"]
bool_tt = [False for i in range(5)]

songs = ["時光是琥珀 淚一滴滴 被反鎖\n情書再不朽 也磨成沙漏\n青春的上游 白雲飛走 蒼狗與海鷗 \n閃過的念頭 潺潺的溜走",
         "可惜不是你，陪我到最後————梁靜茹「可惜不是你」",
         "如果他總為別人撐傘，你何苦非為他等在雨中————梁靜茹「分手快樂」",
         "如果當時我們能不那麼倔強，現在也不那麼遺憾————劉若英「後來」",
         "以為對的人還在最遠的地方等候，所以值得放棄了所有————徐若瑄「幸福的輪廓」"]
bool_songs = [False for i in range(5)]

replys = ["不會，祝您有個美好的一天",
         "nmsl",
         "祝您事事順心",
         "祝您早日脫單",
         "992330"] 
bool_replys = [False for i in range(5)] 


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_imgState(self, event):
        text = event.message.text
        return ("偶像" in text)

    def is_going_to_ttState(self, event):
        text = event.message.text
        return ("搭訕" in text)

    def is_going_to_songState(self, event):
        text = event.message.text
        return ("情歌" in text)

    def is_going_to_searchImage(self, event):
        text = event.message.text
        return ("搜尋" in text)

    def is_going_to_answer(self, event):
        text = event.message.text
        return (("謝謝" in text) or ("牛逼" in text))


    def is_going_to_weather(self, event):
        text = event.message.text
        return ("天氣" in text)

    # image
    def on_enter_imgState(self, event):
        reply_token = event.reply_token
        text = "這是我的偶像"
        line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

        img_url = 'https://s.yimg.com/ny/api/res/1.2/jgyqLsboZ4NBFdzYqvnc3A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTgwMA--/https://media.zenfs.com/zh-tw/setn.com.tw/5acb01afa98f6cd1049dd3843bb4a134'
        image_message = ImageSendMessage(
            original_content_url=img_url, preview_image_url=img_url)
        line_bot_api.push_message(to_user, image_message)
        self.go_back()

    def on_exit_imgState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="字母哥總冠軍!"))

    # tt

    def on_enter_ttState(self, event):
        global bool_tt

        index = random.randint(0, 4)
        while bool_tt[index] is True:
            index = random.randint(0, 4)

        bool_tt[index] = True
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=tt[index]))

        if False not in bool_tt:
            bool_tt = [False for i in range(5)]

        self.go_back()

    def on_exit_ttState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="可以跟你要line嗎"))

    # song

    def on_enter_songState(self, event):
        global bool_songs

        index = random.randint(0, 4)
        while bool_songs[index] is True:
            index = random.randint(0, 4)

        bool_songs[index] = True
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=songs[index]))

        if False not in bool_songs:
            bool_songs = [False for i in range(5)]

        self.go_back()

    def on_exit_songState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="emo了嗎單身狗"))

    # search image

    def on_enter_searchImage(self, event):
        text = str(event.message.text)
        tmp = text.split(" ")
        text = tmp[1]

        img_search = {'tbm': 'isch', 'q': text}
        query = urlencode(img_search)
        base = "https://www.google.com/search?"
        url = str(base+query)

        headers = {'user-agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        res = request.Request(url, headers=headers)
        con = request.urlopen(res)
        data = con.read()

        pattern = '"(https://encrypted-tbn0.gstatic.com[\S]*)"'

        img_list = []
        for match in re.finditer(pattern, str(data, "utf-8")):
            if len(match.group(1)) < 150:
                img_list.append(match.group(1))

        random_img_url = img_list[random.randint(0, len(img_list)+1)]

        line_bot_api.push_message(to_user, ImageSendMessage(original_content_url=random_img_url,
                                                            preview_image_url=random_img_url))

        self.go_back()

    def on_exit_searchImage(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="這圖片有料吧"))

    # answer

    def on_enter_answer(self, event):
        global bool_replys

        index = random.randint(0, 4)
        while bool_replys[index] is True:
            index = random.randint(0, 4)

        bool_replys[index] = True
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=replys[index]))

        if False not in bool_replys:
            bool_replys = [False for i in range(5)]

        self.go_back()

    def on_exit_answer(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="嘻嘻"))



    

    # weather
    def on_enter_weather(self, event):
        text = str(event.message.text)
        tmp = text.split(" ")
        city = tmp[1]

        token = "CWB-7A3D016E-7F19-40AA-94D6-E29866104ED3"
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + \
            token + '&format=JSON&locationName=' + city
        Data = requests.get(url)
        f = open('weather.json', 'w', encoding='utf-8')
        f.write(Data.text)
        f.close()

        jf = open('weather.json', 'r', encoding='utf-8')
        dic_data = json.load(jf)
        jf.close()

        res = dic_data['records']['location'][0]['weatherElement']
        stime = res[1]["time"][0]["startTime"]
        etime = res[1]["time"][0]["endTime"]
        condition = res[0]["time"][0]["parameter"]["parameterName"]
        pop = res[1]["time"][0]["parameter"]["parameterName"]
        mint = res[2]["time"][0]["parameter"]["parameterName"]
        maxt = res[4]["time"][0]["parameter"]["parameterName"]

        t1 = f'{city}十二小時天氣預報\n'
        t2 = f'(從{stime}到{etime})\n'
        t3 = f'天氣狀況: {condition}\n'
        t4 = f'最高溫: {maxt}\n'
        t5 = f'最低溫: {mint}\n'
        t6 = f'降雨機率: {pop}'
        t = t1+t2+t3+t4+t5+t6

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=t))
        if int(maxt) < 20:
            line_bot_api.push_message(
                to_user, TextSendMessage(text="天氣變化劇烈記得多帶件衣物喔！！"))

        self.go_back()

    def on_exit_weather(self):
        pass
