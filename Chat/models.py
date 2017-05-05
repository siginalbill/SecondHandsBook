from __future__ import unicode_literals

from django.db import models
from BookTrade.models import USR

# Create your models here.

class CHAT (models.Model):
    Sender = models.ForeignKey(USR, related_name='chat1_usr')
    Recver = models.ForeignKey(USR, related_name='chat2_usr')
    Content = models.TextField()
    ChatTime = models.DateField(auto_now_add = True)
    manage = models.BooleanField(default = True)

    def __unicode__ (self):
        return u'%s' % self.Content