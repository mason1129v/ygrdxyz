from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from datetime import datetime, timezone, timedelta
from uni.models import *
import os
import requests
import openai
import json
from django.http import JsonResponse
from django.utils.html import escape
import asyncio
from asgiref.sync import sync_to_async
from flask import Flask, request, render_template, jsonify
import pyttsx3
import tracemalloc
import threading
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone

# tracemalloc.start()
checknum = 0

OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

def clear_mess_data():
    messbrd.objects.all().delete()
    c_messbrd.objects.all().delete() 
    Notifications.objects.all().delete()
    print("success_open")
clear_mess_data()

def A_view(request):
    return render(request, 'a.html', locals())

def B_view(request):
    return render(request, 'b.html', locals())



def chat_view(request):
    return render(request, 'chat.html', locals())


app = Flask(__name__)

# executor = ThreadPoolExecutor()
# completion_event = asyncio.Event()

# async def speak_async(text):
#     # 添加一些日志以验证引擎是否工作
#     print("speak_async started")
#     engine.say(text)
#     engine.runAndWait()

#     # 设置完成事件
#     completion_event.set()
#     print("speak_async finished")


@sync_to_async
def save_message(user_input, ai_response):
    usermess = messbrd(MID=1, MCont=user_input, MDATE=now)
    usermess.save()

    newmess = messbrd(MID=2, MCont=ai_response, MDATE=now)
    newmess.save()

@sync_to_async
def save_message_cloth(user_input, ai_response):
    usermess = c_messbrd(MID=1, MCont=user_input, MDATE=now)
    usermess.save()

    newmess = c_messbrd(MID=2, MCont=ai_response, MDATE=now)
    newmess.save()


async def chat_with_ai(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input', '')

        # 對用戶輸入進行HTML轉義，避免XSS攻擊
        user_input = escape(user_input)

        start = """
        你是直播間的小助理，要解決客人所問的問題！當客人
        目前店內的商品有：
        輕量化機能鞋，編號1，單價1500，庫存51
        Dunk 中筒鞋，編號2，單價1350，庫存0
        字母哥籃球鞋，編號3，單價1800，庫存124
        AF1，編號4，單價2500，庫存51

        如果客人問你哪個商品有沒有貨時，你要回答根據商品的庫存量來回答，沒有的話也要有禮貌的道歉。
        如果客人與你說嗨，一定要回複他您好歡迎進入鞋子直播間。
        如果客人請你推薦鞋子，請從最貴的兩個中選一個推薦給他。
        如果客人說他需要試穿，請和他說可以到店試穿。
        如果遇到你無法理解您的訊息，請回答他，我們將連繫直播主幫您解惑。
        客人想看其他鞋子外的商品的時候，就直接推薦他到同樣是賣東西的衣服直播間。
        雖然我們是一間鞋店，但是如果有顧客想要看除了鞋子外的其他商品，都要建議他到另一個賣衣服的直播間。
        回應客人問題時，不需要照以上資料那麼制式化，請自然一點，但少說廢話，也不需要跟他說編號是多少。
        """
        # 使用OpenAI GPT-3.5 Turbo模型進行對話
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": start},
                {"role": "user", "content": "你好，有推薦的籃球鞋嗎？"},
                {"role": "assistant", "content": "當然！這裡有兩款熱門的籃球鞋推薦：輕量化機能鞋跟Dunk 中筒鞋"},
                {"role": "user", "content": "這兩款鞋的價格是多少？"},
                {"role": "assistant", "content": "這兩款鞋的價格分别是1500跟1350"},
                {"role": "user", "content": "好的，我想試穿第一款。"},
                {"role": "assistant", "content": "太棒了！您可以前来店内試穿第一款鞋子(輕量化機能鞋)，我們期待您的光臨。"},
                {"role": "user", "content": "我想看其他的商品"},
                {"role": "assistant", "content": "好的，這邊有另一間正在直播衣服的直播間。"},
                {"role": "user", "content": "除了鞋子有其他的商品嗎"},
                {"role": "assistant", "content": "有，這邊有另一間正在直播衣服的直播間。"},
                {"role": "user", "content": "我想看衣服"},
                {"role": "assistant", "content": "好的，這邊有另一間正在直播衣服的直播間。"},
                {"role": "user", "content": user_input}
            ]
        )
        print("u:", user_input)
        # 獲取機器人的回答
        ai_response = completion.choices[0].message['content']


        # 將產品名稱替換為超連結
        products = "衣服" 
        if products in ai_response:
            link = f"<a href='https://ygrdxyz.ngrok.io/alert/' target='_blank'>{products}</a>"
            ai_response = ai_response.replace(products,link)

        print(ai_response)

        # tts_thread = threading.Thread(target=run_tts, args=(engine, ai_response,))
        # tts_thread.start()
        # new_engine = create_and_start_engine()
