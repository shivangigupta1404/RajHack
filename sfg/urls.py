from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.log, name='log'),
    url(r'^authentication/$',views.login_next, name='login_next'),
    url(r'^log_end/$',views.log_end,name='logout'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^home/$',views.transaction,name='home'),
    ]
