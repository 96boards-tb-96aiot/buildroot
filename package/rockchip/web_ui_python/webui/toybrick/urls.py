# -*- coding=utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from webapp.views import login_view,logout_view,test_ajax,stress_ajax,reboot_ajax

urlpatterns = [
    # Examples:
    # url(r'^$', 'toybrick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login_view),
    url(r'^accounts/logout/$', logout_view),
    url(r'', include('webapp.urls',namespace='webapp')),
    url(r'^reboot_ajax/$', reboot_ajax),
    #factorytest
    url(r'^test_ajax/$', test_ajax),
    url(r'^stress_ajax/$', stress_ajax),
]
