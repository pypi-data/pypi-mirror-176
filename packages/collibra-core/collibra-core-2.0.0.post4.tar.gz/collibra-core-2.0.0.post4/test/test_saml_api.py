# coding: utf-8

"""
    Collibra Data Governance Center Core API

    <p>The Core REST API allows you to create your own integrations with Collibra Data Governance Center.</p><p><i>Create custom applications to help users get access to the right data.</i></p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import collibra_core
from collibra_core.api.saml_api import SAMLApi  # noqa: E501
from collibra_core.rest import ApiException


class TestSAMLApi(unittest.TestCase):
    """SAMLApi unit test stubs"""

    def setUp(self):
        self.api = collibra_core.api.saml_api.SAMLApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_change_certificate(self):
        """Test case for change_certificate

        Changes the certificate to be used with SAML  # noqa: E501
        """
        pass

    def test_delete_customizations(self):
        """Test case for delete_customizations

        Delete the specified SAML certificate from the SAML keystore.  # noqa: E501
        """
        pass

    def test_get_sp_metadata_as_string(self):
        """Test case for get_sp_metadata_as_string

        Returns the SAML Service Provider metadata for this instance.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
