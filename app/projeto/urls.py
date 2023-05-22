"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.urls import re_path,path, include
from django.contrib import admin

from personal.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('contacts_login/', contacts_login_view, name='contacts_login'),
    path('contacts_logout/', contacts_logout_view, name='contacts_logout'),
    path('insert_temp/', insert_temp, name='insert_temp'),
    path('delete_temp/', delete_temp, name='delete_temp'),
    path('insert_desovas/', insert_desovas, name='insert_desovas'),
    path('delete_desova/', delete_desova, name='delete_desova'),
    path('ins_excel_desovas/', ins_excel_desovas, name='ins_excel_desovas'),
    path('ins_excel_temp/', ins_excel_temp, name='ins_excel_temp'),
    #path('teste/', teste, name='teste'),
    path('auth/', include("django.contrib.auth.urls"), name='auth'),
    path('transicoes/', transicoes, name='transicoes'),
    path('amostragens/', amostragens, name='amostragens'),
    path('insert_venda/', insert_venda, name='insert_venda'),
    path('comida/', comida, name='comida'),
    path('setup_jaula/', setup_jaula, name='setup_jaula'),
    path('dados_jaula/', dados_jaula, name='dados_jaula'),
    path('vacinados/', vacinados, name='vacinados'),
    path('alimentacao/', alimentacao, name='alimentacao'),
    path('delete_dados',delete_dados,name='delete_dados')
]
"""
re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', home_screen_view),
    re_path(r'^dashboard/', dashboard_view, name='dashboard'),
    re_path(r'^insert/', insert_view, name='insert'),
    re_path(r'^contacts/', contacts_view, name='contacts'),
"""
