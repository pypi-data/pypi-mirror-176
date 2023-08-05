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
from collibra_importer.models.asset_identifier import AssetIdentifier  # noqa: E501
from collibra_importer.rest import ApiException

class TestAssetIdentifier(unittest.TestCase):
    """AssetIdentifier unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AssetIdentifier
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_importer.models.asset_identifier.AssetIdentifier()  # noqa: E501
        if include_optional :
            return AssetIdentifier(
                id = '0', 
                indexes = [
                    56
                    ], 
                external_system_id = '0', 
                external_entity_id = '0', 
                name = '0', 
                domain = collibra_importer.models.domain_identifier.DomainIdentifier(
                    id = '0', 
                    indexes = [
                        56
                        ], 
                    external_system_id = '0', 
                    external_entity_id = '0', 
                    name = '0', 
                    community = collibra_importer.models.community_identifier.CommunityIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        name = '0', ), )
            )
        else :
            return AssetIdentifier(
        )

    def testAssetIdentifier(self):
        """Test AssetIdentifier"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
