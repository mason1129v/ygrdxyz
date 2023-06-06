from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timezone, timedelta
from chat.models import *

# import random


# Create your views here.

names = ["PIN", "mason", "doris", "Hui"]

def lobby(request):
    return render(request, 'chat/lobby.html')

now = datetime.datetime.now()
checknum = 0

def index_view(request):
    return render(request, 'chat/index.html', locals())

def host_view(request):
    return render(request, 'chat/host.html', locals())

def sp_view(request):
    m = member.objects.get( MID = 3 )
    Member_id = m.MAC
    mess = messbrd.objects.all()
    keyword = request.GET.get('keyword') 
    h = keyword  
    productname = product.objects.get( PID = h )  
    print(h)
    print(productname)
    return render(request, 'chat/client_sp.html', locals())

def client_view(request):
    m = member.objects.get( MID = 3 )
    Member_id = m.MAC
    mess = messbrd.objects.all()
    return render(request, 'chat/client.html', locals())

def seperate(request):
    global checknum
    checknum += 1 
    mess = messbrd.objects.all()
    context = {
        'checknum' : checknum,
        'mess' : mess,
    }
    return render(request, 'chat/host.html', context)

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
    return render(request, 'chat/host.html', context)

# def sendmess(request):
#     cont = request.POST.get('cont', '')
#     newmess = messbrd( MID = 1, MCont = cont, MDATE = now)
#     newmess.save()
#     text = cont
#     keyword = "鞋子"
#     found = search_keyword(text, keyword)
#     print("Keyword found:", found) 
#     return HttpResponseRedirect('/client/')

def search_keyword(text, keyword):
    if keyword.lower() in text.lower():
        return True
    else:
        return False