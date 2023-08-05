# coding: utf-8

"""
    Collibra Data Governance Center Core API

    <p>The Core REST API allows you to create your own integrations with Collibra Data Governance Center.</p><p><i>Create custom applications to help users get access to the right data.</i></p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import collibra_core
from collibra_core.models.asset_assignment_rule_impl import AssetAssignmentRuleImpl  # noqa: E501
from collibra_core.rest import ApiException

class TestAssetAssignmentRuleImpl(unittest.TestCase):
    """AssetAssignmentRuleImpl unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AssetAssignmentRuleImpl
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_core.models.asset_assignment_rule_impl.AssetAssignmentRuleImpl()  # noqa: E501
        if include_optional :
            return AssetAssignmentRuleImpl(
                id = '0', 
                asset_type = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                    resource_type = 'Community', 
                    name = '0', ), 
                domain = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                    resource_type = 'Community', 
                    name = '0', ), 
                community = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                    resource_type = 'Community', 
                    name = '0', ), 
                status = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                    resource_type = 'Community', 
                    name = '0', )
            )
        else :
            return AssetAssignmentRuleImpl(
                id = '0',
        )

    def testAssetAssignmentRuleImpl(self):
        """Test AssetAssignmentRuleImpl"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
