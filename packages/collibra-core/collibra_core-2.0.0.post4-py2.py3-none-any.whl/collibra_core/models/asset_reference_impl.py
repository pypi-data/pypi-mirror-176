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


class AssetReferenceImpl(object):
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
        'resource_type': 'str',
        'name': 'str',
        'display_name': 'str'
    }

    attribute_map = {
        'id': 'id',
        'resource_type': 'resourceType',
        'name': 'name',
        'display_name': 'displayName'
    }

    def __init__(self, id=None, resource_type=None, name=None, display_name=None, local_vars_configuration=None):  # noqa: E501
        """AssetReferenceImpl - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._resource_type = None
        self._name = None
        self._display_name = None
        self.discriminator = None

        self.id = id
        self.resource_type = resource_type
        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name

    @property
    def id(self):
        """Gets the id of this AssetReferenceImpl.  # noqa: E501

        The id of the referenced resource.  # noqa: E501

        :return: The id of this AssetReferenceImpl.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AssetReferenceImpl.

        The id of the referenced resource.  # noqa: E501

        :param id: The id of this AssetReferenceImpl.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def resource_type(self):
        """Gets the resource_type of this AssetReferenceImpl.  # noqa: E501

        The type of the resource, i.e. [Community, Asset, Domain, Attribute, Relation, WorkflowInstance].  # noqa: E501

        :return: The resource_type of this AssetReferenceImpl.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this AssetReferenceImpl.

        The type of the resource, i.e. [Community, Asset, Domain, Attribute, Relation, WorkflowInstance].  # noqa: E501

        :param resource_type: The resource_type of this AssetReferenceImpl.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and resource_type is None:  # noqa: E501
            raise ValueError("Invalid value for `resource_type`, must not be `None`")  # noqa: E501
        allowed_values = ["View", "Asset", "Community", "Domain", "AssetType", "DomainType", "Status", "User", "ClassificationMatch", "UserGroup", "Attribute", "StringAttribute", "ScriptAttribute", "BooleanAttribute", "DateAttribute", "NumericAttribute", "SingleValueListAttribute", "MultiValueListAttribute", "Comment", "Attachment", "Responsibility", "Workflow", "Job", "Relation", "RelationType", "ComplexRelation", "ComplexRelationType", "ArticulationRule", "Assignment", "Scope", "RelationTrace", "ValidationRule", "DataQualityRule", "DataQualityMetric", "Address", "InstantMessagingAccount", "Email", "PhoneNumber", "Website", "Activity", "FormProperty", "WorkflowTask", "ActivityChange", "WorkflowInstance", "Role", "AttributeType", "BooleanAttributeType", "DateAttributeType", "DateTimeAttributeType", "MultiValueListAttributeType", "NumericAttributeType", "ScriptAttributeType", "SingleValueListAttributeType", "StringAttributeType", "ViewSharingRule", "ViewAssignmentRule", "JdbcDriverFile", "JdbcDriver", "JdbcIngestionProperties", "CsvIngestionProperties", "ExcelIngestionProperties", "ConnectionStringParameter", "AssignedCharacteristicType", "Notification", "Tag", "ComplexRelationLegType", "ComplexRelationAttributeType", "ComplexRelationLeg", "BaseDataType", "AdvancedDataType", "DiagramPicture", "DiagramPictureSharingRule", "DiagramPictureAssignmentRule", "Rating", "Classification", "PhysicalDataConnector", "Context"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and resource_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `resource_type` ({0}), must be one of {1}"  # noqa: E501
                .format(resource_type, allowed_values)
            )

        self._resource_type = resource_type

    @property
    def name(self):
        """Gets the name of this AssetReferenceImpl.  # noqa: E501

        The name of the referenced resource.  # noqa: E501

        :return: The name of this AssetReferenceImpl.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AssetReferenceImpl.

        The name of the referenced resource.  # noqa: E501

        :param name: The name of this AssetReferenceImpl.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this AssetReferenceImpl.  # noqa: E501


        :return: The display_name of this AssetReferenceImpl.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this AssetReferenceImpl.


        :param display_name: The display_name of this AssetReferenceImpl.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

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
        if not isinstance(other, AssetReferenceImpl):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AssetReferenceImpl):
            return True

        return self.to_dict() != other.to_dict()
