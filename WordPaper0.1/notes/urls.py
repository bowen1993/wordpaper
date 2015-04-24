from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from notes import views

urlpatterns = patterns('',
    url(r'^dashboard/', views.dashboardView),
    url(r'^addWord', views.addWordAction),
    url(r'^dayWord', views.getWordOfDay),
    url(r'^wordCount', views.getWordCount),
    url(r'^getWords', views.getWordsByOffset),
)