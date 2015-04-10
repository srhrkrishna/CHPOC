from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.response import Response


class VideoView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        video_file = open('/home/ubuntu/files/test.mp4', 'rb')
        response = HttpResponse(FileWrapper(video_file), content_type='application/video')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'test1.mp4'
        return response

    def put(self, request, *args, **kwargs):
        return Response('',status=status.HTTP_201_CREATED)