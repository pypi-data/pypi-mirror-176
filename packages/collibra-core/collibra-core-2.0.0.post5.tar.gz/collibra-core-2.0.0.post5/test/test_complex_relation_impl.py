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
from collibra_core.models.complex_relation_impl import ComplexRelationImpl  # noqa: E501
from collibra_core.rest import ApiException

class TestComplexRelationImpl(unittest.TestCase):
    """ComplexRelationImpl unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ComplexRelationImpl
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_core.models.complex_relation_impl.ComplexRelationImpl()  # noqa: E501
        if include_optional :
            return ComplexRelationImpl(
                id = '0', 
                created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                created_on = 1475503010320, 
                last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                last_modified_on = 1476703764163, 
                system = True, 
                resource_type = 'View', 
                type = collibra_core.models.complex_relation_type_impl.ComplexRelationTypeImpl(
                    id = '0', 
                    created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                    created_on = 1475503010320, 
                    last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                    last_modified_on = 1476703764163, 
                    system = True, 
                    resource_type = 'View', 
                    name = 'Test name', 
                    description = 'Sample descripion of the resource.', 
                    symbol_data = collibra_core.models.symbol_data_impl.SymbolDataImpl(
                        color = '0', 
                        symbol_type = 'NONE', 
                        icon_code = '0', 
                        acronym_code = '0', ), 
                    attribute_types = [
                        collibra_core.models.complex_relation_attribute_type_impl.ComplexRelationAttributeTypeImpl(
                            id = '0', 
                            created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                            created_on = 1475503010320, 
                            last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                            last_modified_on = 1476703764163, 
                            system = True, 
                            resource_type = 'View', 
                            minimum_occurrences = 56, 
                            maximum_occurrences = 56, 
                            read_only = True, 
                            attribute_type = collibra_core.models.attribute_type.AttributeType(
                                description = 'Sample descripion of the resource.', 
                                name = 'Test name', 
                                created_on = 1475503010320, 
                                last_modified_on = 1476703764163, 
                                created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                system = True, 
                                id = '0', ), )
                        ], 
                    leg_types = [
                        collibra_core.models.complex_relation_leg_type_impl.ComplexRelationLegTypeImpl(
                            id = '0', 
                            created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                            created_on = 1475503010320, 
                            last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                            last_modified_on = 1476703764163, 
                            system = True, 
                            resource_type = 'View', 
                            minimum_occurrences = 56, 
                            maximum_occurrences = 56, 
                            asset_type = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                                id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                                resource_type = 'Community', 
                                name = '0', ), 
                            role = '0', 
                            co_role = '0', 
                            relation_type_id = '0', )
                        ], ), 
                legs = [
                    collibra_core.models.complex_relation_leg_impl.ComplexRelationLegImpl(
                        id = '0', 
                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                        created_on = 1475503010320, 
                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                        last_modified_on = 1476703764163, 
                        system = True, 
                        resource_type = 'View', 
                        asset_type = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', ), 
                        asset = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', ), 
                        asset_reference = collibra_core.models.asset_reference_impl.AssetReferenceImpl(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', 
                            display_name = '0', ), 
                        role = '0', 
                        co_role = '0', )
                    ], 
                attributes = [
                    collibra_core.models.attribute.Attribute(
                        asset = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', ), 
                        value = collibra_core.models.value.value(), 
                        type = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', ), 
                        created_on = 1475503010320, 
                        last_modified_on = 1476703764163, 
                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                        system = True, 
                        id = '0', )
                    ]
            )
        else :
            return ComplexRelationImpl(
                id = '0',
                resource_type = 'View',
        )

    def testComplexRelationImpl(self):
        """Test ComplexRelationImpl"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
