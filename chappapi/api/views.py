from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import zlib
import base64
import keystoneclient.v2_0.client as ksclient
import httplib


class VideoView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):

        keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                           username="sreehari.parameswaran@cognizant.com",
                           password="GbU4ytu0",
                           tenant_name="sreehari.parameswaran@cognizant.com")

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": keystone.auth_token}
        h.request('GET', '/swift/v1/Test/test.mp4', '', headers_content)
        response = h.getresponse()
        #
        # print response.status
        # for header in response.getheaders():
        #     print header
        return  HttpResponse(response.read(), status.HTTP_200_OK)
        # video_file = open('/home/ubuntu/files/test.mp4', 'rb')
        # response = HttpResponse(FileWrapper(video_file), content_type='application/video')
        # response['Content-Disposition'] = 'attachment; filename="%s"' % 'test1.mp4'
        # return response


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request):
        
        # try:
        #     auth_token = request.META.get('HTTP_X_A12N')
        # except:
        #     return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                           username="sreehari.parameswaran@cognizant.com",
                           password="GbU4ytu0",
                           tenant_name="sreehari.parameswaran@cognizant.com")

        up_file = request.data.get('file', '')
        file_path = '/home/ubuntu/files/'
        video_path = file_path + up_file.name

        # save video to local directory
        destination = open(video_path, 'wb+')
        
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        # save thumbnail to local directory
        thumbnail = request.META.get('HTTP_THUMBNAIL')
        thumbnail_name = request.META.get('HTTP_THUMBNAILNAME')
        str1 = zlib.decompress(base64.b64decode(thumbnail))
        thumbnail_path = file_path + thumbnail_name
        destination1 = open(thumbnail_path, 'wb+')
        destination1.write(str1)
        destination1.close()

        # ...
        # store video and thumbnail in swift
        # ...
        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": keystone.auth_token, "X-Object-Meta-Thumbnail": thumbnail_name}
        h.request('PUT', '/swift/v1/Test/'+up_file.name, open(video_path, 'rb'), headers_content)

        h2 = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content1 = {"X-Auth-Token": keystone.auth_token, "X-Object-Meta-VideoFileName": up_file.name}
        h2.request('PUT', '/swift/v1/Test/'+thumbnail_name, open(thumbnail_path, 'rb'), headers_content1)

        return Response(up_file.name, status.HTTP_201_CREATED)



class UserView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # ...
        # get auth-token
        # ...
        keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                           username="sreehari.parameswaran@cognizant.com",
                           password="GbU4ytu0",
                           tenant_name="sreehari.parameswaran@cognizant.com")
        response = Response(data='{}', status=status.HTTP_202_ACCEPTED)
        response['x-a12n'] = keystone.auth_token
        return response


class List(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(data='{"Links":["TestVideo1.mp4", "Test2.mp4"]}', status=status.HTTP_200_OK)