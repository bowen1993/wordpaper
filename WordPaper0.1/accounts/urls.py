from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.indexView),
    url(r'^login', views.loginAction),
    url(r'^register', views.registerAction),
    url(r'^logout', views.logoutAction),
)