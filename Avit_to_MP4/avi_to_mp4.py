#!/usr/bin/python

# ...
# imports
# ...
import json
import subprocess
import httplib
import os
import os.path
import time
import logging
import logging.handlers
import argparse
import sys

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
                                   password="Admin1234$$",
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
            h.request('HEAD', '/swift/v1/Avis/' + file_name, '', headers_content)
            response = h.getresponse()
            if not response.status == status.HTTP_200_OK:
                h.close()
                return 'File not found'
            response_headers = response.getheaders()
            h.close()
        else:
            h = httplib.HTTPConnection(self.swift_ip)
            headers_content = {"X-Auth-Token": self.auth_token}
            h.request('GET', '/swift/v1/Avis/' + file_name, '', headers_content)
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
        command = '~/bin/ffmpeg -y -i %s -c:v libx264 -crf 19 -c:a aac -strict experimental -movflags +faststart %s%s' % (
            video_file_path, self.file_path, mp4_file_name)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]

        # Upload converted video
        try:
            h2 = httplib.HTTPConnection(self.swift_ip)
            headers_content2 = {"X-Auth-Token": self.auth_token}
            for header in metadata:
                headers_content2.update({header: metadata.get(header)})

            if 'x-object-meta-http-x-ch-cam-serial-num' in metadata.keys() and 'x-object-meta-http-x-ch-cam-hardware-id' in metadata.keys():
                endpoint = '/swift/v1/Videos/Camera_%s_%s/%s' % (
                metadata['x-object-meta-http-x-ch-cam-manufacturer'],
                metadata['x-object-meta-http-x-ch-cam-serial-num'],
                mp4_file_name)
            else:
                endpoint = '/swift/v1/Videos/%s' % mp4_file_name

            h2.request('PUT', endpoint, open(self.file_path + mp4_file_name, 'rb'), headers_content2)
            response2 = h2.getresponse()
        except Exception, e:
            return str(e)

        if not response2.status == status.HTTP_201_CREATED:
            return 'File not uploaded'
        else:
            # Delete previous file
            h3 = httplib.HTTPConnection(self.swift_ip)
            headers_content3 = {"X-Auth-Token": self.auth_token, "Content-Type": "application/json"}
            h3.request('DELETE', '/swift/v1/Avis/' + file_name, '', headers_content3)
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
        h.request('GET', '/swift/v1/Avis?format=json', '', headers_content)
        response = h.getresponse()
        output = response.read()
        if response.status == status.HTTP_200_OK:
            obj = json.loads(output)
        else:
            return
        h.close()

        for item in obj:
            item_name = str(item['name'])
            if item_name.endswith('.avi'):
                message = self.convert_to_mp4(item_name)
                print "%s : %s" % (item_name, message)

# Logging
LOG_FILENAME = "/tmp/avi_to_mp4.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
    LOG_FILENAME = args.log

# Configure logging to log to a file
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())


sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)


while True:
    VideoProcessor().convert_from_avi_to_mp4()
    time.sleep(10)
# VideoProcessor().convert_from_avi_to_mp4()
