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


class ChangeAssignmentRequest(object):
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
        'status_ids': 'list[str]',
        'characteristic_types': 'list[CharacteristicTypeAssignmentReference]',
        'articulation_rules': 'list[ArticulationRuleRequest]',
        'validation_rule_ids': 'list[str]',
        'data_quality_rule_ids': 'list[str]',
        'domain_type_ids': 'list[str]',
        'default_status_id': 'str',
        'scope_id': 'str'
    }

    attribute_map = {
        'status_ids': 'statusIds',
        'characteristic_types': 'characteristicTypes',
        'articulation_rules': 'articulationRules',
        'validation_rule_ids': 'validationRuleIds',
        'data_quality_rule_ids': 'dataQualityRuleIds',
        'domain_type_ids': 'domainTypeIds',
        'default_status_id': 'defaultStatusId',
        'scope_id': 'scopeId'
    }

    def __init__(self, status_ids=None, characteristic_types=None, articulation_rules=None, validation_rule_ids=None, data_quality_rule_ids=None, domain_type_ids=None, default_status_id=None, scope_id=None, local_vars_configuration=None):  # noqa: E501
        """ChangeAssignmentRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._status_ids = None
        self._characteristic_types = None
        self._articulation_rules = None
        self._validation_rule_ids = None
        self._data_quality_rule_ids = None
        self._domain_type_ids = None
        self._default_status_id = None
        self._scope_id = None
        self.discriminator = None

        if status_ids is not None:
            self.status_ids = status_ids
        if characteristic_types is not None:
            self.characteristic_types = characteristic_types
        if articulation_rules is not None:
            self.articulation_rules = articulation_rules
        if validation_rule_ids is not None:
            self.validation_rule_ids = validation_rule_ids
        if data_quality_rule_ids is not None:
            self.data_quality_rule_ids = data_quality_rule_ids
        if domain_type_ids is not None:
            self.domain_type_ids = domain_type_ids
        if default_status_id is not None:
            self.default_status_id = default_status_id
        if scope_id is not None:
            self.scope_id = scope_id

    @property
    def status_ids(self):
        """Gets the status_ids of this ChangeAssignmentRequest.  # noqa: E501

        The list of IDs of the statuses  # noqa: E501

        :return: The status_ids of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._status_ids

    @status_ids.setter
    def status_ids(self, status_ids):
        """Sets the status_ids of this ChangeAssignmentRequest.

        The list of IDs of the statuses  # noqa: E501

        :param status_ids: The status_ids of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[str]
        """

        self._status_ids = status_ids

    @property
    def characteristic_types(self):
        """Gets the characteristic_types of this ChangeAssignmentRequest.  # noqa: E501

        A list of references to characteristic types corresponding to the assignment.  When adding a 'relationTypeDirection' for a CharacteristicTypeAssignmentReference, all characteristicTypes that reference a RelationType must have the direction set.  # noqa: E501

        :return: The characteristic_types of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[CharacteristicTypeAssignmentReference]
        """
        return self._characteristic_types

    @characteristic_types.setter
    def characteristic_types(self, characteristic_types):
        """Sets the characteristic_types of this ChangeAssignmentRequest.

        A list of references to characteristic types corresponding to the assignment.  When adding a 'relationTypeDirection' for a CharacteristicTypeAssignmentReference, all characteristicTypes that reference a RelationType must have the direction set.  # noqa: E501

        :param characteristic_types: The characteristic_types of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[CharacteristicTypeAssignmentReference]
        """

        self._characteristic_types = characteristic_types

    @property
    def articulation_rules(self):
        """Gets the articulation_rules of this ChangeAssignmentRequest.  # noqa: E501

        The articulation rule definitions  # noqa: E501

        :return: The articulation_rules of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[ArticulationRuleRequest]
        """
        return self._articulation_rules

    @articulation_rules.setter
    def articulation_rules(self, articulation_rules):
        """Sets the articulation_rules of this ChangeAssignmentRequest.

        The articulation rule definitions  # noqa: E501

        :param articulation_rules: The articulation_rules of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[ArticulationRuleRequest]
        """

        self._articulation_rules = articulation_rules

    @property
    def validation_rule_ids(self):
        """Gets the validation_rule_ids of this ChangeAssignmentRequest.  # noqa: E501

        The list of IDs of the validation rules  # noqa: E501

        :return: The validation_rule_ids of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._validation_rule_ids

    @validation_rule_ids.setter
    def validation_rule_ids(self, validation_rule_ids):
        """Sets the validation_rule_ids of this ChangeAssignmentRequest.

        The list of IDs of the validation rules  # noqa: E501

        :param validation_rule_ids: The validation_rule_ids of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[str]
        """

        self._validation_rule_ids = validation_rule_ids

    @property
    def data_quality_rule_ids(self):
        """Gets the data_quality_rule_ids of this ChangeAssignmentRequest.  # noqa: E501

        The list of IDs of the data quality rules  # noqa: E501

        :return: The data_quality_rule_ids of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._data_quality_rule_ids

    @data_quality_rule_ids.setter
    def data_quality_rule_ids(self, data_quality_rule_ids):
        """Sets the data_quality_rule_ids of this ChangeAssignmentRequest.

        The list of IDs of the data quality rules  # noqa: E501

        :param data_quality_rule_ids: The data_quality_rule_ids of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[str]
        """

        self._data_quality_rule_ids = data_quality_rule_ids

    @property
    def domain_type_ids(self):
        """Gets the domain_type_ids of this ChangeAssignmentRequest.  # noqa: E501

        The list of IDs of the domain types  # noqa: E501

        :return: The domain_type_ids of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._domain_type_ids

    @domain_type_ids.setter
    def domain_type_ids(self, domain_type_ids):
        """Sets the domain_type_ids of this ChangeAssignmentRequest.

        The list of IDs of the domain types  # noqa: E501

        :param domain_type_ids: The domain_type_ids of this ChangeAssignmentRequest.  # noqa: E501
        :type: list[str]
        """

        self._domain_type_ids = domain_type_ids

    @property
    def default_status_id(self):
        """Gets the default_status_id of this ChangeAssignmentRequest.  # noqa: E501

        The ID of the default status for the asset type  # noqa: E501

        :return: The default_status_id of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: str
        """
        return self._default_status_id

    @default_status_id.setter
    def default_status_id(self, default_status_id):
        """Sets the default_status_id of this ChangeAssignmentRequest.

        The ID of the default status for the asset type  # noqa: E501

        :param default_status_id: The default_status_id of this ChangeAssignmentRequest.  # noqa: E501
        :type: str
        """

        self._default_status_id = default_status_id

    @property
    def scope_id(self):
        """Gets the scope_id of this ChangeAssignmentRequest.  # noqa: E501

        The ID of the scope the assignment corresponds to. The scopeId will be removed in the future.  # noqa: E501

        :return: The scope_id of this ChangeAssignmentRequest.  # noqa: E501
        :rtype: str
        """
        return self._scope_id

    @scope_id.setter
    def scope_id(self, scope_id):
        """Sets the scope_id of this ChangeAssignmentRequest.

        The ID of the scope the assignment corresponds to. The scopeId will be removed in the future.  # noqa: E501

        :param scope_id: The scope_id of this ChangeAssignmentRequest.  # noqa: E501
        :type: str
        """

        self._scope_id = scope_id

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
        if not isinstance(other, ChangeAssignmentRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeAssignmentRequest):
            return True

        return self.to_dict() != other.to_dict()
