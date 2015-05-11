import httplib
import base64
import zlib


class CustomRequest(object):
    def __init__(self, request_type, header_content, payload, full_path):
        self.request_type = request_type
        self.header_content = header_content
        self.payload = payload
        self.full_path = full_path

    def send_request(self):
        h = httplib.HTTPConnection("127.0.0.1:8000")
        # h = httplib.HTTPConnection("169.53.139.163")
        h.request(self.request_type, self.full_path, self.payload, self.header_content)
        return h.getresponse()


# Gateway Login
headersContent = {"Accept":"application/json"}
request_body = '{"ConsumerNumber":"sreehari.parameswaran@cognizant.com","SmartKey":"demo"}'

obj = CustomRequest('POST', headersContent, request_body, '/gateway/login/')
# print obj.send_request().msg
response = obj.send_request()
print response.read()
auth_token = response.msg['x-a12n']
# auth_token = 'adsfadsfs'
print 'auth_token: '+auth_token


# upload video
# headersContent = {"Content-Disposition": "attachment; filename=airhorse.avi", "Content-Type": "multipart/form-data",
#                   "x-a12n":auth_token, "x-ch-date-created":"5-4-2015", "x-ch-RDK_FW_VERSION_TAG2":"cartoon", "x-ch-sample-long-metadata": "This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information.This is a very very very very very very very very very very very very very very very very very very very long metadata information." }
#
# obj = CustomRequest('PUT', headersContent, open('/home/krishna/Documents/airhorse.avi', 'rb'), '/upload/')
# response = obj.send_request()
# print '---- Upload Video ----'
# print 'body: ' + str(response.read())
# print 'status: ' + str(response.status)

# # upload thumbnail
# headersContent = {"Content-Disposition": "attachment; filename=test.png", "Content-Type": "multipart/form-data",
#                   "x-a12n":auth_token, "x-ch-date-created":"4-20-2015"}
#
# obj = CustomRequest('PUT', headersContent, open('/home/krishna/Public/test.png', 'rb'), '/uploadthumbnail/')
# response = obj.send_request()
# print '---- Upload Thumbnail ----'
# print 'body: ' + str(response.read())
# print 'status: ' + str(response.status)
#
# Get Video
# headersContent = {"x-a12n":auth_token}
# obj = CustomRequest('GET', headersContent, '', '/video/CuteBaby.mp4')
# response = obj.send_request()
# response.read()
# print '---- Get Video ----'
# print response.status
# #
# # # Get Thumbnail
# # headersContent = {"x-a12n":auth_token, "filename":"test.png"}
# # obj = CustomRequest('GET', headersContent, '', '/thumbnail/')
# # response = obj.send_request()
# # print '---- Get Thumbnail ----'
# # print response.status
#
# # Get Metadata
headersContent = {"x-a12n":auth_token}
obj = CustomRequest('GET', headersContent, '', '/video/metadata/rdk20150506_074318.avi')
response = obj.send_request()
print '---- Get Video metadata ----'
print response.read()
#
# # Get List
# headersContent = {"x-a12n":auth_token}
# obj = CustomRequest('GET', headersContent, '', '/list/')
# response = obj.send_request()
# print response.status
# print str(response.read())

# curl -i -X PUT -S -H "Content-Disposition:attachment; filename=airhorse.avi" -H "x-a12n:267b938ad6e44c6cab7f135920700276" -T "/home/krishna/Documents/airhorse.avi" http://169.53.139.163/upload/

