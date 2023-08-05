# coding: utf-8

"""
    Collibra Import API

    <p>The Import API is an efficient way to load large volumes of data into the Collibra Data Governance Center. The API can automatically differentiate between creating and updating data.</p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import collibra_importer
from collibra_importer.models.paged_response_import_error import PagedResponseImportError  # noqa: E501
from collibra_importer.rest import ApiException

class TestPagedResponseImportError(unittest.TestCase):
    """PagedResponseImportError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PagedResponseImportError
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_importer.models.paged_response_import_error.PagedResponseImportError()  # noqa: E501
        if include_optional :
            return PagedResponseImportError(
                total = 1000, 
                offset = 10, 
                limit = 100, 
                results = [
                    collibra_importer.models.import_error.ImportError(
                        error_type = 'VALIDATION', 
                        resource_type = 'COMMUNITY', 
                        error_message = '0', 
                        command = collibra_importer.models.import_command_reference.ImportCommandReference(
                            indices = [
                                56
                                ], 
                            identifier = '0', ), )
                    ]
            )
        else :
            return PagedResponseImportError(
        )

    def testPagedResponseImportError(self):
        """Test PagedResponseImportError"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
