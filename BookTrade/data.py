#-*- coding: utf-8 -*-

from django.http import JsonResponse,HttpResponse
import json
from BookTrade.models import USR
from BookTrade.models import BOOK
from BookTrade.models import BOOKIMG
from BookTrade.models import TRADE

def ajax_newest(request):
    page = 0
    if (request.GET['page']):
        page = request.GET['page']
    rsp = []
    min = int(page)*22
    max = 22 + int(page)*22
    maxitems = BOOK.objects.filter(Lock = True, Live = True).count()
    if min<0:
        min = 0
    if max>maxitems:
        max = maxitems
#    print str(min)+' '+str(max)
    for item in BOOK.objects.order_by('-BookId').filter(Lock = True, Live = True)[min:max]:       
        dic = {'bookimg':'','bookname':'','bookauthor':'','bookauthor':'','bookbrief':''} 
        if (BOOKIMG.objects.filter(BookID = item)) :      
            dic['bookimg'] = str(BOOKIMG.objects.filter(BookID = item)[0].BookImg)
        else :
            dic['bookimg'] = ''
        dic['bookname'] = item.BookName
        dic['bookauthor'] = item.BookAuthor
        dic['bookpublish'] = item.BookPublish
        dic['bookbrief'] = item.BookBrief
        dic['bookid'] = item.BookId
        dic['booksell'] = item.BookSell
        dic['bookprice'] = item.BookPrice
        rsp.append(dic)
#        print item.BookName
#    all_jsons = json.dumps(rsp,ensure_ascii=False)
    return JsonResponse(rsp, safe=False)

def ajax_trade(request):
    if request.method == 'POST':
        rsp = {}
        if request.session["CheckCode"] != request.POST['checkcode'].upper():
            return JsonResponse({'error':'验证码错误'}, safe=False)
        usrid = request.session.get('usrid')
        bookid = request.POST['bookid']
        tradebrief = request.POST['tradebrief']        
        try:
            usr_object = USR.objects.filter(USRId = usrid)
            book_object = BOOK.objects.filter(BookId = bookid)
        except KeyError:
            return HttpResponse("DataError:In reading database. ")
        if usr_object and book_object :
            usr = usr_object[0]
            book = book_object[0]
            if (book.Lock and book.Live):
                trade = TRADE.objects.create(BuyerId = usr, BookID = book, TradeBrief = tradebrief)
#                book.objects.update(Lock = False)
                rsp['bookname'] = book.BookName
                rsp['booksell'] = book.BookSell
                rsp['tradetime'] = trade.TradeTime
                rsp['sellname'] = book.Owner.Name
                rsp['wechat'] = book.Wechat
                rsp['tencentqq'] = book.TencentQQ
                rsp['callothers'] = book.CallOthers
                rsp['tradebrief'] = trade.TradeBrief
                BOOK.objects.filter(BookId = book.BookId).update(Lock = False)
                return JsonResponse(rsp, safe=False)
            else:
                rsp['error'] = '该商品已被购买,请选择其他商品购买'
                return JsonResponse(rsp, safe=False)
        else :
            return JsonResponse({'error':'请求失败'}, safe=False)

def account_booksell (request):
    if request.method == 'GET':
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return HttpResponse("DataError:In reading database. ")
        booklist = usr_object[0].usr_book.all()
        rsp = []
        for item in booklist :
            dic = {}
            if (item.Live == False and item.Lock == False) :
                dic['status'] = 2 # 已售出
            if (item.Live == True and item.Lock == False) :
                dic['status'] = 1 # 已预定
            if (item.Lock and item.Live) :
                dic['status'] = 0 # 待售
            bookimg = BOOKIMG.objects.filter(BookID = item)
            if (bookimg):
                dic['bookimg'] = str(bookimg[0].BookImg)
            dic['bookname'] = item.BookName
            dic['bookid'] = item.BookId
            dic['booksell'] = item.BookSell
            if (dic['status']):
                trade = TRADE.objects.filter(BookID = item)[0]
                buyer = trade.BuyerId
                dic['tradetime'] = trade.TradeTime
                dic['tradebrief'] = trade.TradeBrief
                dic['buyername'] = buyer.Name
                rsp.append(dic)
            else :
                rsp.append(dic)
        return JsonResponse(rsp, safe=False)
    if (request.method == 'POST' and request.POST['method'] == 'refuse'):  ######refuse trade#######
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return JsonResponse({"status": False})
        if usr_object:
            usr = usr_object[0]
            bookid = request.POST['bookid']            
            if not (BOOK.objects.filter(Owner = usr, BookId = bookid)):
                return JsonResponse({"status": False})     
            book_objects = BOOK.objects.filter(BookId = bookid)
            book = book_objects[0]       
            if not (book.Live == True and book.Lock == False):
                return JsonResponse({"status": False})
            trade_object = TRADE.objects.filter(BookID = book)
            if trade_object:
                trades = trade_object[0]
                trades.delete()
                BOOK.objects.filter(BookId = bookid).update(Lock = True)
                return JsonResponse({"status": True})
            else :
                return JsonResponse({"status": False})
        else :
            return JsonResponse({"status": False})
    if (request.method == 'POST' and request.POST['method'] == 'makesure'):  ######make trade#######
        
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return JsonResponse({"status": False})
        if usr_object:
            usr = usr_object[0]
            bookid = request.POST['bookid']
            if not (BOOK.objects.filter(Owner = usr, BookId = bookid)):
                return JsonResponse({"status": False})                   
            book_objects = BOOK.objects.filter(BookId = bookid)
            book = book_objects[0]            
            if not (book.Live == True and book.Lock == False):
                return JsonResponse({"status": False})
            trade_object = TRADE.objects.filter(BookID = book)
            if trade_object:               
                BOOK.objects.filter(BookId = bookid).update(Live = False, Lock = False)
                return JsonResponse({"status": True})
            else :
                return JsonResponse({"status": False})
        else :
            return JsonResponse({"status": False})
    if (request.method == 'POST' and request.POST['method'] == 'delete'):  ######book delete#######
        
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return JsonResponse({"status": False})
        if usr_object:
            usr = usr_object[0]
            bookid = request.POST['bookid']
            if not (BOOK.objects.filter(Owner = usr, BookId = bookid)):
                return JsonResponse({"status": False})                   
            book_objects = BOOK.objects.filter(BookId = bookid)
            book = book_objects[0]            
            if not (book.Live == True and book.Lock == True):
                return JsonResponse({"status": False})
            trade_object = TRADE.objects.filter(BookID = book)
            if trade_object:               
                return JsonResponse({"status": False})
            else :
                book.delete()
                return JsonResponse({"status": True})
        else :
            return JsonResponse({"status": False})

