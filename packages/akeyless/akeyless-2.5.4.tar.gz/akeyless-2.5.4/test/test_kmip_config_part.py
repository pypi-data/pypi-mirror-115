# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import akeyless
from akeyless.models.kmip_config_part import KMIPConfigPart  # noqa: E501
from akeyless.rest import ApiException

class TestKMIPConfigPart(unittest.TestCase):
    """KMIPConfigPart unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test KMIPConfigPart
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.kmip_config_part.KMIPConfigPart()  # noqa: E501
        if include_optional :
            return KMIPConfigPart(
                clients = {
                    'key' : akeyless.models.kmip_client.KMIPClient(
                        id = '0', 
                        name = '0', 
                        rules = [
                            akeyless.models.path_rule_is_a_single_rule_used_in_akeyless_rbac/.PathRule is a single rule used in AKEYLESS RBAC.(
                                capabilities = [
                                    '0'
                                    ], 
                                path = '0', 
                                type = '0', )
                            ], )
                    }, 
                server_enc = [
                    56
                    ]
            )
        else :
            return KMIPConfigPart(
        )

    def testKMIPConfigPart(self):
        """Test KMIPConfigPart"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
