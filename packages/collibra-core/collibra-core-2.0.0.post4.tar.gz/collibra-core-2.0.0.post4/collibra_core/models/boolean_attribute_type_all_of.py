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


class BooleanAttributeTypeAllOf(object):
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
        'statistics_enabled': 'bool'
    }

    attribute_map = {
        'statistics_enabled': 'statisticsEnabled'
    }

    def __init__(self, statistics_enabled=None, local_vars_configuration=None):  # noqa: E501
        """BooleanAttributeTypeAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._statistics_enabled = None
        self.discriminator = None

        if statistics_enabled is not None:
            self.statistics_enabled = statistics_enabled

    @property
    def statistics_enabled(self):
        """Gets the statistics_enabled of this BooleanAttributeTypeAllOf.  # noqa: E501


        :return: The statistics_enabled of this BooleanAttributeTypeAllOf.  # noqa: E501
        :rtype: bool
        """
        return self._statistics_enabled

    @statistics_enabled.setter
    def statistics_enabled(self, statistics_enabled):
        """Sets the statistics_enabled of this BooleanAttributeTypeAllOf.


        :param statistics_enabled: The statistics_enabled of this BooleanAttributeTypeAllOf.  # noqa: E501
        :type: bool
        """

        self._statistics_enabled = statistics_enabled

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
        if not isinstance(other, BooleanAttributeTypeAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BooleanAttributeTypeAllOf):
            return True

        return self.to_dict() != other.to_dict()
