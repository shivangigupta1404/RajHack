from django.conf.urls import include, url
from . import views
from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    #url(r'a^$',views.index,name='index'),
    url(r'^$',views.log, name='log'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^authentication/$',views.login_next, name='login_next'),
    url(r'^home/$',views.transaction,name='home'),
    url(r'^log_end/$',views.log_end,name='logout'),
    ]
