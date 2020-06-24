from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream

# TBD I don't think this is needed but...
urlpatterns = [
    url(r'^api/v0/new-event-stream/(?P<city>\w+)', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'format-channels': ['{city}']}),
    url(r'', AsgiHandler),
]
