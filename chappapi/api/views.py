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
        return Response('', status=status.HTTP_201_CREATED)


class UserView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response = Response(data='{}', status=status.HTTP_202_ACCEPTED)
        response['x-a12n'] = '711722bf-1fb4-43e1-b23b-00c755aeeeab'
        return response


class List(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(data='{Links:[TestVideo1.mp4, Test2.mp4]}', status=status.HTTP_200_OK)