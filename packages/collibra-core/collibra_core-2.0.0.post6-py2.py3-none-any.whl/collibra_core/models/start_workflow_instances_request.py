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


class StartWorkflowInstancesRequest(object):
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
        'workflow_definition_id': 'str',
        'business_item_ids': 'list[str]',
        'business_item_type': 'str',
        'form_properties': 'dict(str, str)',
        'guest_user_id': 'str',
        'send_notification': 'bool'
    }

    attribute_map = {
        'workflow_definition_id': 'workflowDefinitionId',
        'business_item_ids': 'businessItemIds',
        'business_item_type': 'businessItemType',
        'form_properties': 'formProperties',
        'guest_user_id': 'guestUserId',
        'send_notification': 'sendNotification'
    }

    def __init__(self, workflow_definition_id=None, business_item_ids=None, business_item_type=None, form_properties=None, guest_user_id=None, send_notification=None, local_vars_configuration=None):  # noqa: E501
        """StartWorkflowInstancesRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._workflow_definition_id = None
        self._business_item_ids = None
        self._business_item_type = None
        self._form_properties = None
        self._guest_user_id = None
        self._send_notification = None
        self.discriminator = None

        self.workflow_definition_id = workflow_definition_id
        if business_item_ids is not None:
            self.business_item_ids = business_item_ids
        if business_item_type is not None:
            self.business_item_type = business_item_type
        if form_properties is not None:
            self.form_properties = form_properties
        if guest_user_id is not None:
            self.guest_user_id = guest_user_id
        if send_notification is not None:
            self.send_notification = send_notification

    @property
    def workflow_definition_id(self):
        """Gets the workflow_definition_id of this StartWorkflowInstancesRequest.  # noqa: E501

        The ID of the workflow definition.  # noqa: E501

        :return: The workflow_definition_id of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._workflow_definition_id

    @workflow_definition_id.setter
    def workflow_definition_id(self, workflow_definition_id):
        """Sets the workflow_definition_id of this StartWorkflowInstancesRequest.

        The ID of the workflow definition.  # noqa: E501

        :param workflow_definition_id: The workflow_definition_id of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and workflow_definition_id is None:  # noqa: E501
            raise ValueError("Invalid value for `workflow_definition_id`, must not be `None`")  # noqa: E501

        self._workflow_definition_id = workflow_definition_id

    @property
    def business_item_ids(self):
        """Gets the business_item_ids of this StartWorkflowInstancesRequest.  # noqa: E501

        The list of IDs for the business items.  # noqa: E501

        :return: The business_item_ids of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._business_item_ids

    @business_item_ids.setter
    def business_item_ids(self, business_item_ids):
        """Sets the business_item_ids of this StartWorkflowInstancesRequest.

        The list of IDs for the business items.  # noqa: E501

        :param business_item_ids: The business_item_ids of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: list[str]
        """

        self._business_item_ids = business_item_ids

    @property
    def business_item_type(self):
        """Gets the business_item_type of this StartWorkflowInstancesRequest.  # noqa: E501

        The resource type of the passed in business items.  # noqa: E501

        :return: The business_item_type of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._business_item_type

    @business_item_type.setter
    def business_item_type(self, business_item_type):
        """Sets the business_item_type of this StartWorkflowInstancesRequest.

        The resource type of the passed in business items.  # noqa: E501

        :param business_item_type: The business_item_type of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["ASSET", "DOMAIN", "COMMUNITY", "GLOBAL"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and business_item_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `business_item_type` ({0}), must be one of {1}"  # noqa: E501
                .format(business_item_type, allowed_values)
            )

        self._business_item_type = business_item_type

    @property
    def form_properties(self):
        """Gets the form_properties of this StartWorkflowInstancesRequest.  # noqa: E501

        The properties of the workflow.  # noqa: E501

        :return: The form_properties of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._form_properties

    @form_properties.setter
    def form_properties(self, form_properties):
        """Sets the form_properties of this StartWorkflowInstancesRequest.

        The properties of the workflow.  # noqa: E501

        :param form_properties: The form_properties of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: dict(str, str)
        """

        self._form_properties = form_properties

    @property
    def guest_user_id(self):
        """Gets the guest_user_id of this StartWorkflowInstancesRequest.  # noqa: E501

        The ID of the guest user starting the workflow.  # noqa: E501

        :return: The guest_user_id of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._guest_user_id

    @guest_user_id.setter
    def guest_user_id(self, guest_user_id):
        """Sets the guest_user_id of this StartWorkflowInstancesRequest.

        The ID of the guest user starting the workflow.  # noqa: E501

        :param guest_user_id: The guest_user_id of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: str
        """

        self._guest_user_id = guest_user_id

    @property
    def send_notification(self):
        """Gets the send_notification of this StartWorkflowInstancesRequest.  # noqa: E501

        Whether a mail notification on starting the workflows should be sent. This notification is only used in the asynchronous api version (in a job).  # noqa: E501

        :return: The send_notification of this StartWorkflowInstancesRequest.  # noqa: E501
        :rtype: bool
        """
        return self._send_notification

    @send_notification.setter
    def send_notification(self, send_notification):
        """Sets the send_notification of this StartWorkflowInstancesRequest.

        Whether a mail notification on starting the workflows should be sent. This notification is only used in the asynchronous api version (in a job).  # noqa: E501

        :param send_notification: The send_notification of this StartWorkflowInstancesRequest.  # noqa: E501
        :type: bool
        """

        self._send_notification = send_notification

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
        if not isinstance(other, StartWorkflowInstancesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StartWorkflowInstancesRequest):
            return True

        return self.to_dict() != other.to_dict()
