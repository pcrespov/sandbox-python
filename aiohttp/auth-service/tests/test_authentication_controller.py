# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from auth.models.inline_response400 import InlineResponse400  # noqa: E501
from auth.models.registration_data import RegistrationData  # noqa: E501

from .utils import BaseTestCase


class TestAuthenticationController(BaseTestCase):
    """AuthenticationController integration test stubs"""

    def test_confirm_token_post(self):
        """Test case for confirm_token_post

        Confirms some operation by given user
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/confirm/{token}'.format(token='token_example'),
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        Logs client into the service
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/login',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_post(self):
        """Test case for logout_post

        
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/logout',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_me_get(self):
        """Test case for me_get

        Base entry-point for current API client's information
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/me',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_post(self):
        """Test case for register_post

        Registers new user
        """
        body = RegistrationData()
        response = self.client.open(
            '/pcrespov/test/1.0.0/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
