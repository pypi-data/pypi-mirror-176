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


class ChangeScopeRequest(object):
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
        'domain_ids': 'list[str]',
        'community_ids': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'domain_ids': 'domainIds',
        'community_ids': 'communityIds'
    }

    def __init__(self, name=None, description=None, domain_ids=None, community_ids=None, local_vars_configuration=None):  # noqa: E501
        """ChangeScopeRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._domain_ids = None
        self._community_ids = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if domain_ids is not None:
            self.domain_ids = domain_ids
        if community_ids is not None:
            self.community_ids = community_ids

    @property
    def name(self):
        """Gets the name of this ChangeScopeRequest.  # noqa: E501

        The new name for the scope  # noqa: E501

        :return: The name of this ChangeScopeRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ChangeScopeRequest.

        The new name for the scope  # noqa: E501

        :param name: The name of this ChangeScopeRequest.  # noqa: E501
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
        """Gets the description of this ChangeScopeRequest.  # noqa: E501

        The new description for the scope  # noqa: E501

        :return: The description of this ChangeScopeRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ChangeScopeRequest.

        The new description for the scope  # noqa: E501

        :param description: The description of this ChangeScopeRequest.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 255):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    @property
    def domain_ids(self):
        """Gets the domain_ids of this ChangeScopeRequest.  # noqa: E501

        The new list of IDs of domains that should included in the scope  # noqa: E501

        :return: The domain_ids of this ChangeScopeRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._domain_ids

    @domain_ids.setter
    def domain_ids(self, domain_ids):
        """Sets the domain_ids of this ChangeScopeRequest.

        The new list of IDs of domains that should included in the scope  # noqa: E501

        :param domain_ids: The domain_ids of this ChangeScopeRequest.  # noqa: E501
        :type: list[str]
        """

        self._domain_ids = domain_ids

    @property
    def community_ids(self):
        """Gets the community_ids of this ChangeScopeRequest.  # noqa: E501

        The new list of IDs of communities that should included in the scope  # noqa: E501

        :return: The community_ids of this ChangeScopeRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._community_ids

    @community_ids.setter
    def community_ids(self, community_ids):
        """Sets the community_ids of this ChangeScopeRequest.

        The new list of IDs of communities that should included in the scope  # noqa: E501

        :param community_ids: The community_ids of this ChangeScopeRequest.  # noqa: E501
        :type: list[str]
        """

        self._community_ids = community_ids

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
        if not isinstance(other, ChangeScopeRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeScopeRequest):
            return True

        return self.to_dict() != other.to_dict()
