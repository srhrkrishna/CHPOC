# ...
# imports
# ...
import json
import subprocess
import httplib
import os
import re
import os.path

from rest_framework import status
import keystoneclient.v2_0.client as ksclient


class VideoProcessor():
    auth_token = ''
    swift_ip = '23.246.246.66:8080'
    file_path = '/home/ubuntu/files/'

    def __init__(self):
        # ...
        # get auth-token
        # ...
        keystone = ksclient.Client(auth_url="http://23.246.246.66:5000/v2.0",
                                   username="sreehari.parameswaran@cognizant.com",
                                   password="demo",
                                   tenant_name="sreehari.parameswaran@cognizant.com")
        self.auth_token = keystone.auth_token

    def convert_to_mp4(self, file_name):
        # ...
        # convert to mp4
        # ...
        try:
            mp4_file_name = file_name.split('.')[0] + '.mp4'
        except:
            return 'Invalid file name'

        # Download video if not exists
        video_file_path = self.file_path + 'temp_' + file_name

        response_headers = ''
        if os.path.isfile(video_file_path) and os.access(video_file_path, os.R_OK):
            h = httplib.HTTPConnection(self.swift_ip)
            headers_content = {"X-Auth-Token": self.auth_token, "Accept": "application/json"}
            h.request('HEAD', '/swift/v1/Videos/' + file_name, '', headers_content)
            response = h.getresponse()
            if not response.status == status.HTTP_200_OK:
                h.close()
                return 'File not found'
            response_headers = response.getheaders()
            h.close()
        else:
            h = httplib.HTTPConnection(self.swift_ip)
            headers_content = {"X-Auth-Token": self.auth_token}
            h.request('GET', '/swift/v1/Videos/' + file_name, '', headers_content)
            response = h.getresponse()
            if not response.status == status.HTTP_200_OK:
                h.close()
                return 'File not found'
            destination = open(video_file_path, 'wb+')
            destination.write(response.read())
            destination.close()
            response_headers = response.getheaders()
            h.close()

        # Extract Metadata headers alone
        metadata = dict((header, value) for (header, value)
                        in response_headers if header.startswith('x-object-meta-'))

        # convert file format
        command = '/home/ubuntu/bin/ffmpeg -y -i %s -c:v libx264 -crf 19 -c:a aac -strict experimental -movflags +faststart %s%s' % (
            video_file_path, self.file_path, mp4_file_name)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        print p.returncode
        print p.stderr

        # Upload converted video
        h2 = httplib.HTTPConnection(self.swift_ip)
        headers_content2 = {"X-Auth-Token": self.auth_token}
        for header in metadata:
            headers_content2.update({header: metadata.get(header)})

        h2.request('PUT', '/swift/v1/Videos/' + mp4_file_name, open(video_file_path, 'rb'), headers_content2)
        response2 = h2.getresponse()

        if not response2.status == status.HTTP_201_CREATED:
            return 'File not uploaded'
        else:
            # Delete previous file
            h3 = httplib.HTTPConnection(self.swift_ip)
            headers_content3 = {"X-Auth-Token": self.auth_token, "Content-Type":"application/json"}
            h3.request('DELETE', '/swift/v1/Videos/' + file_name, '', headers_content3)
            response3 = h3.getresponse()
            if response3.status == status.HTTP_204_NO_CONTENT:
                return "Success"
            else:
                return "Old file not deleted"

    def convert_from_avi_to_mp4(self):
        # ...
        # Get list of .avi files and convert all to .mp4
        # ...
        h = httplib.HTTPConnection(self.swift_ip)
        headers_content = {"X-Auth-Token": self.auth_token, "Accept": "application/json"}
        h.request('GET', '/swift/v1/Videos?format=json', '', headers_content)
        response = h.getresponse()
        if response.status == status.HTTP_200_OK:
            obj = json.loads(response.read())
        else:
            return
        h.close()

        for item in obj:
            item_name = str(item['name'])
            if item_name.endswith('.avi'):
                mp4_file_name = self.convert_to_mp4(item_name)


VideoProcessor().convert_from_avi_to_mp4()