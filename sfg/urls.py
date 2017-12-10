from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$',views.log, name='log'),
    url(r'^authentication/$',views.login_next, name='login_next'),
    url(r'^log_end/$',views.log_end,name='logout'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^home/$',views.apiAddBlock,name='home'),
    url(r'^dashboard/$',views.dashboard,name='dashboard'),
    #url(r'^upload/$',views.upload,name='upload'),
    ]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
