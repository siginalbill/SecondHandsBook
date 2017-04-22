"""SecondHandsBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static

from . import views
import settings

urlpatterns = [
    url(r'^book/',include('BookTrade.urls')),
    url(r'^admin/', admin.site.urls),
#    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL }),
    url(r'^login/$', views.login),
    url(r'^$',views.login),
    url(r'^regist/$',views.regist),
    url(r'^main/$',views.main),
    url(r'^logout/$',views.logout),
    url(r'^account/$',views.account),
    url(r'^check_code/$',views.check_code),
    url(r'^details/$', views.showdetails),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