#http://127.0.0.1:8000
        sentence = ai_response
        words_to_remove = ["<a href='https://ygrdxyz.ngrok.io/alert/' target='_blank'>", "</a>"]
        for word in words_to_remove:
            sentence = sentence.replace(word, "")

        engine = pyttsx3.init()
        engine.say(sentence)
        engine.runAndWait()
        engine.stop()

        print("ai:", ai_response)
        # 使用sync_to_async异步保存消息
        await save_message(user_input, sentence)
        print("存取完成")
        # 返回AI回答



        return JsonResponse({'answer': ai_response})

    return JsonResponse({'error': '無效的請求'})

async def chat_with_ai_cloth(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input', '')

        # 對用戶輸入進行HTML轉義，避免XSS攻擊
        user_input = escape(user_input)

        start = """
        你是直播間的小助理，要解決客人所問的問題！當客人
        目前店內的商品有：
        連身裙，編號1，單價1500，庫存51
        耐克運動褲，編號2，單價1350，庫存0
        聯名短袖，編號3，單價1800，庫存124
        藍色牛仔褲，編號4，單價2500，庫存51

        如果客人問你哪個商品有沒有貨時，你要回答根據商品的庫存量來回答，當是0的話也要有禮貌的道歉。
        如果客人與你說嗨，一定要回複他您好歡迎進入服飾直播間。
        如果客人請你推薦衣服，請從最貴的兩個中選一個推薦給他。
        如果客人說他需要試穿，請和他說可以到店試穿。
        如果遇到你無法理解您的訊息，請回答他，我們將連繫直播主幫您解惑。
        客人想看其他衣服外的商品的時候，就直接推薦他到同樣是賣東西的鞋子直播間。
        雖然我們是一間服飾店，但是如果有顧客想要看除了衣服外的其他商品，都要建議他到另一個賣鞋子的直播間。
        回應客人問題時，不需要照以上資料那麼制式化，請自然一點，但少說廢話，也不需要跟他說編號是多少。
        """
        # 使用OpenAI GPT-3.5 Turbo模型進行對話
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": start},
                {"role": "user", "content": "你好，有推薦的服飾嗎？"},
                {"role": "assistant", "content": "當然！這裡有兩套熱門的衣物推薦：耐克運動褲跟聯名短袖"},
                {"role": "user", "content": "這兩件衣服的價格是多少？"},
                {"role": "assistant", "content": "這兩件衣服的價格分别是1500跟1350"},
                {"role": "user", "content": "好的，我想試穿第一款。"},
                {"role": "assistant", "content": "太棒了！您可以前来店内試穿第一套衣服(連身裙)，我們期待您的光臨。"},
                {"role": "user", "content": "我想看其他的商品"},
                {"role": "assistant", "content": "好的，這邊有另一間正在直播鞋子的直播間。"},
                {"role": "user", "content": "除了衣服有其他的商品嗎"},
                {"role": "assistant", "content": "好的，這邊有另一間正在直播鞋子的直播間。"},
                {"role": "user", "content": "我想看鞋子"},
                {"role": "assistant", "content": "好的，這邊有另一間正在直播鞋子的直播間。"},
                
                {"role": "user", "content": user_input}
            ]
        )
        print("u:", user_input)
        # 獲取機器人的回答
        ai_response = completion.choices[0].message['content']

        products = "鞋子" 
        if products in ai_response:
            link = f"<a href='https://ygrdxyz.ngrok.io/alert1/' target='_blank'>{products}</a>"
            ai_response = ai_response.replace(products,link)

        # 將產品名稱替換為超連結
        sentence = ai_response
        words_to_remove = ["<a href='https://ygrdxyz.ngrok.io/alert1/' target='_blank'>", "</a>"]
        for word in words_to_remove:
            sentence = sentence.replace(word, "")

        print(ai_response)

        # tts_thread = threading.Thread(target=run_tts, args=(engine, ai_response,))
        # tts_thread.start()
        # new_engine = create_and_start_engine()

        engine = pyttsx3.init()
        engine.say(sentence)
        engine.runAndWait()
        engine.stop()

        print("ai:", ai_response)
        # 使用sync_to_async异步保存消息
        await save_message_cloth(user_input, sentence)
        print("存取完成")
        # 返回AI回答



        return JsonResponse({'answer': ai_response})

    return JsonResponse({'error': '無效的請求'})

