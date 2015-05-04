# ...
# imports
# ...
from wsgiref.util import FileWrapper
import datetime
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.decorators import detail_route
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from urlparse import parse_qs
import zlib
import base64
import keystoneclient.v2_0.client as ksclient
import httplib
import json
import re


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
    """
    Download Video file
    """
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        ---
        omit_serializer: true
        parameters:
            - name: filename
              paramType: path
            - name: x-a12n
              paramType: header
        """
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        try:
            parsed_query_string = parse_qs(request.GET.urlencode())
            # file_name = parsed_query_string.get('filename')[0]
            file_name = kwargs['filename']
            # print file_name
            if not file_name:
                return Response('File name not provided', status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Videos/'+file_name, '', headers_content)
        response = h.getresponse()
        # print file_name
        destination = open('/home/ubuntu/files/temp_' + file_name, 'wb+')
        destination.write(response.read())
        destination.close()

        video_file = open('/home/ubuntu/files/temp_' + file_name, 'rb')

        obj = HttpResponse(FileWrapper(video_file), content_type='application/video', status = response.status)
        obj['Content-Disposition'] = 'attachment; filename="%s"' % (file_name)
        return obj


class ThumbnailView(views.APIView):
    """
    Download Thumbnail file
    """
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        ---
        omit_serializer: true
        parameters:
            - name: filename
              paramType: header
            - name: x-a12n
              paramType: header
        """
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)
        # print auth_token
        file_name = request.META.get('HTTP_FILENAME')
        # print file_name
        if not file_name:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Thumbnails/'+file_name, '', headers_content)
        response = h.getresponse()
        return HttpResponse(response.read(), response.status)


class VideoUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request):
        try:
            logfile = open('/home/ubuntu/files/log.txt', 'wb+')
            auth_token = AuthToken.get_auth_token(request)
            if not auth_token:
                return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

            up_file = request.data.get('file', '')
            file_path = '/home/ubuntu/files/'
            video_path = file_path + up_file.name

            logfile.write('Video Upload started for %s: %s\n' % (up_file.name, str(datetime.datetime.utcnow().time())))

            # save video to local directory
            destination = open(video_path, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()
            logfile.write('Video Upload completed for %s: %s\n' % (up_file.name, str(datetime.datetime.utcnow().time())))

            # save thumbnail to local directory
            thumbnail = request.META.get('HTTP_THUMBNAIL')
            thumbnail_name = request.META.get('HTTP_THUMBNAILNAME')
            headers_content = {"X-Auth-Token": auth_token}

            if thumbnail and thumbnail_name:
                # print thumbnail_name
                str1 = zlib.decompress(base64.b64decode(thumbnail))
                thumbnail_path = file_path + thumbnail_name
                destination1 = open(thumbnail_path, 'wb+')
                destination1.write(str1)
                destination1.close()
                headers_content["X-Object-Meta-Thumbnail"] = thumbnail_name
                h2 = httplib.HTTPConnection("23.246.246.66:8080")
                headers_content1 = {"X-Auth-Token": auth_token, "X-Object-Meta-VideoFileName": up_file.name}
                h2.request('PUT', '/swift/v1/Thumbnails/' + thumbnail_name, open(thumbnail_path, 'rb'), headers_content1)

            logfile.write('Video Upload to swift started for %s: %s\n' % (up_file.name, str(datetime.datetime.utcnow().time())))
            # print up_file.name
            # ...
            # store video and thumbnail in swift
            # ...
            regex = re.compile('^HTTP__X_CH_')
            metadata = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_X_CH_'))

            for header in metadata:
                headers_content.update({'X-Object-Meta-' + header: metadata.get(header)})

            # print headers_content
            h = httplib.HTTPConnection("23.246.246.66:8080")
            h.request('PUT', '/swift/v1/Videos/' + up_file.name, open(video_path, 'rb'), headers_content)
            response = h.getresponse()
            logfile.write('Video Upload to swift completed for %s: %s\n' % (up_file.name, str(datetime.datetime.utcnow().time())))
            logfile.flush()
            logfile.close()
            return Response(response.read(), response.status)
        except:
            return Response('', status.HTTP_400_BAD_REQUEST)


class ThumbnailUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def put(self, request):
        try:
            auth_token = AuthToken.get_auth_token(request)
            if not auth_token:
                return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

            up_file = request.data.get('file', '')
            file_path = '/home/ubuntu/files/'
            thumbnail_path = file_path + up_file.name

            headers_content = {"X-Auth-Token": auth_token}

            # save video to local directory
            destination = open(thumbnail_path, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()

            # print up_file.name
            # ...
            # store thumbnail in swift
            # ...
            h = httplib.HTTPConnection("23.246.246.66:8080")
            # print up_file.name
            h.request('PUT', '/swift/v1/Thumbnails/' + up_file.name, open(thumbnail_path, 'rb'), headers_content)
            response = h.getresponse()
            return Response(response.read(), response.status)
        except:
            return Response('', status.HTTP_400_BAD_REQUEST)


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
        obj = json.loads(response.read())
        return Response(obj, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})


class MetadataView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        ---
        omit_serializer: true
        parameters:
            - name: filename
              paramType: path
            - name: x-a12n
              paramType: header
        """
        auth_token = AuthToken.get_auth_token(request)
        if not auth_token:
            return Response("Authentication token Invalid", status.HTTP_401_UNAUTHORIZED)

        # Get file name
        try:
            # parsed_query_string = parse_qs(request.GET.urlencode())
            # file_name = parsed_query_string.get('filename')[0]
            file_name = kwargs['filename']
            # print file_name
            if not file_name:
                return Response('File name not provided', status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        # Get Headers
        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token, "Accept":"application/json"}
        h.request('HEAD', '/swift/v1/Videos/' + file_name, '', headers_content)
        response = h.getresponse()
        response_headers = response.getheaders()

        # Extract Metadata headers alone
        regex = re.compile('^x-object-meta-http-x-ch-')
        metadata = dict((regex.sub('', header), value) for (header, value)
                        in response_headers if header.startswith('x-object-meta-http-x-ch-'))

        modified_response_headers = []
        for header in metadata:
            modified_response_headers.append({"Key": header, "Value": metadata.get(header)})
            # print header

        # obj = json.loads(response.read())
        return Response(modified_response_headers, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})