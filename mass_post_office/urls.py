from django.conf.urls import patterns, url, include
from .views import unsubscribe, unsubscribed

app_urlpatterns = patterns('',
    url(r'^unsubscribe/(?P<hashed>.*)/(?P<data>.*)/$', unsubscribe, name='unsubscribe'),
    url(r'^unsubscribe/complete/$', unsubscribed, name='unsubscribed'),
)

urlpatterns = patterns('',
    url(r'^', include(app_urlpatterns, namespace='mass_post_office')),
)