def account_bookbuy (request):
    if request.method == 'GET':
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return HttpResponse("DataError:In reading database. ")
        tradelist = usr_object[0].trade_usr.all()
        rsp = []
        for t in tradelist :
            item = t.BookID
            dic = {}
            if (item.Live == False and item.Lock == False) :
                dic['status'] = 2 # 已售出
            if (item.Live == True and item.Lock == False) :
                dic['status'] = 1 # 已预定
            if (item.Lock and item.Live) :
                dic['status'] = 0 # 待售
            bookimg = BOOKIMG.objects.filter(BookID = item)
            if (bookimg):
                dic['bookimg'] = str(bookimg[0].BookImg)
            dic['bookname'] = item.BookName
            dic['bookid'] = item.BookId
            dic['booksell'] = item.BookSell
            dic['wechat'] = item.Wechat
            dic['tencentqq'] = item.TencentQQ
            dic['callothers'] = item.CallOthers
            if (dic['status']):
                seller = item.Owner
                dic['tradetime'] = t.TradeTime
                dic['tradebrief'] = t.TradeBrief
                dic['sellername'] = seller.Name
                rsp.append(dic)
            else :
                dic['tradetime'] = '异常数据请报告'
                dic['tradebrief'] = '异常数据请报告'
                dic['sellername'] = '异常数据请报告'
                rsp.append(dic)
        return JsonResponse(rsp, safe=False)
    if request.method == 'POST':
        usrid = request.session.get('usrid')
        try:
            usr_object = USR.objects.filter(USRId = usrid)
        except KeyError:
            return JsonResponse({"status": False})
        if usr_object:
            usr = usr_object[0]
            bookid = request.POST['bookid']
            book_objects = BOOK.objects.filter(BookId = bookid)
            book = book_objects[0]            
            if not (book.Live == True and book.Lock == False):
                return JsonResponse({"status": False})
            trade_object = TRADE.objects.filter(BuyerId = usr, BookID = book)
            if trade_object:
                trades = trade_object[0]
                trades.delete()
                BOOK.objects.filter(BookId = bookid).update(Lock = True)
                return JsonResponse({"status": True})
            else :
                return JsonResponse({"status": False})
        else :
            return JsonResponse({"status": False})

def search_data(request):
    searchstr = request.GET['searchstr']
    rsp = []
    for item in BOOK.objects.order_by('-BookId').filter(Lock = True, Live = True, BookName__contains=searchstr):       
        dic = {'bookimg':'','bookname':'','bookauthor':'','bookauthor':'','bookbrief':''} 
        if (BOOKIMG.objects.filter(BookID = item)) :      
            dic['bookimg'] = str(BOOKIMG.objects.filter(BookID = item)[0].BookImg)
        else :
            dic['bookimg'] = ''
        dic['bookname'] = item.BookName
        dic['bookauthor'] = item.BookAuthor
        dic['bookpublish'] = item.BookPublish
        dic['bookbrief'] = item.BookBrief
        dic['bookid'] = item.BookId
        dic['booksell'] = item.BookSell
        dic['bookprice'] = item.BookPrice
        rsp.append(dic)
#    all_jsons = json.dumps(rsp,ensure_ascii=False)
    return JsonResponse(rsp, safe=False)
            


