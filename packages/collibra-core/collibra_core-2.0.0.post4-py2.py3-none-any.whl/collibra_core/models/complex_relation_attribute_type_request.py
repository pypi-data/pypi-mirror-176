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


class ComplexRelationAttributeTypeRequest(object):
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
        'min': 'int',
        'max': 'int',
        'attribute_type_id': 'str',
        'id': 'str'
    }

    attribute_map = {
        'min': 'min',
        'max': 'max',
        'attribute_type_id': 'attributeTypeId',
        'id': 'id'
    }

    def __init__(self, min=None, max=None, attribute_type_id=None, id=None, local_vars_configuration=None):  # noqa: E501
        """ComplexRelationAttributeTypeRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._min = None
        self._max = None
        self._attribute_type_id = None
        self._id = None
        self.discriminator = None

        if min is not None:
            self.min = min
        if max is not None:
            self.max = max
        self.attribute_type_id = attribute_type_id
        if id is not None:
            self.id = id

    @property
    def min(self):
        """Gets the min of this ComplexRelationAttributeTypeRequest.  # noqa: E501

        The minimum number of Attribute Type occurrences.  # noqa: E501

        :return: The min of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :rtype: int
        """
        return self._min

    @min.setter
    def min(self, min):
        """Sets the min of this ComplexRelationAttributeTypeRequest.

        The minimum number of Attribute Type occurrences.  # noqa: E501

        :param min: The min of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :type: int
        """

        self._min = min

    @property
    def max(self):
        """Gets the max of this ComplexRelationAttributeTypeRequest.  # noqa: E501

        The maximum number of Attribute Type occurrences.  # noqa: E501

        :return: The max of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :rtype: int
        """
        return self._max

    @max.setter
    def max(self, max):
        """Sets the max of this ComplexRelationAttributeTypeRequest.

        The maximum number of Attribute Type occurrences.  # noqa: E501

        :param max: The max of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :type: int
        """

        self._max = max

    @property
    def attribute_type_id(self):
        """Gets the attribute_type_id of this ComplexRelationAttributeTypeRequest.  # noqa: E501

        The ID of the Attribute Type.  # noqa: E501

        :return: The attribute_type_id of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :rtype: str
        """
        return self._attribute_type_id

    @attribute_type_id.setter
    def attribute_type_id(self, attribute_type_id):
        """Sets the attribute_type_id of this ComplexRelationAttributeTypeRequest.

        The ID of the Attribute Type.  # noqa: E501

        :param attribute_type_id: The attribute_type_id of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and attribute_type_id is None:  # noqa: E501
            raise ValueError("Invalid value for `attribute_type_id`, must not be `None`")  # noqa: E501

        self._attribute_type_id = attribute_type_id

    @property
    def id(self):
        """Gets the id of this ComplexRelationAttributeTypeRequest.  # noqa: E501

        The ID of the Complex Relation Attribute Type. It will be created with this id or updated.<br/>If left empty on update the Complex Attribute Type will be recreated.  # noqa: E501

        :return: The id of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ComplexRelationAttributeTypeRequest.

        The ID of the Complex Relation Attribute Type. It will be created with this id or updated.<br/>If left empty on update the Complex Attribute Type will be recreated.  # noqa: E501

        :param id: The id of this ComplexRelationAttributeTypeRequest.  # noqa: E501
        :type: str
        """

        self._id = id

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
        if not isinstance(other, ComplexRelationAttributeTypeRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComplexRelationAttributeTypeRequest):
            return True

        return self.to_dict() != other.to_dict()
