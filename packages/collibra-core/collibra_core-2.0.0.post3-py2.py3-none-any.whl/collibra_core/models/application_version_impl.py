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


class ApplicationVersionImpl(object):
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
        'major': 'int',
        'minor': 'int',
        'full_version': 'str',
        'display_version': 'str'
    }

    attribute_map = {
        'major': 'major',
        'minor': 'minor',
        'full_version': 'fullVersion',
        'display_version': 'displayVersion'
    }

    def __init__(self, major=None, minor=None, full_version=None, display_version=None, local_vars_configuration=None):  # noqa: E501
        """ApplicationVersionImpl - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._major = None
        self._minor = None
        self._full_version = None
        self._display_version = None
        self.discriminator = None

        if major is not None:
            self.major = major
        if minor is not None:
            self.minor = minor
        if full_version is not None:
            self.full_version = full_version
        if display_version is not None:
            self.display_version = display_version

    @property
    def major(self):
        """Gets the major of this ApplicationVersionImpl.  # noqa: E501

        The major version number of the application version. This version number is increased with the major changes and releases of the application  # noqa: E501

        :return: The major of this ApplicationVersionImpl.  # noqa: E501
        :rtype: int
        """
        return self._major

    @major.setter
    def major(self, major):
        """Sets the major of this ApplicationVersionImpl.

        The major version number of the application version. This version number is increased with the major changes and releases of the application  # noqa: E501

        :param major: The major of this ApplicationVersionImpl.  # noqa: E501
        :type: int
        """

        self._major = major

    @property
    def minor(self):
        """Gets the minor of this ApplicationVersionImpl.  # noqa: E501

        The minor version number of the application version. This version number is increased whenever new features are added in given release  # noqa: E501

        :return: The minor of this ApplicationVersionImpl.  # noqa: E501
        :rtype: int
        """
        return self._minor

    @minor.setter
    def minor(self, minor):
        """Sets the minor of this ApplicationVersionImpl.

        The minor version number of the application version. This version number is increased whenever new features are added in given release  # noqa: E501

        :param minor: The minor of this ApplicationVersionImpl.  # noqa: E501
        :type: int
        """

        self._minor = minor

    @property
    def full_version(self):
        """Gets the full_version of this ApplicationVersionImpl.  # noqa: E501

        The full version of the application.  # noqa: E501

        :return: The full_version of this ApplicationVersionImpl.  # noqa: E501
        :rtype: str
        """
        return self._full_version

    @full_version.setter
    def full_version(self, full_version):
        """Sets the full_version of this ApplicationVersionImpl.

        The full version of the application.  # noqa: E501

        :param full_version: The full_version of this ApplicationVersionImpl.  # noqa: E501
        :type: str
        """

        self._full_version = full_version

    @property
    def display_version(self):
        """Gets the display_version of this ApplicationVersionImpl.  # noqa: E501

        The display version of the application. This is the version to be displayed to the customer and can be different from the actual internal version.  # noqa: E501

        :return: The display_version of this ApplicationVersionImpl.  # noqa: E501
        :rtype: str
        """
        return self._display_version

    @display_version.setter
    def display_version(self, display_version):
        """Sets the display_version of this ApplicationVersionImpl.

        The display version of the application. This is the version to be displayed to the customer and can be different from the actual internal version.  # noqa: E501

        :param display_version: The display_version of this ApplicationVersionImpl.  # noqa: E501
        :type: str
        """

        self._display_version = display_version

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
        if not isinstance(other, ApplicationVersionImpl):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApplicationVersionImpl):
            return True

        return self.to_dict() != other.to_dict()
