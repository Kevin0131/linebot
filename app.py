from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from flask import jsonify,  send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import render_template, jsonify, send_from_directory

import configparser

import random

from myfsm import TocMachine

app = Flask(__name__, static_url_path='/image')

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

#port記得用5003
machine = TocMachine(
    states=["user", "imgState", "ttState",
            "songState", "searchImage", "answer", "weather"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "imgState",
            "conditions": "is_going_to_imgState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "ttState",
            "conditions": "is_going_to_ttState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "songState",
            "conditions": "is_going_to_songState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "searchImage",
            "conditions": "is_going_to_searchImage",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "answer",
            "conditions": "is_going_to_answer",
        },
        
        {
            "trigger": "advance",
            "source": "user",
            "dest": "weather",
            "conditions": "is_going_to_weather",
        },
        {"trigger": "go_back", "source": [
            "imgState", "ttState", "songState", "searchImage", "answer", "weather"], 
            "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

# 自動推播
line_bot_api.push_message(
    'U1aba4f467e2c0ae46c21b2aeea79b519', TextSendMessage(text='我是你的個人小助理kevin,很高興為你服務'))

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     line_bot_api.push_message(
#         'Udaa53119f038c9c8a346b9a6b5a770e5', TextSendMessage(text='我是你的個人小助理nikey,很高興為你服務'))
#     return 'success'

# 接收 LINE 的資訊


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        response = machine.advance(event)
        if response == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="not enter any state")
            )


if __name__ == "__main__":
    app.run(port=5003)