from __future__ import unicode_literals

from ImageStorage.storage import ImageStorage

from django.db import models

# Create your models here.

class USR (models.Model):
    USRId = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 30)
    StuId = models.BigIntegerField()
    PassWord = models.CharField(max_length = 32)
    Email = models.EmailField()
    TelPhone = models.CharField(max_length = 22)

class BOOK (models.Model):
    BookId = models.AutoField(primary_key = True)
    Owner = models.ForeignKey(USR, related_name='usr_book')
    BookName = models.CharField(max_length = 32)    
    BookAuthor = models.CharField(max_length = 32)
    BookBrief = models.CharField(max_length = 320)
    BookPublish = models.CharField(max_length = 32)
    BookPrice = models.FloatField(default = 0.0)
    BookSell = models.FloatField(default = 0.0)
    Wechat = models.CharField(max_length = 32, default = '无')
    TencentQQ = models.CharField(max_length = 22, default = '无')
    CallOthers = models.CharField(max_length = 32, default = '无')
    Lock = models.BooleanField(default = True)
    Live = models.BooleanField(default = True)

class TRADE (models.Model):
    TradeId = models.AutoField(primary_key = True)
    BuyerId = models.ForeignKey(USR, related_name='trade_usr')
    BookID = models.ForeignKey(BOOK, related_name='book_trade')
    TradeTime = models.DateField(auto_now_add = True)
    TradeBrief = models.CharField(max_length = 320, default='无')

class BOOKIMG (models.Model):
    BookID = models.ForeignKey(BOOK, related_name='book_img')
    BookImg = models.ImageField(upload_to='./img/%Y/%m/%d',storage=ImageStorage())

class USRIMG (models.Model):
    UsrID = models.ForeignKey(USR, related_name='usr_img')
    UsrImg = models.ImageField(upload_to='./img/%Y/%m/%d',storage=ImageStorage())

