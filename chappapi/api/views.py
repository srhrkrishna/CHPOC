# ...
# imports
# ...
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from urlparse import parse_qs
import base64
import keystoneclient.v2_0.client as ksclient
import httplib
import json
import re
import subprocess


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
            file_name = kwargs['filename']
            if not file_name:
                return Response('File name not provided', status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        if '___' in file_name:
            str_file_name = file_name.replace('___', '/')

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Videos/' + str_file_name, '', headers_content)
        response = h.getresponse()
        if not response.status == status.HTTP_200_OK:
            return Response(response.read(), response.status)
        destination = open('/home/ubuntu/files/temp_' + file_name, 'wb+')
        destination.write(response.read())
        destination.close()

        video_file = open('/home/ubuntu/files/temp_' + file_name, 'rb')

        obj = HttpResponse(FileWrapper(video_file), content_type='application/video', status=response.status)
        obj['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return obj


class VideoStreamView(views.APIView):
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
        temporary_filename = ''
        try:
            auth_token = kwargs['authtoken']
            file_name = kwargs['filename']
            temporary_filename = 'temp_' + file_name
            if not file_name:
                return Response('File name not provided', status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        if '___' in file_name:
            str_file_name = file_name.replace('___', '/')


        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Videos/' + str_file_name, '', headers_content)
        response = h.getresponse()
        if not response.status == status.HTTP_200_OK:
            return Response(response.read(), response.status)
        destination = open('/var/www/CHPOC/static/videos/' + temporary_filename, 'wb+')
        destination.write(response.read())
        destination.close()

        obj = HttpResponse('http://169.53.139.163/static/videos/' + temporary_filename, content_type='text/plain',
                           status=response.status)
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
        file_name = request.META.get('HTTP_FILENAME')
        if not file_name:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token}
        h.request('GET', '/swift/v1/Thumbnails/' + file_name, '', headers_content)
        response = h.getresponse()
        return HttpResponse(response.read(), response.status)


class VideoUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request):
        try:
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

            # Create Thumbnail
            thumbnail_name = up_file.name.split('.')[0] + '.jpeg'
            thumbnail_path = file_path + thumbnail_name

            command = '~/bin/ffmpeg -y -itsoffset -2  -i %s -vcodec mjpeg -vframes 1 -an -f rawvideo -s 320x240 %s' % \
                      (video_path, thumbnail_path)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.communicate()[0]

            metadata = dict((header, value) for (header, value)
                            in request.META.items() if header.startswith('HTTP_X_CH_'))
            headers_content = {"X-Auth-Token": auth_token}

            if thumbnail_name:
                headers_content["X-Object-Meta-Thumbnail"] = thumbnail_name
                if 'HTTP_X_CH_CAM_HARDWARE_ID' in metadata.keys() and 'HTTP_X_CH_CAM_SERIAL_NUM' in metadata.keys():
                    endpoint = '/swift/v1/Thumbnails/Camera_%s_%s/%s' % (
                        metadata['HTTP_X_CH_CAM_MANUFACTURER'],
                        metadata['HTTP_X_CH_CAM_SERIAL_NUM'],
                        thumbnail_name)
                else:
                    endpoint = '/swift/v1/Thumbnails/%s' % thumbnail_name

                h2 = httplib.HTTPConnection("23.246.246.66:8080")
                headers_content1 = {"X-Auth-Token": auth_token, "X-Object-Meta-VideoFileName": up_file.name}
                h2.request('PUT', endpoint, open(thumbnail_path, 'rb'),
                           headers_content1)

            # ...
            # store video and thumbnail in swift
            # ...

            for header in metadata:
                headers_content.update({'X-Object-Meta-' + header: metadata.get(header)})

            h = httplib.HTTPConnection("23.246.246.66:8080")
            h.request('PUT', '/swift/v1/Avis/' + up_file.name, open(video_path, 'rb'), headers_content)
            response = h.getresponse()
            return Response(response.read(), response.status)
        except:
            return Response('', status.HTTP_400_BAD_REQUEST)


class ThumbnailUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

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

            # ...
            # store thumbnail in swift
            # ...
            h = httplib.HTTPConnection("23.246.246.66:8080")
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
        try:
            pseudo_folder = request.META.get('HTTP_X_PSEUDO_FOLDER')
        except:
            pseudo_folder = ''
        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token, "Accept": "application/json"}
        h.request('GET', '/swift/v1/Videos?format=json', '', headers_content)
        response = h.getresponse()
        if not response.status == status.HTTP_200_OK:
            return Response(response.read(), response.status)
        obj = json.loads(response.read())
        h.close()
        # Get Pseudo-folder list
        if not pseudo_folder:
            folder_names = []
            for item in obj:
                video_name = item['name']
                if '/' in video_name:
                    pseudo_folder_name = video_name.split('/')[0]

                    if not len(folder_names) > 0:
                        folder_names.append({'name': pseudo_folder_name, 'count': 1})
                    else:
                        match_item = [element for element in folder_names if element['name'] == pseudo_folder_name]
                        if match_item:
                            match_item[0]['count'] += 1
                        else:
                            folder_names.append({'name': pseudo_folder_name, 'count': 1})

            return Response(folder_names, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})
        # Get only file names in given Pseudo-folder
        else:
            new_list = []
            for item in obj:
                video_name = item['name']
                if pseudo_folder in video_name:
                    image_name = video_name.split('/')[1].split('.')[0] + '.jpeg'
                    image_full_name = video_name.split('.')[0] + '.jpeg'
                else:
                    continue

                h1 = httplib.HTTPConnection("23.246.246.66:8080")
                headers_content_image = {"X-Auth-Token": auth_token}
                url = '/swift/v1/Thumbnails/' + image_full_name
                h1.request('GET', url, '', headers_content_image)
                response = h1.getresponse()
                thumbnail_output = response.read()
                thumbnail_status = response.status
                h1.close()

                if thumbnail_status == status.HTTP_404_NOT_FOUND:
                    item['thumbnail'] = 'Thumbnail not found'
                else:
                    temp_image_name = '/home/ubuntu/files/temp_{0}'.format(image_name)
                    with open(temp_image_name, 'wb+') as thumbnail_dest:
                        thumbnail_dest.write(thumbnail_output)
                    with open(temp_image_name, 'rb') as thumbnail_read:
                        item['thumbnail'] = base64.b64encode(thumbnail_read.read())
                item['name'] = video_name.split('/')[1]
                new_list.append(item)

            return Response(new_list, status=status.HTTP_200_OK, headers={"Content-Type": "application/json"})


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
            file_name = kwargs['filename']
            if not file_name:
                return Response('File name not provided', status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response('File name not provided', status.HTTP_400_BAD_REQUEST)

        # Get Headers
        h = httplib.HTTPConnection("23.246.246.66:8080")
        headers_content = {"X-Auth-Token": auth_token, "Accept": "application/json"}
        h.request('HEAD', '/swift/v1/Videos/' + file_name, '', headers_content)
        response = h.getresponse()
        response_headers = response.getheaders()
        if not response.status == status.HTTP_200_OK:
            return Response(response.read(), response.status)
        # Extract Metadata headers alone
        regex = re.compile('^x-object-meta-http-x-ch-')
        metadata = dict((regex.sub('', header), value) for (header, value)
                        in response_headers if header.startswith('x-object-meta-http-x-ch-'))

        modified_response_headers = []
        for header in metadata:
            modified_response_headers.append({"Key": header, "Value": metadata.get(header)})

        return Response(modified_response_headers, status=status.HTTP_200_OK,
                        headers={"Content-Type": "application/json"})
