#-*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from BookTrade.models import USR
from BookTrade.models import BOOK
from BookTrade.models import BOOKIMG
from BookTrade.models import USRIMG
#from django import forms
from django.views.decorators.cache import cache_page

#@cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性

def add (request):
    if request.method == 'GET':
        rsp = {}
        try:
            usrname = request.session.get('usrname')
            usrid = request.session.get('usrid')
        except KeyError:
            return HttpResponse(KeyError)
        test = USR.objects.filter(Name = usrname,USRId = usrid)        
        if test:
            rsp['usrname'] = usrname
            rsp['Owner'] = ''
            return render(request,'Book_Sale.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        if request.session["CheckCode"] != request.POST['checkcode'].upper():
            return render(request,'Book_Sale.html',{'ErrorMessage': '验证码错误'})
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        test = USR.objects.filter(Name = usrname,USRId = usrid)
#        print '>>>>' + str(test.all()[0].USRId)
        if test:
                data = {}
#            try:
                
                data['usrname'] = usrname
                data['Owner'] = usrid
                data['BookName'] = request.POST['bookname']
                data['BookAuthor'] = request.POST['bookauthor']
                data['BookBrief'] = request.POST['bookbrief']
                data['BookPublish'] = request.POST['publish']
                data['BookSell'] = request.POST['booksell']
                data['BookPrice'] = request.POST['bookprice']
                data['WeChat'] = request.POST['wechat']
                data['TencentQQ'] = request.POST['tencentqq']
                data['CallOthers'] = request.POST['callothers']
                bookimg = request.FILES.get('img')
                p = BOOK.objects.create(Owner = test.all()[0], BookName = data['BookName'], BookAuthor = data['BookAuthor'], BookPublish = data['BookPublish'], BookBrief = data['BookBrief'],\
                    BookSell = data['BookSell'], BookPrice = data['BookPrice'], Wechat = data['WeChat'], TencentQQ = data['TencentQQ'], CallOthers = data['CallOthers'], )
                new_img = BOOKIMG(BookID = p, BookImg = bookimg)
                data['bookimg'] = new_img.BookImg
                new_img.save()
                return render(request,'Book_Sale.html',data)

#            except KeyError:
#                return HttpResponse('Error')
        else:
            return HttpResponseRedirect('/login/')

def details(request):
    if request.method == 'GET':
        bookid = request.GET.get('bookid')
        usrname = request.session.get('usrname')
        usrid = request.session.get('usrid')
        test = USR.objects.filter(Name = usrname,USRId = usrid)
        rsp = {}
        if test:
            rsp['usrname'] = test[0].Name
            imgflg = USRIMG.objects.filter(UsrID = test)
            if imgflg:  
                rsp['usrimg'] = '/media/' + str(imgflg[0].UsrImg)
            else :
                rsp['usrimg'] = '/static/img/normal.jpg'
            bookdet = BOOK.objects.filter(BookId = bookid)[0]            
            rsp['bookname'] = bookdet.BookName
            rsp['bookimg'] = '/media/' + str(BOOKIMG.objects.filter(BookID = bookdet)[0].BookImg)
            rsp['booksell'] = bookdet.BookSell
            rsp['bookprice'] = bookdet.BookPrice
            rsp['bookauthor'] = bookdet.BookAuthor
            rsp['bookpublish'] = bookdet.BookPublish
            rsp['bookbrief'] = bookdet.BookBrief
            rsp['wechat'] = bookdet.Wechat
            rsp['tencentqq'] = bookdet.TencentQQ
            rsp['callothers'] = bookdet.CallOthers
            seller = bookdet.Owner
            rsp['sellname'] = seller.Name
            rsp['bookid'] = bookid
#            rsp['sellimg'] =  USRIMG.objects.filter(UsrID = (USR.objects.filter(USRId = seller.USRId)))[0].UsrImg
            return render(request,'Book_Details.html',rsp)
        else :
            return HttpResponseRedirect('/login/')
    else :
         return HttpResponse('Error!')
