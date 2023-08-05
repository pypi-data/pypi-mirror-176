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


class ChangeMappingByExternalEntityRequest(object):
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
        'external_entity_url': 'str',
        'description': 'str',
        'mapped_resource_id': 'str',
        'last_sync_date': 'int',
        'sync_action': 'str'
    }

    attribute_map = {
        'external_entity_url': 'externalEntityUrl',
        'description': 'description',
        'mapped_resource_id': 'mappedResourceId',
        'last_sync_date': 'lastSyncDate',
        'sync_action': 'syncAction'
    }

    def __init__(self, external_entity_url=None, description=None, mapped_resource_id=None, last_sync_date=None, sync_action=None, local_vars_configuration=None):  # noqa: E501
        """ChangeMappingByExternalEntityRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._external_entity_url = None
        self._description = None
        self._mapped_resource_id = None
        self._last_sync_date = None
        self._sync_action = None
        self.discriminator = None

        if external_entity_url is not None:
            self.external_entity_url = external_entity_url
        if description is not None:
            self.description = description
        if mapped_resource_id is not None:
            self.mapped_resource_id = mapped_resource_id
        if last_sync_date is not None:
            self.last_sync_date = last_sync_date
        if sync_action is not None:
            self.sync_action = sync_action

    @property
    def external_entity_url(self):
        """Gets the external_entity_url of this ChangeMappingByExternalEntityRequest.  # noqa: E501

        The external URL of the mapped resource.  # noqa: E501

        :return: The external_entity_url of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._external_entity_url

    @external_entity_url.setter
    def external_entity_url(self, external_entity_url):
        """Sets the external_entity_url of this ChangeMappingByExternalEntityRequest.

        The external URL of the mapped resource.  # noqa: E501

        :param external_entity_url: The external_entity_url of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                external_entity_url is not None and len(external_entity_url) > 255):
            raise ValueError("Invalid value for `external_entity_url`, length must be less than or equal to `255`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                external_entity_url is not None and len(external_entity_url) < 1):
            raise ValueError("Invalid value for `external_entity_url`, length must be greater than or equal to `1`")  # noqa: E501

        self._external_entity_url = external_entity_url

    @property
    def description(self):
        """Gets the description of this ChangeMappingByExternalEntityRequest.  # noqa: E501

        The description of the mapped resource.  # noqa: E501

        :return: The description of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ChangeMappingByExternalEntityRequest.

        The description of the mapped resource.  # noqa: E501

        :param description: The description of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def mapped_resource_id(self):
        """Gets the mapped_resource_id of this ChangeMappingByExternalEntityRequest.  # noqa: E501

        The ID of the mapped resource.  # noqa: E501

        :return: The mapped_resource_id of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._mapped_resource_id

    @mapped_resource_id.setter
    def mapped_resource_id(self, mapped_resource_id):
        """Sets the mapped_resource_id of this ChangeMappingByExternalEntityRequest.

        The ID of the mapped resource.  # noqa: E501

        :param mapped_resource_id: The mapped_resource_id of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :type: str
        """

        self._mapped_resource_id = mapped_resource_id

    @property
    def last_sync_date(self):
        """Gets the last_sync_date of this ChangeMappingByExternalEntityRequest.  # noqa: E501

        The timestamp (in UTC time standard) of the last synchronization of mapped resource.  # noqa: E501

        :return: The last_sync_date of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :rtype: int
        """
        return self._last_sync_date

    @last_sync_date.setter
    def last_sync_date(self, last_sync_date):
        """Sets the last_sync_date of this ChangeMappingByExternalEntityRequest.

        The timestamp (in UTC time standard) of the last synchronization of mapped resource.  # noqa: E501

        :param last_sync_date: The last_sync_date of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :type: int
        """

        self._last_sync_date = last_sync_date

    @property
    def sync_action(self):
        """Gets the sync_action of this ChangeMappingByExternalEntityRequest.  # noqa: E501

        Represents the type of the action performed during last successful synchronization  # noqa: E501

        :return: The sync_action of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._sync_action

    @sync_action.setter
    def sync_action(self, sync_action):
        """Sets the sync_action of this ChangeMappingByExternalEntityRequest.

        Represents the type of the action performed during last successful synchronization  # noqa: E501

        :param sync_action: The sync_action of this ChangeMappingByExternalEntityRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["ADD", "UPDATE", "REMOVE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and sync_action not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `sync_action` ({0}), must be one of {1}"  # noqa: E501
                .format(sync_action, allowed_values)
            )

        self._sync_action = sync_action

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
        if not isinstance(other, ChangeMappingByExternalEntityRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeMappingByExternalEntityRequest):
            return True

        return self.to_dict() != other.to_dict()
