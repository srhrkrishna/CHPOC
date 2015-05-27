from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status


# Create your tests here.
class ViewsTestCase(APITestCase):
    def test_user_login_valid_credentials(self):
        url = reverse('user-login')
        request_body = {"ConsumerNumber":"sreehari.parameswaran@cognizant.com","Password":"demo"}
        response = self.client.post(url, request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, '{}')
        self.assertTrue('x-a12n' in response)

    def test_user_login_invalid_credentials(self):
        url = reverse('user-login')
        request_body = {"ConsumerNumber":"sreehari.parameswaran@cognizant.com","Password":"demo1"}
        response = self.client.post(url, request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('x-a12n' in response)

    def test_gateway_login_valid_credentials(self):
        url = reverse('gateway-login')
        request_body = {"ConsumerNumber":"sreehari.parameswaran@cognizant.com","SmartKey":"demo"}
        response = self.client.post(url, request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, '{}')
        self.assertTrue('x-a12n' in response)

    def test_gateway_login_invalid_credentials(self):
        url = reverse('gateway-login')
        request_body = {"ConsumerNumber":"sreehari.parameswaran@cognizant.com","SmartKey":"demo1"}
        response = self.client.post(url, request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('x-a12n' in response)


# curl -v -H 'X-Auth-Token: AUTH_tk59bf5e497bda4a298c06ba723cbad57d' http://127.0.0.1:8080/v1/AUTH_test