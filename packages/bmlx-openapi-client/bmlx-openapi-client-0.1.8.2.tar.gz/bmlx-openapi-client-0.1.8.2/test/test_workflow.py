# coding: utf-8

"""
    bmlx api-server.

    Documentation of bmlx api-server apis. To find more info about generating spec from source, please refer to https://goswagger.io/use/spec.html  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import openapi_client
from openapi_client.models.workflow import Workflow  # noqa: E501
from openapi_client.rest import ApiException

class TestWorkflow(unittest.TestCase):
    """Workflow unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Workflow
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.workflow.Workflow()  # noqa: E501
        if include_optional :
            return Workflow(
                checksum = '0', 
                create_time = 56, 
                id = 56, 
                name = '0', 
                spec = '0', 
                uri = '0'
            )
        else :
            return Workflow(
        )

    def testWorkflow(self):
        """Test Workflow"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
