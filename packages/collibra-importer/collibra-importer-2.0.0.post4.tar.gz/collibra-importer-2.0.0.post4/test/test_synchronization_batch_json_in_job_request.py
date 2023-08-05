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
from collibra_importer.models.synchronization_batch_json_in_job_request import SynchronizationBatchJsonInJobRequest  # noqa: E501
from collibra_importer.rest import ApiException

class TestSynchronizationBatchJsonInJobRequest(unittest.TestCase):
    """SynchronizationBatchJsonInJobRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SynchronizationBatchJsonInJobRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_importer.models.synchronization_batch_json_in_job_request.SynchronizationBatchJsonInJobRequest()  # noqa: E501
        if include_optional :
            return SynchronizationBatchJsonInJobRequest(
                send_notification = True, 
                batch_size = 1, 
                simulation = True, 
                save_result = True, 
                synchronization_id = '0', 
                file_id = '0', 
                file = bytes(b'blah'), 
                file_name = '0', 
                delete_file = True, 
                continue_on_error = True, 
                relations_action = 'a'
            )
        else :
            return SynchronizationBatchJsonInJobRequest(
                synchronization_id = '0',
        )

    def testSynchronizationBatchJsonInJobRequest(self):
        """Test SynchronizationBatchJsonInJobRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
