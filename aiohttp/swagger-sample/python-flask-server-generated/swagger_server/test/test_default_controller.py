# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.project_item import ProjectItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_project(self):
        """Test case for add_project

        adds a new project
        """
        projectItem = ProjectItem()
        response = self.client.open(
            '/pcrespov/test-simple/1.0.0/projects',
            method='POST',
            data=json.dumps(projectItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_projects_get(self):
        """Test case for projects_get

        searches projects
        """
        query_string = [('searchString', 'searchString_example')]
        response = self.client.open(
            '/pcrespov/test-simple/1.0.0/projects',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
