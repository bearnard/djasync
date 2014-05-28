from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'zootest.views.sync')
)
