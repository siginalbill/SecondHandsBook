#-*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from BookTrade.models import USR
from BookTrade.models import BOOK
from BookTrade.models import USRIMG
#from django import forms
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
#@cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性

def regist (request):
    if request.method == 'POST':
        if request.session["CheckCode"] != request.POST['checkcode'].upper():
            return render_to_response('Regist.html',{'ErrorMessage': '验证码错误'})
        usrname = request.POST['usrname']
        if USR.objects.filter(Name = usrname):          
            return render_to_response('Regist.html',{'ErrorMessage': '该用户名已存在'})
        password = request.POST['password']
        telphone = request.POST['telphone']
        email = request.POST['email']
        stuid = request.POST['stuid']
        usrimg = request.FILES.get('img')
        p = USR.objects.create(Name = usrname,StuId = stuid,PassWord = password,Email = email,TelPhone = telphone)
        new_img = USRIMG(UsrID = p, UsrImg = usrimg)
        new_img.save()
        return HttpResponse('<a href="/login/">Success!</a>')
    else:
        
        return render(request,'Regist.html')

def login (request):
    if request.method == 'POST':
        rsp = {}
        if request.session["CheckCode"] != request.POST['checkcode'].upper():
            rsp['error'] = '验证码错误'
            return render(request,'Login.html',rsp)
        usrname = request.POST['usrname']
        password = request.POST['password']

        test = USR.objects.filter(Name = usrname,PassWord = password)
        
        if test:
#            rsp['usrname'] = usrname 
            request.session['usrname'] = test[0].Name
            request.session['usrid'] = test[0].USRId
#            return render(request,'Main.html',rsp)
            return HttpResponseRedirect('/main/')
        else :
            rsp['error'] = '账号或密码错误'  #.decode('gb2312').encode('utf-8')
            return render(request,'Login.html',rsp)
    else :
        rsp = {}
        rsp['error'] = ''  
        return render(request,'Login.html',rsp)

def logout (request):
    try:
        del request.session['usrid']
        del request.session['usrname']
    except ObjectDoesNotExist:
        pass
    return HttpResponse('You are logged out.<a href="/login/">重新登陆</a>')

def main (request):
    if request.method == 'GET':
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        test = ''
        try:
            test = USR.objects.filter(Name = usrname,USRId = usrid)
        except KeyError:
            pass
        rsp = {}
        if test:
            rsp['usrname'] = test.all()[0].Name
            imgflg = USRIMG.objects.filter(UsrID = test.all()[0])
            if imgflg:  
                rsp['usrimg'] = imgflg.all()[0].UsrImg
            else :
                rsp['usrimg'] = '/static/img/normal.jpg'
            return render(request,'Main.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error!')

def account (request):
    if request.method == 'GET':
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        test = ''
        try:
            test = USR.objects.filter(Name = usrname,USRId = usrid)
        except KeyError:
            pass
        rsp = {}
        if test:
            rsp['usrname'] = test[0].Name
            imgflg = USRIMG.objects.filter(UsrID = test[0])
            if imgflg:  
                rsp['usrimg'] = imgflg[0].UsrImg
            else :
                rsp['usrimg'] = '/static/img/normal.jpg'
            return render(request,'Myaccount.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error!')

def check_code(request):
    import io
    from . import check_code as CheckCode

    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code.upper()
    return HttpResponse(stream.getvalue())

    # 代码：生成一张图片，在图片中写文件
    # request.session['CheckCode'] =  图片上的内容

    # 自动生成图片，并且将图片中的文字保存在session中
    # 将图片内容返回给用户

def showdetails(request):
    if request.method == 'GET':
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        test = ''
        try:
            test = USR.objects.filter(Name = usrname,USRId = usrid)
        except KeyError:
            pass
        rsp = {}
        if test:
            rsp['usrname'] = test.all()[0].Name
            imgflg = USRIMG.objects.filter(UsrID = test.all()[0])
            if imgflg:  
                rsp['usrimg'] = imgflg.all()[0].UsrImg
            else :
                rsp['usrimg'] = '/static/img/normal.jpg'
            rsp['stuid'] = test[0].StuId
            rsp['email'] = test[0].Email
            rsp['telphone'] = test[0].TelPhone           
            return render(request,'Usr_Details.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error!')

     


       

