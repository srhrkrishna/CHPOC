from django.conf.urls import url, include
from rest_framework import routers
from chappapi.api import views

router = routers.DefaultRouter(trailing_slash=False)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    url(r'^docs/', include('rest_framework_swagger.urls')),
    # url(r'^video/$', views.VideoView.as_view()),
    url(r'^video/metadata/(?P<filename>.+)', views.MetadataView.as_view()),
    url(r'^video/(?P<filename>.+)/stream/(?P<authtoken>.+)', views.VideoStreamView.as_view()),
    url(r'^video/(?P<filename>.+)', views.VideoView.as_view()),
    url(r'^thumbnail/', views.ThumbnailView.as_view()),
    url(r'^gateway/login', views.GatewayView.as_view(), name='gateway-login'),
    url(r'^user/login', views.UserView.as_view(), name='user-login'),
    url(r'^list/', views.List.as_view()),
    url(r'^upload/', views.VideoUploadView.as_view()),
    url(r'^uploadthumbnail/', views.ThumbnailUploadView.as_view()),
    # url(r'^metadata', views.MetadataView.as_view())
]
