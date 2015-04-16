# ...
# imports
# ...
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import zlib
import base64
import keystoneclient.v2_0.client as ksclient
import httplib
import json


class AuthToken(object):
    @staticmethod
    def get_auth_token(request):
        try:
            auth_token = request.META.get('HTTP_X_A12N')
            if not auth_token:
                return ''
            else:
                return auth_token
        except:
            return ''


class VideoView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            print auth_token
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)
        print auth_token
        file_name = request.META.get('HTTP_FILENAME')
        print file_name
        if not file_name:
            return Response('', status.HTTP_400_BAD_REQUEST)

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Videos/'+file_name, '', headers_content)
        response = h.getresponse()

        return HttpResponse(response.read(), status.HTTP_200_OK)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request):
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

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
        headers_content = {"X-Auth-Token": auth_token, "X-Object-Meta-Thumbnail": thumbnail_name}
        h.request('PUT', '/swift/v1/Videos/' + up_file.name, open(video_path, 'rb'), headers_content)

        h2 = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content1 = {"X-Auth-Token": auth_token, "X-Object-Meta-VideoFileName": up_file.name}
        h2.request('PUT', '/swift/v1/Thumbnails/' + thumbnail_name, open(thumbnail_path, 'rb'), headers_content1)
        # return Response('',status.HTTP_201_CREATED)
        return Response(up_file.name, status.HTTP_201_CREATED)


class UserView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            gateway_login = json.loads(request.body)

            if not gateway_login["ConsumerNumber"]:
                return Response('', status.HTTP_401_UNAUTHORIZED)

            if not gateway_login["Password"]:
                return Response('', status.HTTP_401_UNAUTHORIZED)
            else:
                password = gateway_login["Password"]
            # ...
            # get auth-token
            # ...
            keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                                       username=gateway_login["ConsumerNumber"],
                                       password=password,
                                       tenant_name="sreehari.parameswaran@cognizant.com")
            response = Response(data='{}', status=status.HTTP_202_ACCEPTED)
            response['x-a12n'] = keystone.auth_token
            return response
        except:
            return Response('', status.HTTP_401_UNAUTHORIZED)


class GatewayView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            gateway_login = json.loads(request.body)

            if not gateway_login["ConsumerNumber"]:
                return Response('', status.HTTP_401_UNAUTHORIZED)

            if not gateway_login["SmartKey"]:
                return Response('', status.HTTP_401_UNAUTHORIZED)
            else:
                password = gateway_login["SmartKey"]
            # ...
            # get auth-token
            # ...
            keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                                       username=gateway_login["ConsumerNumber"],
                                       password=password,
                                       tenant_name="sreehari.parameswaran@cognizant.com")
            response = Response(data='{}', status=status.HTTP_202_ACCEPTED)
            response['x-a12n'] = keystone.auth_token
            return response
        except:
            return Response('', status.HTTP_401_UNAUTHORIZED)


class List(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token, "Accept":"application/json"}
        h.request('GET', '/swift/v1/Videos?format=json', '', headers_content)
        response = h.getresponse()
        # print response.HTTP_CONTENT_TYPE
        obj = json.loads(response.read())
        return HttpResponse(obj, status=status.HTTP_200_OK)