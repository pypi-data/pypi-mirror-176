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
from collibra_core.models.dgc_session import DGCSession  # noqa: E501
from collibra_core.rest import ApiException

class TestDGCSession(unittest.TestCase):
    """DGCSession unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DGCSession
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_core.models.dgc_session.DGCSession()  # noqa: E501
        if include_optional :
            return DGCSession(
                csrf_token = '0', 
                user = collibra_core.models.user.User(
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
            )
        else :
            return DGCSession(
        )

    def testDGCSession(self):
        """Test DGCSession"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
