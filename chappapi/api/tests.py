from django.test import TestCase
from views import *
import httplib


class CustomRequest(object):
    def __init__(self, request_type, header_content, payload, full_path):
        self.request_type = request_type
        self.header_content = header_content
        self.payload = payload
        self.full_path = full_path

    def send_request(self):
        # h = httplib.HTTPConnection("127.0.0.1:8000")
        h = httplib.HTTPConnection("169.53.139.163")
        h.request(self.request_type, self.full_path, self.payload, self.header_content)
        return h.getresponse()


# Create your tests here.
class ViewsTestCase(TestCase):
    def test_user_login_valid_credentials(self):
        headers_content = {"Accept": "application/json"}
        request_body = '{"ConsumerNumber":"sreehari.parameswaran@cognizant.com","Password":"demo"}'
        obj = CustomRequest('POST', headers_content, request_body, '/user/login/')
        response = obj.send_request()
        response.read()
        self.assertTrue('x-a12n' in response.msg)
        self.assertEqual(response.status, 202)

    def test_user_login_invalid_credentials(self):
        headers_content = {"Accept": "application/json"}
        request_body = '{"ConsumerNumber":"sreehari.parameswaran@cognizant.com","Password":"demo1"}'
        obj = CustomRequest('POST', headers_content, request_body, '/user/login/')
        # print obj.send_request().msg
        response = obj.send_request()
        response.read()
        self.assertFalse('x-a12n' in response.msg)
        self.assertEqual(response.status, 401)

    def test_gateway_login_valid_credentials(self):
        headers_content = {"Accept": "application/json"}
        request_body = '{"ConsumerNumber":"sreehari.parameswaran@cognizant.com","SmartKey":"demo"}'
        obj = CustomRequest('POST', headers_content, request_body, '/gateway/login/')
        # print obj.send_request().msg
        response = obj.send_request()
        response.read()
        self.assertTrue('x-a12n' in response.msg)
        self.assertEqual(response.status, 202)

    def test_gateway_login_invalid_credentials(self):
        headers_content = {"Accept": "application/json"}
        request_body = '{"ConsumerNumber":"sreehari.parameswaran@cognizant.com","SmartKey":"demo1"}'
        obj = CustomRequest('POST', headers_content, request_body, '/gateway/login/')
        # print obj.send_request().msg
        response = obj.send_request()
        response.read()
        self.assertFalse('x-a12n' in response.msg)
        self.assertEqual(response.status, 401)
