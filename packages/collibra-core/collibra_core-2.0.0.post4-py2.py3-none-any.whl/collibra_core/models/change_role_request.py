# coding: utf-8

"""
    Collibra Data Governance Center Core API

    <p>The Core REST API allows you to create your own integrations with Collibra Data Governance Center.</p><p><i>Create custom applications to help users get access to the right data.</i></p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from collibra_core.configuration import Configuration


class ChangeRoleRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'description': 'str',
        'permissions': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'permissions': 'permissions'
    }

    def __init__(self, name=None, description=None, permissions=None, local_vars_configuration=None):  # noqa: E501
        """ChangeRoleRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._permissions = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if permissions is not None:
            self.permissions = permissions

    @property
    def name(self):
        """Gets the name of this ChangeRoleRequest.  # noqa: E501

        The new name for the role. Should be unique within all roles.  # noqa: E501

        :return: The name of this ChangeRoleRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ChangeRoleRequest.

        The new name for the role. Should be unique within all roles.  # noqa: E501

        :param name: The name of this ChangeRoleRequest.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 255):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ChangeRoleRequest.  # noqa: E501

        The new description for the role.  # noqa: E501

        :return: The description of this ChangeRoleRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ChangeRoleRequest.

        The new description for the role.  # noqa: E501

        :param description: The description of this ChangeRoleRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def permissions(self):
        """Gets the permissions of this ChangeRoleRequest.  # noqa: E501

        The new permissions to be set. If null, no changes are made, otherwise the current permissions are<br/>replaced with the given ones.  # noqa: E501

        :return: The permissions of this ChangeRoleRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ChangeRoleRequest.

        The new permissions to be set. If null, no changes are made, otherwise the current permissions are<br/>replaced with the given ones.  # noqa: E501

        :param permissions: The permissions of this ChangeRoleRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["EDGE", "EDGE_SITE_CONNECT", "EDGE_SITE_MANAGE", "EDGE_SITE_ADMINISTER", "EDGE_INTEGRATION_CAPABILITY_MANAGE", "EDGE_VIEW_CONNECTIONS_AND_CAPABILITIES", "EDGE_VIEW_LOGS", "ASSET_GRID_ADMINISTRATION", "ATTACHMENT_ADD", "ATTACHMENT_CHANGE", "ATTACHMENT_REMOVE", "COMMENT_ADD", "COMMENT_CHANGE", "COMMENT_REMOVE", "RATING_ADD", "RATING_CHANGE", "RATING_REMOVE", "COMMUNITY_ADD", "COMMUNITY_CHANGE", "COMMUNITY_REMOVE", "COMMUNITY_CONFIGURE_EXTERNAL_SYSTEM", "COMMUNITY_RESPONSIBILITY_ADD", "COMMUNITY_RESPONSIBILITY_CHANGE", "COMMUNITY_RESPONSIBILITY_REMOVE", "DOMAIN_ADD", "DOMAIN_CHANGE", "DOMAIN_REMOVE", "DOMAIN_RESPONSIBILITY_ADD", "DOMAIN_RESPONSIBILITY_CHANGE", "DOMAIN_RESPONSIBILITY_REMOVE", "WORKFLOW_MANAGE", "WORKFLOW_DESIGNER_ACCESS", "ASSET_ADD", "ASSET_CHANGE", "ASSET_REMOVE", "ASSET_STATUS_CHANGE", "ASSET_TYPE_CHANGE", "ASSET_TAG_CHANGE", "ASSET_ATTRIBUTE_ADD", "ASSET_ATTRIBUTE_CHANGE", "ASSET_ATTRIBUTE_REMOVE", "ASSET_RESPONSIBILITY_ADD", "ASSET_RESPONSIBILITY_CHANGE", "ASSET_RESPONSIBILITY_REMOVE", "VIEW_PERMISSIONS_CHANGE", "BUSINESS_SEMANTICS_GLOSSARY", "REFERENCE_DATA_MANAGER", "DATA_STEWARDSHIP_MANAGER", "SYSTEM_ADMINISTRATION", "USER_ADMINISTRATION", "WORKFLOW_ADMINISTRATION", "DATA_HELPDESK", "POLICY_MANAGER", "DATA_DICTIONARY", "CATALOG", "WORKFLOW_MANAGE_ALL", "WORKFLOW_MESSAGE_EVENTS_USE", "VIEW_PERMISSIONS_VIEW_ALL", "VIEW_MANAGE", "VIEW_SHARE", "VIEW_MANAGE_ALL", "ADVANCED_DATA_TYPE_ADD", "ADVANCED_DATA_TYPE_EDIT", "ADVANCED_DATA_TYPE_REMOVE", "TAGS_VIEW", "TAGS_MANAGE", "VALIDATION_EXECUTION", "ACCESS_DATA", "VIEW_SAMPLES", "RELATION_TYPE_ADD", "RELATION_TYPE_REMOVE", "RELATION_TYPE_CHANGE", "REGISTER_PROFILING_INFORMATION", "REPORTING_DOWNLOAD_INSIGHTS_DATA", "REPORTING_VIEW_INSIGHTS_REPORTS", "INSIGHTS_VIEW", "INSIGHTS_SUMMARY", "TECHNICAL_LINEAGE", "LOGS_VIEW", "RESOURCE_MANAGE_ALL", "CONFIGURATION_VIEW", "CONFIGURATION_EDIT", "BACKSTORE_VIEW", "BACKSTORE_EDIT", "ASSESSMENTS", "METADATA_LAKE", "PROTECT", "PROTECT_EDIT", "PROTECT_ADMINISTRATION", "PRIVACY"]  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                not set(permissions).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `permissions` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(permissions) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._permissions = permissions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ChangeRoleRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeRoleRequest):
            return True

        return self.to_dict() != other.to_dict()
