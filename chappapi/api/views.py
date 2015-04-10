from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views
from rest_framework.response import Response
from chappapi.api.serializers import cdx_compositesSerializer


class VideoView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # serializer = cdx_compositesSerializer(many=True)
        # if format == 'raw':
        video_file = open('/home/ubuntu/files/test.mp4', 'rb')
        response = HttpResponse(FileWrapper(video_file), content_type='application/video')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'test1.mp4'
        return response
        #
        # else:
        #     return Response(serializer.data)
