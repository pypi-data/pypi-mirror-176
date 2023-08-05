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


class ChangeAssetTypeAssignmentRuleRequest(object):
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
        'asset_type_id': 'str',
        'domain_id': 'str',
        'community_id': 'str',
        'status_id': 'str'
    }

    attribute_map = {
        'asset_type_id': 'assetTypeId',
        'domain_id': 'domainId',
        'community_id': 'communityId',
        'status_id': 'statusId'
    }

    def __init__(self, asset_type_id=None, domain_id=None, community_id=None, status_id=None, local_vars_configuration=None):  # noqa: E501
        """ChangeAssetTypeAssignmentRuleRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._asset_type_id = None
        self._domain_id = None
        self._community_id = None
        self._status_id = None
        self.discriminator = None

        self.asset_type_id = asset_type_id
        if domain_id is not None:
            self.domain_id = domain_id
        if community_id is not None:
            self.community_id = community_id
        if status_id is not None:
            self.status_id = status_id

    @property
    def asset_type_id(self):
        """Gets the asset_type_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501

        The ID of the asset type the changed rule should refer to.  # noqa: E501

        :return: The asset_type_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._asset_type_id

    @asset_type_id.setter
    def asset_type_id(self, asset_type_id):
        """Sets the asset_type_id of this ChangeAssetTypeAssignmentRuleRequest.

        The ID of the asset type the changed rule should refer to.  # noqa: E501

        :param asset_type_id: The asset_type_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and asset_type_id is None:  # noqa: E501
            raise ValueError("Invalid value for `asset_type_id`, must not be `None`")  # noqa: E501

        self._asset_type_id = asset_type_id

    @property
    def domain_id(self):
        """Gets the domain_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501

        The ID of the domain the assignment rule should apply for.  # noqa: E501

        :return: The domain_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id):
        """Sets the domain_id of this ChangeAssetTypeAssignmentRuleRequest.

        The ID of the domain the assignment rule should apply for.  # noqa: E501

        :param domain_id: The domain_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :type: str
        """

        self._domain_id = domain_id

    @property
    def community_id(self):
        """Gets the community_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501

        The ID of the community the assignment rule should apply for.  # noqa: E501

        :return: The community_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._community_id

    @community_id.setter
    def community_id(self, community_id):
        """Sets the community_id of this ChangeAssetTypeAssignmentRuleRequest.

        The ID of the community the assignment rule should apply for.  # noqa: E501

        :param community_id: The community_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :type: str
        """

        self._community_id = community_id

    @property
    def status_id(self):
        """Gets the status_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501

        The ID of the (Asset Type) status the assignment rule should apply for.  # noqa: E501

        :return: The status_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._status_id

    @status_id.setter
    def status_id(self, status_id):
        """Sets the status_id of this ChangeAssetTypeAssignmentRuleRequest.

        The ID of the (Asset Type) status the assignment rule should apply for.  # noqa: E501

        :param status_id: The status_id of this ChangeAssetTypeAssignmentRuleRequest.  # noqa: E501
        :type: str
        """

        self._status_id = status_id

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
        if not isinstance(other, ChangeAssetTypeAssignmentRuleRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeAssetTypeAssignmentRuleRequest):
            return True

        return self.to_dict() != other.to_dict()
