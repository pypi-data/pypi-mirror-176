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


class ConnectionStringParameter(object):
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
        'label': 'str',
        'parameter': 'str',
        'required': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'label': 'label',
        'parameter': 'parameter',
        'required': 'required'
    }

    def __init__(self, id=None, label=None, parameter=None, required=None, local_vars_configuration=None):  # noqa: E501
        """ConnectionStringParameter - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._label = None
        self._parameter = None
        self._required = None
        self.discriminator = None

        self.id = id
        self.label = label
        self.parameter = parameter
        if required is not None:
            self.required = required

    @property
    def id(self):
        """Gets the id of this ConnectionStringParameter.  # noqa: E501

        The id of the represented object (entity).  # noqa: E501

        :return: The id of this ConnectionStringParameter.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConnectionStringParameter.

        The id of the represented object (entity).  # noqa: E501

        :param id: The id of this ConnectionStringParameter.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def label(self):
        """Gets the label of this ConnectionStringParameter.  # noqa: E501


        :return: The label of this ConnectionStringParameter.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ConnectionStringParameter.


        :param label: The label of this ConnectionStringParameter.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and label is None:  # noqa: E501
            raise ValueError("Invalid value for `label`, must not be `None`")  # noqa: E501

        self._label = label

    @property
    def parameter(self):
        """Gets the parameter of this ConnectionStringParameter.  # noqa: E501


        :return: The parameter of this ConnectionStringParameter.  # noqa: E501
        :rtype: str
        """
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        """Sets the parameter of this ConnectionStringParameter.


        :param parameter: The parameter of this ConnectionStringParameter.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and parameter is None:  # noqa: E501
            raise ValueError("Invalid value for `parameter`, must not be `None`")  # noqa: E501

        self._parameter = parameter

    @property
    def required(self):
        """Gets the required of this ConnectionStringParameter.  # noqa: E501


        :return: The required of this ConnectionStringParameter.  # noqa: E501
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this ConnectionStringParameter.


        :param required: The required of this ConnectionStringParameter.  # noqa: E501
        :type: bool
        """

        self._required = required

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
        if not isinstance(other, ConnectionStringParameter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ConnectionStringParameter):
            return True

        return self.to_dict() != other.to_dict()
