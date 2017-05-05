#-*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
from BookTrade.models import USR
from BookTrade.models import USRIMG
from Chat.models import CHAT
from django.core.exceptions import ObjectDoesNotExist

def chat_view (request):
    if request.method == 'GET':
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        recvername = request.GET.get('recver_name')
        sender = ''
        try:
            sender = USR.objects.filter(Name = usrname,USRId = usrid)
        except KeyError:
            pass
        rsp = {} 
        if sender:              
            imgflg = USRIMG.objects.filter(UsrID = sender[0])
            if imgflg:  
                rsp['usrimg'] = imgflg.all()[0].UsrImg
            else :
                rsp['usrimg'] = '/static/img/normal.jpg'  
            rsp['usrname'] = usrname 
            rsp['recvername'] = recvername                
            return render(request,'Chat.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error!')

def chat_data (request):
    if request.method == 'GET':
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        sender = ''
        try:
            sender = USR.objects.filter(Name = usrname,USRId = usrid)
        except KeyError:
            pass
        rsp = []
        if sender:
            sender = sender[0]
            recver_name = request.GET.get('recver_name')
            try:
                recver = USR.objects.filter(Name = recver_name)
            except KeyError:
                return HttpResponse('Error2!')
            if not recver:
                return HttpResponse('Error3!')
            else:
                recver = recver[0]
            if USRIMG.objects.filter(UsrID = recver):
                recver_img = USRIMG.objects.filter(UsrID = recver)[0].UsrImg
            if USRIMG.objects.filter(UsrID = sender):
                sender_img = USRIMG.objects.filter(UsrID = sender)[0].UsrImg
            for m in CHAT.objects.order_by('-ChatTime').filter(Sender = sender, Recver = recver).all():
                dic = {'time':'','message':'','name':sender.Name,'img': str(sender_img)} 
                dic['time'] = m.ChatTime
                dic['message'] = m.Content
                rsp.append(dic)
            for m in CHAT.objects.order_by('-ChatTime').filter(Sender = recver, Recver = sender).all():
                dic = {'time':'','message':'','name':recver.Name,'img': str(recver_img),} 
                dic['time'] = m.ChatTime
                dic['message'] = m.Content
                rsp.append(dic)
            return JsonResponse(rsp, safe=False)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error1!')

def chat_post (request):
    if request.method == 'POST':    
        usrid = request.session.get('usrid')
        recver_name = request.POST['recver_name'] 
        message = request.POST['message']               
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return HttpResponse("DataError:In reading database. ")
        if usr_object:
            sender = usr_object[0]
            try:
                recver = USR.objects.filter(Name = recver_name)
            except KeyError:
                return JsonResponse({'error':'用户不存在1'}, safe=False)
            if recver:
                recver = recver[0]
            else:
                return JsonResponse({'error':'用户不存在2'}, safe=False)
            chat = CHAT.objects.create(Sender = sender,Recver = recver,Content = message)
            return JsonResponse({'error':''}, safe=False)
        else :
            return JsonResponse({'error':'请求失败'}, safe=False)