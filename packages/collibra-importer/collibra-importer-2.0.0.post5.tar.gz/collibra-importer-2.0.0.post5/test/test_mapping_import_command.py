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
from collibra_importer.models.mapping_import_command import MappingImportCommand  # noqa: E501
from collibra_importer.rest import ApiException

class TestMappingImportCommand(unittest.TestCase):
    """MappingImportCommand unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MappingImportCommand
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_importer.models.mapping_import_command.MappingImportCommand()  # noqa: E501
        if include_optional :
            return MappingImportCommand(
                identifier = collibra_importer.models.mapping_identifier.MappingIdentifier(
                    id = '0', 
                    indexes = [
                        56
                        ], 
                    external_system_id = '0', 
                    external_entity_id = '0', 
                    dgc_id = '0', 
                    asset = collibra_importer.models.asset_identifier.AssetIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        name = '0', 
                        domain = collibra_importer.models.domain_identifier.DomainIdentifier(
                            id = '0', 
                            external_system_id = '0', 
                            external_entity_id = '0', 
                            name = '0', 
                            community = collibra_importer.models.community_identifier.CommunityIdentifier(
                                id = '0', 
                                external_system_id = '0', 
                                external_entity_id = '0', 
                                name = '0', ), ), ), 
                    domain = collibra_importer.models.domain_identifier.DomainIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        name = '0', ), 
                    community = collibra_importer.models.community_identifier.CommunityIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        name = '0', ), 
                    complex_relation = collibra_importer.models.complex_relation_identifier.ComplexRelationIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        relations = {
                            'key' : [
                                collibra_importer.models.asset_identifier.AssetIdentifier(
                                    id = '0', 
                                    external_system_id = '0', 
                                    external_entity_id = '0', 
                                    name = '0', )
                                ]
                            }, ), ), 
                indexes = [
                    56
                    ], 
                external_system_id = '0', 
                external_entity_id = '0', 
                dgc_id = '0', 
                asset = collibra_importer.models.asset_identifier.AssetIdentifier(
                    id = '0', 
                    indexes = [
                        56
                        ], 
                    external_system_id = '0', 
                    external_entity_id = '0', 
                    name = '0', 
                    domain = collibra_importer.models.domain_identifier.DomainIdentifier(
                        id = '0', 
                        external_system_id = '0', 
                        external_entity_id = '0', 
                        name = '0', 
                        community = collibra_importer.models.community_identifier.CommunityIdentifier(
                            id = '0', 
                            external_system_id = '0', 
                            external_entity_id = '0', 
                            name = '0', ), ), ), 
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
                        name = '0', ), ), 
                community = collibra_importer.models.community_identifier.CommunityIdentifier(
                    id = '0', 
                    indexes = [
                        56
                        ], 
                    external_system_id = '0', 
                    external_entity_id = '0', 
                    name = '0', ), 
                complex_relation = collibra_importer.models.complex_relation_identifier.ComplexRelationIdentifier(
                    id = '0', 
                    indexes = [
                        56
                        ], 
                    external_system_id = '0', 
                    external_entity_id = '0', 
                    relations = {
                        'key' : [
                            collibra_importer.models.asset_identifier.AssetIdentifier(
                                id = '0', 
                                external_system_id = '0', 
                                external_entity_id = '0', 
                                name = '0', 
                                domain = collibra_importer.models.domain_identifier.DomainIdentifier(
                                    id = '0', 
                                    external_system_id = '0', 
                                    external_entity_id = '0', 
                                    name = '0', 
                                    community = collibra_importer.models.community_identifier.CommunityIdentifier(
                                        id = '0', 
                                        external_system_id = '0', 
                                        external_entity_id = '0', 
                                        name = '0', ), ), )
                            ]
                        }, ), 
                ext_entity_url = '0', 
                last_sync_date = 56, 
                sync_action = 'ADD', 
                description = '0', 
                resource_type = '0'
            )
        else :
            return MappingImportCommand(
        )

    def testMappingImportCommand(self):
        """Test MappingImportCommand"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
