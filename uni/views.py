from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from datetime import datetime, timezone, timedelta
from uni.models import *
#from myapp.models import *
# Create your views here.

now = datetime.datetime.now()
checknum = 0
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







