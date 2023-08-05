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


class ChangeAttributeRequest(object):
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
        'id': 'str',
        'value': 'object'
    }

    attribute_map = {
        'id': 'id',
        'value': 'value'
    }

    def __init__(self, id=None, value=None, local_vars_configuration=None):  # noqa: E501
        """ChangeAttributeRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._value = None
        self.discriminator = None

        self.id = id
        self.value = value

    @property
    def id(self):
        """Gets the id of this ChangeAttributeRequest.  # noqa: E501

        The ID of the attribute to be changed. Silently ignored if the ID is provided as path parameter of the request.  # noqa: E501

        :return: The id of this ChangeAttributeRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ChangeAttributeRequest.

        The ID of the attribute to be changed. Silently ignored if the ID is provided as path parameter of the request.  # noqa: E501

        :param id: The id of this ChangeAttributeRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def value(self):
        """Gets the value of this ChangeAttributeRequest.  # noqa: E501

        The value of this attribute. Expected type of the value depends on the type of the attribute.<br/>Following list presents type of the value depending on the kind of the attribute<br/><ul><br/><li> kind: Numeric               -> value type: number or string<br/><li> kind: Script                -> value type: string<br/><li> kind: Single Value List     -> value type: string<br/><li> kind: Date                  -> value type: number or string<br/><li> kind: String                -> value type: string<br/><li> kind: Boolean               -> value type: boolean or string<br/><li> kind: Multi Value List      -> value type: array of strings<br/></ul>  # noqa: E501

        :return: The value of this ChangeAttributeRequest.  # noqa: E501
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ChangeAttributeRequest.

        The value of this attribute. Expected type of the value depends on the type of the attribute.<br/>Following list presents type of the value depending on the kind of the attribute<br/><ul><br/><li> kind: Numeric               -> value type: number or string<br/><li> kind: Script                -> value type: string<br/><li> kind: Single Value List     -> value type: string<br/><li> kind: Date                  -> value type: number or string<br/><li> kind: String                -> value type: string<br/><li> kind: Boolean               -> value type: boolean or string<br/><li> kind: Multi Value List      -> value type: array of strings<br/></ul>  # noqa: E501

        :param value: The value of this ChangeAttributeRequest.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

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
        if not isinstance(other, ChangeAttributeRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeAttributeRequest):
            return True

        return self.to_dict() != other.to_dict()
