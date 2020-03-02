# -*- coding=utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from webapp.views import login_view,logout_view

from django.conf.urls import url
from webapp import views

urlpatterns = [

    url(r'^index/', views.index,name='index'),
    url(r'^$', views.index,name='index'),
    url(r'^register/', views.register,name='register'),
    url(r'^workmode/', views.workmode,name='workmode'),
    url(r'^usbfunction/', views.usbfunction,name='usbfunction'),
    url(r'^rpm/', views.rpm,name='rpm'),
    url(r'^pypackages/', views.pypackages,name='pypackages'),
    url(r'^aiapp/', views.aiapp,name='aiapp'),
    url(r'^password_setting/', views.password_setting,name='password_setting'),
    url(r'^network/', views.network,name='network'),
    url(r'^setmode/', views.setmode,name='setmode'),
    url(r'^reboot/', views.reboot,name='reboot'),
    url(r'^network_setting/(.*?)/$',views.network_setting,name='network_setting'),
    url(r'^isreboot/$',views.isreboot,name='isreboot'),
    url(r'^help/$',views.help,name='help'),
    url(r'^update_ajax/$',views.update_ajax,name='update_ajax'),
    url(r'^install_ajax/$',views.install_ajax,name='install_ajax'),
    url(r'^isupdate/$',views.isupdate,name='isupdate'),
    url(r'^restore_factory_settings/$',views.restore_factory_settings,name='restore_factory_settings'),
    url(r'^dhcp_setting/$',views.dhcp_setting,name='dhcp_setting'),
    #factorytest
    url(r'^factorytest/$',views.fttest,name='fttest'),
    url(r'^isrecovery/$',views.isrecovery,name='isrecovery'),
    url(r'^recovery/$',views.recovery,name='recovery'),
    url(r'^stress_test/$',views.stress_test,name='stress_test'),
    url(r'^page_ajax/$',views.page_ajax,name='page_ajax'),
    url(r'^read_ajax/$',views.read_ajax,name='read_ajax'),
]

