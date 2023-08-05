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


class RelationTraceEntryImpl(object):
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
        'out_bound_role_direction': 'bool',
        'role_direction': 'bool',
        'relation_type_id': 'str',
        'out_bound_relation_type_id': 'str'
    }

    attribute_map = {
        'out_bound_role_direction': 'outBoundRoleDirection',
        'role_direction': 'roleDirection',
        'relation_type_id': 'relationTypeId',
        'out_bound_relation_type_id': 'outBoundRelationTypeId'
    }

    def __init__(self, out_bound_role_direction=None, role_direction=None, relation_type_id=None, out_bound_relation_type_id=None, local_vars_configuration=None):  # noqa: E501
        """RelationTraceEntryImpl - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._out_bound_role_direction = None
        self._role_direction = None
        self._relation_type_id = None
        self._out_bound_relation_type_id = None
        self.discriminator = None

        if out_bound_role_direction is not None:
            self.out_bound_role_direction = out_bound_role_direction
        if role_direction is not None:
            self.role_direction = role_direction
        if relation_type_id is not None:
            self.relation_type_id = relation_type_id
        if out_bound_relation_type_id is not None:
            self.out_bound_relation_type_id = out_bound_relation_type_id

    @property
    def out_bound_role_direction(self):
        """Gets the out_bound_role_direction of this RelationTraceEntryImpl.  # noqa: E501

        Whether the outbound relation is followed in role direction.  # noqa: E501

        :return: The out_bound_role_direction of this RelationTraceEntryImpl.  # noqa: E501
        :rtype: bool
        """
        return self._out_bound_role_direction

    @out_bound_role_direction.setter
    def out_bound_role_direction(self, out_bound_role_direction):
        """Sets the out_bound_role_direction of this RelationTraceEntryImpl.

        Whether the outbound relation is followed in role direction.  # noqa: E501

        :param out_bound_role_direction: The out_bound_role_direction of this RelationTraceEntryImpl.  # noqa: E501
        :type: bool
        """

        self._out_bound_role_direction = out_bound_role_direction

    @property
    def role_direction(self):
        """Gets the role_direction of this RelationTraceEntryImpl.  # noqa: E501

        Whether the relation is followed in role direction, i.e. from source to target.  # noqa: E501

        :return: The role_direction of this RelationTraceEntryImpl.  # noqa: E501
        :rtype: bool
        """
        return self._role_direction

    @role_direction.setter
    def role_direction(self, role_direction):
        """Sets the role_direction of this RelationTraceEntryImpl.

        Whether the relation is followed in role direction, i.e. from source to target.  # noqa: E501

        :param role_direction: The role_direction of this RelationTraceEntryImpl.  # noqa: E501
        :type: bool
        """

        self._role_direction = role_direction

    @property
    def relation_type_id(self):
        """Gets the relation_type_id of this RelationTraceEntryImpl.  # noqa: E501

        The ID of the relation type.  # noqa: E501

        :return: The relation_type_id of this RelationTraceEntryImpl.  # noqa: E501
        :rtype: str
        """
        return self._relation_type_id

    @relation_type_id.setter
    def relation_type_id(self, relation_type_id):
        """Sets the relation_type_id of this RelationTraceEntryImpl.

        The ID of the relation type.  # noqa: E501

        :param relation_type_id: The relation_type_id of this RelationTraceEntryImpl.  # noqa: E501
        :type: str
        """

        self._relation_type_id = relation_type_id

    @property
    def out_bound_relation_type_id(self):
        """Gets the out_bound_relation_type_id of this RelationTraceEntryImpl.  # noqa: E501

        The ID of the outbound relation type.  # noqa: E501

        :return: The out_bound_relation_type_id of this RelationTraceEntryImpl.  # noqa: E501
        :rtype: str
        """
        return self._out_bound_relation_type_id

    @out_bound_relation_type_id.setter
    def out_bound_relation_type_id(self, out_bound_relation_type_id):
        """Sets the out_bound_relation_type_id of this RelationTraceEntryImpl.

        The ID of the outbound relation type.  # noqa: E501

        :param out_bound_relation_type_id: The out_bound_relation_type_id of this RelationTraceEntryImpl.  # noqa: E501
        :type: str
        """

        self._out_bound_relation_type_id = out_bound_relation_type_id

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
        if not isinstance(other, RelationTraceEntryImpl):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RelationTraceEntryImpl):
            return True

        return self.to_dict() != other.to_dict()
