# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from .utils import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_root_get(self):
        """Test case for root_get

        Service health-check endpoint
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
