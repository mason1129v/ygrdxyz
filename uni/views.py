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
# tracemalloc.start()
checknum = 0
from concurrent.futures import ThreadPoolExecutor

OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

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
        如果客人與你說嗨，一定要回複他您好歡迎進入直播間。
        如果客人請你推薦鞋子，請從最貴的兩個中選一個推薦給他。
        如果客人說他需要試穿，請和他說可以到店試穿。
        如果遇到你無法理解您的訊息，請回答他，我們將連繫直播主幫您解惑。
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
                {"role": "user", "content": user_input}
            ]
        )
        print("u:", user_input)
        # 獲取機器人的回答
        ai_response = completion.choices[0].message['content']
        
        # tts_thread = threading.Thread(target=run_tts, args=(engine, ai_response,))
        # tts_thread.start()
        # new_engine = create_and_start_engine()

        engine = pyttsx3.init()
        engine.say(ai_response)
        engine.runAndWait()
        engine.stop()

        print("ai:", ai_response)
        # 使用sync_to_async异步保存消息
        await save_message(user_input, ai_response)
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

def seperate(request):
    global checknum
    checknum += 1 
    mess = messbrd.objects.all()
    context = {
        'checknum' : checknum,
        'mess' : mess,
    }
    return render(request, 'host.html', context)

def delete(request):
    global checknum
    if checknum > 0 :
        checknum -= 1 
    else :
        checknum = 0 
    mess = messbrd.objects.all()
    context = {
        'checknum' : checknum,
        'mess' : mess,
    }
    return render(request, 'host.html', context)

def sendmess(request):
    cont = request.POST.get('cont', '')
    newmess = messbrd( MID = 1, MCont = cont, MDATE = now)
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







