# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from auth.models.document import Document  # noqa: E501
from .utils import BaseTestCase


class TestDocumentsController(BaseTestCase):
    """DocumentsController integration test stubs"""

    def test_docs_doc_id_get(self):
        """Test case for docs_doc_id_get

        
        """
        response = self.client.open(
            '/pcrespov/test/1.0.0/docs/{doc_id}'.format(doc_id=1),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_document(self):
        """Test case for set_document

        
        """
        document = Document()
        response = self.client.open(
            '/pcrespov/test/1.0.0/docs/{doc_id}'.format(doc_id=1),
            method='POST',
            data=json.dumps(document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