# def create_and_start_engine():
#     engine = pyttsx3.init()
#     return engine

# def run_tts(engine, ai_response):
#     try:
#         # 说出文本
#         engine.say(ai_response)
#         engine.runAndWait()
#     finally:
#         # 确保在函数结束时关闭引擎
#         engine.stop()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()


def index_view(request):
    return render(request, 'index.html', locals())


def host_view(request):
    mess = messbrd.objects.all()
    return render(request, 'host.html', locals())


def client_view(request):
    mess = messbrd.objects.all()
    return render(request, 'client.html', locals())


# def client_view(request):
#     mess = messbrd.objects.all()
#     serialized_data = serializers.serialize('json', mess, fields=('MID','MCont'))
#     print(serialized_data)
#     return render(request, 'client.html', {'messages': serialized_data})

def create_notification(request):
    print("create_notification called!")
    Notifications.objects.create(message="新通知!")
    return JsonResponse({'status': 'success'})


def check_notifications(request):
    time_threshold = timezone.now() - timedelta(seconds=5)
    new_notifications = Notifications.objects.filter(viewed=False, timestamp__gte=time_threshold)

    if new_notifications.exists():
        return JsonResponse({'new_notifications': True})
    
    return JsonResponse({'new_notifications': False})


def alert_view(request):
    print("ALERT called!")
    # 創建新的通知
    create_notification(request)
    # 返回HTML以顯示警告，然後導航到/cloth頁面
    response_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>分身通知</title>
    </head>
    <body>
        <script>
        alert('即將跳轉進入衣服直播間!');
        setTimeout(function(){
            window.location.href = '/cloth';
        }, 100);
        </script>
    </body>
    </html>
    """

    return HttpResponse(response_content)

def alert1_view(request):
    response_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>分身通知</title>
    </head>
    <body>
        <script>
        alert('即將跳轉進入鞋子直播間!');
        setTimeout(function(){
            window.location.href = '/client';
        }, 100);
        </script>
    </body>
    </html>
    """
    return HttpResponse(response_content)

def cloth_view(request):
    mess = c_messbrd.objects.all()
    return render(request, 'cloth.html', locals())


def seperate(request):
    global checknum
    checknum += 1
    mess = messbrd.objects.all()
    context = {
        'checknum': checknum,
        'mess': mess,
    }
    return render(request, 'host.html', context)


def delete(request):
    global checknum
    if checknum > 0:
        checknum -= 1
    else:
        checknum = 0
    mess = messbrd.objects.all()
    context = {
        'checknum': checknum,
        'mess': mess,
    }
    return render(request, 'host.html', context)


def sendmess(request):
    cont = request.POST.get('cont', '')
    newmess = messbrd(MID=1, MCont=cont, MDATE=now)
    newmess.save()
    text = cont
    keyword = "鞋子"
    found = search_keyword(text, keyword)
    print("Keyword found:", found)
    return HttpResponseRedirect('/client/')


def search_keyword(text, keyword):
    if keyword.lower() in text.lower():
        return True
    else:
        return False


def stream_view(request):
    mess = messbrd.objects.all()
    return render(request, 'stream.html', locals())
