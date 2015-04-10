from django.conf.urls import url, include
from rest_framework import routers
from chappapi.api import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^video/', views.VideoView.as_view())
]
