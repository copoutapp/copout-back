from channels.routing import ProtocolTypeRouter, URLRouter
import map.routing

application = ProtocolTypeRouter({
    'http': URLRouter(map.routing.urlpatterns),
})