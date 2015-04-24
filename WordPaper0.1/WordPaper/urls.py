from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WordPaper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^home/', include('notes.urls')),
)
