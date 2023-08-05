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
from collibra_core.models.paged_response_workflow_instance import PagedResponseWorkflowInstance  # noqa: E501
from collibra_core.rest import ApiException

class TestPagedResponseWorkflowInstance(unittest.TestCase):
    """PagedResponseWorkflowInstance unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PagedResponseWorkflowInstance
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_core.models.paged_response_workflow_instance.PagedResponseWorkflowInstance()  # noqa: E501
        if include_optional :
            return PagedResponseWorkflowInstance(
                total = 1000, 
                offset = 10, 
                limit = 100, 
                results = [
                    collibra_core.models.workflow_instance.WorkflowInstance(
                        id = '0', 
                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                        created_on = 1475503010320, 
                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                        last_modified_on = 1476703764163, 
                        system = True, 
                        resource_type = 'View', 
                        workflow_definition = collibra_core.models.workflow_definition_reference.WorkflowDefinitionReference(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', 
                            name = '0', 
                            process_id = '0', ), 
                        sub_instances = [
                            collibra_core.models.workflow_instance.WorkflowInstance(
                                id = '0', 
                                created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                created_on = 1475503010320, 
                                last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                last_modified_on = 1476703764163, 
                                system = True, 
                                resource_type = 'View', 
                                sub_process_instances_count = 56, 
                                parent_workflow_instance_id = '0', 
                                business_item = collibra_core.models.resource_reference.ResourceReference(
                                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                                    resource_type = 'Community', ), 
                                tasks = [
                                    collibra_core.models.workflow_task.WorkflowTask(
                                        id = '0', 
                                        system = True, 
                                        resource_type = 'View', 
                                        workflow_instance_id = '0', 
                                        key = '0', 
                                        type = '0', 
                                        aggregation_key = '0', 
                                        priority = 56, 
                                        owner = '0', 
                                        candidate_users = [
                                            collibra_core.models.user.User(
                                                id = '0', 
                                                created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                created_on = 1475503010320, 
                                                last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                last_modified_on = 1476703764163, 
                                                system = True, 
                                                resource_type = 'View', 
                                                user_name = '0', 
                                                first_name = '0', 
                                                last_name = '0', 
                                                email_address = '0', 
                                                gender = 'MALE', 
                                                language = '0', 
                                                additional_email_addresses = [
                                                    collibra_core.models.email.Email(
                                                        id = '0', 
                                                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                        created_on = 1475503010320, 
                                                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                        last_modified_on = 1476703764163, 
                                                        system = True, 
                                                        resource_type = 'View', 
                                                        email_address = '0', )
                                                    ], 
                                                phone_numbers = [
                                                    collibra_core.models.phone_number.PhoneNumber(
                                                        id = '0', 
                                                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                        created_on = 1475503010320, 
                                                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                        last_modified_on = 1476703764163, 
                                                        system = True, 
                                                        resource_type = 'View', 
                                                        type = 'FAX', 
                                                        phone_number = '0', )
                                                    ], 
                                                instant_messaging_accounts = [
                                                    collibra_core.models.instant_messaging_account.InstantMessagingAccount(
                                                        id = '0', 
                                                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                        created_on = 1475503010320, 
                                                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                        last_modified_on = 1476703764163, 
                                                        system = True, 
                                                        resource_type = 'View', 
                                                        account = '0', 
                                                        type = 'AOL', )
                                                    ], 
                                                websites = [
                                                    collibra_core.models.website.Website(
                                                        id = '0', 
                                                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                        created_on = 1475503010320, 
                                                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                        last_modified_on = 1476703764163, 
                                                        system = True, 
                                                        resource_type = 'View', 
                                                        url = '0', 
                                                        type = 'FACEBOOK', )
                                                    ], 
                                                addresses = [
                                                    collibra_core.models.address.Address(
                                                        id = '0', 
                                                        created_by = '4d250cc5-e583-4640-9874-b93d82c7a6cb', 
                                                        created_on = 1475503010320, 
                                                        last_modified_by = 'a073ff90-e7bc-4b35-ba90-c4d475f642fe', 
                                                        last_modified_on = 1476703764163, 
                                                        system = True, 
                                                        resource_type = 'View', 
                                                        city = '0', 
                                                        street = '0', 
                                                        number = '0', 
                                                        state = '0', 
                                                        country = '0', 
                                                        postal_code = '0', 
                                                        type = 'HOME', )
                                                    ], 
                                                activated = True, 
                                                enabled = True, 
                                                ldap_user = True, 
                                                user_source = 'INTERNAL', 
                                                guest_user = True, 
                                                api_user = True, 
                                                license_type = 'CONSUMER', )
                                            ], 
                                        create_time = 56, 
                                        due_date = 56, 
                                        cancelable = True, 
                                        reassignable = True, 
                                        form_required = True, 
                                        form_key_available = True, 
                                        contains_activity_stream = True, 
                                        in_error = True, 
                                        error_message = '0', 
                                        custom_buttons = [
                                            collibra_core.models.form_property.FormProperty(
                                                id = '0', 
                                                name = '0', 
                                                type = '0', 
                                                value = '0', 
                                                writable = True, 
                                                required = True, 
                                                enum_values = [
                                                    collibra_core.models.dropdown_value.DropdownValue(
                                                        parents = [
                                                            '0'
                                                            ], 
                                                        id_as_string = '0', 
                                                        id = '0', 
                                                        text = '0', )
                                                    ], 
                                                check_buttons = [
                                                    collibra_core.models.option_value.OptionValue(
                                                        label = '0', 
                                                        value = '0', )
                                                    ], 
                                                radio_buttons = [
                                                    collibra_core.models.option_value.OptionValue(
                                                        label = '0', 
                                                        value = '0', )
                                                    ], 
                                                default_dropdown_values = [
                                                    collibra_core.models.dropdown_value.DropdownValue(
                                                        id_as_string = '0', 
                                                        id = '0', 
                                                        text = '0', )
                                                    ], 
                                                proposed_dropdown_values = [
                                                    collibra_core.models.dropdown_value.DropdownValue(
                                                        id_as_string = '0', 
                                                        id = '0', 
                                                        text = '0', )
                                                    ], 
                                                date_time_type = '0', 
                                                multi_value = True, 
                                                proposed_fixed = True, 
                                                default_from_resource = True, 
                                                multi_default_dropdown_values = {
                                                    'key' : [
                                                        collibra_core.models.dropdown_value.DropdownValue(
                                                            id_as_string = '0', 
                                                            id = '0', 
                                                            text = '0', )
                                                        ]
                                                    }, 
                                                multi_proposed_dropdown_values = {
                                                    'key' : [
                                                        collibra_core.models.dropdown_value.DropdownValue(
                                                            id_as_string = '0', 
                                                            id = '0', 
                                                            text = '0', )
                                                        ]
                                                    }, 
                                                asset_type = collibra_core.models.resource_reference.ResourceReference(
                                                    id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                                                    resource_type = 'Community', ), 
                                                community_ids = [
                                                    '0'
                                                    ], 
                                                domain_ids = [
                                                    '0'
                                                    ], 
                                                status_ids = [
                                                    '0'
                                                    ], )
                                            ], 
                                        description = '0', 
                                        title = '0', 
                                        business_item_reference = collibra_core.models.named_resource_reference_impl.NamedResourceReferenceImpl(
                                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                                            resource_type = 'Community', 
                                            name = '0', ), )
                                    ], 
                                start_date = 56, 
                                ended = True, 
                                created_asset_id = '0', 
                                in_error = True, 
                                error_message = '0', )
                            ], 
                        sub_process_instances_count = 56, 
                        parent_workflow_instance_id = '0', 
                        business_item = collibra_core.models.resource_reference.ResourceReference(
                            id = '2b7f3a1a-4e50-4077-96f0-a58a395c860d', 
                            resource_type = 'Community', ), 
                        tasks = [
                            collibra_core.models.workflow_task.WorkflowTask(
                                id = '0', 
                                system = True, 
                                resource_type = 'View', 
                                workflow_instance_id = '0', 
                                key = '0', 
                                type = '0', 
                                aggregation_key = '0', 
                                priority = 56, 
                                owner = '0', 
                                create_time = 56, 
                                due_date = 56, 
                                cancelable = True, 
                                reassignable = True, 
                                form_required = True, 
                                form_key_available = True, 
                                contains_activity_stream = True, 
                                in_error = True, 
                                error_message = '0', 
                                description = '0', 
                                title = '0', )
                            ], 
                        start_date = 56, 
                        ended = True, 
                        created_asset_id = '0', 
                        in_error = True, 
                        error_message = '0', )
                    ]
            )
        else :
            return PagedResponseWorkflowInstance(
        )

    def testPagedResponseWorkflowInstance(self):
        """Test PagedResponseWorkflowInstance"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
