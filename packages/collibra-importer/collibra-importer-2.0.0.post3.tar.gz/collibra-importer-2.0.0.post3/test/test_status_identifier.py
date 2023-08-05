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
from collibra_importer.models.status_identifier import StatusIdentifier  # noqa: E501
from collibra_importer.rest import ApiException

class TestStatusIdentifier(unittest.TestCase):
    """StatusIdentifier unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test StatusIdentifier
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_importer.models.status_identifier.StatusIdentifier()  # noqa: E501
        if include_optional :
            return StatusIdentifier(
                id = '0', 
                indexes = [
                    56
                    ], 
                name = '0'
            )
        else :
            return StatusIdentifier(
        )

    def testStatusIdentifier(self):
        """Test StatusIdentifier"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
