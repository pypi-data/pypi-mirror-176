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


class ExportComplexRelationsToExcelRequest(object):
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
        'complex_relation_type_id': 'str',
        'domain_id': 'str',
        'store_as_attachment': 'bool',
        'file_name': 'str',
        'include_header_row': 'bool',
        'support_roundtrip': 'bool',
        'remove_formatting': 'bool',
        'sheet_name': 'str',
        'xlsx': 'bool'
    }

    attribute_map = {
        'complex_relation_type_id': 'complexRelationTypeId',
        'domain_id': 'domainId',
        'store_as_attachment': 'storeAsAttachment',
        'file_name': 'fileName',
        'include_header_row': 'includeHeaderRow',
        'support_roundtrip': 'supportRoundtrip',
        'remove_formatting': 'removeFormatting',
        'sheet_name': 'sheetName',
        'xlsx': 'xlsx'
    }

    def __init__(self, complex_relation_type_id=None, domain_id=None, store_as_attachment=None, file_name=None, include_header_row=None, support_roundtrip=None, remove_formatting=None, sheet_name=None, xlsx=None, local_vars_configuration=None):  # noqa: E501
        """ExportComplexRelationsToExcelRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._complex_relation_type_id = None
        self._domain_id = None
        self._store_as_attachment = None
        self._file_name = None
        self._include_header_row = None
        self._support_roundtrip = None
        self._remove_formatting = None
        self._sheet_name = None
        self._xlsx = None
        self.discriminator = None

        self.complex_relation_type_id = complex_relation_type_id
        if domain_id is not None:
            self.domain_id = domain_id
        if store_as_attachment is not None:
            self.store_as_attachment = store_as_attachment
        if file_name is not None:
            self.file_name = file_name
        if include_header_row is not None:
            self.include_header_row = include_header_row
        if support_roundtrip is not None:
            self.support_roundtrip = support_roundtrip
        if remove_formatting is not None:
            self.remove_formatting = remove_formatting
        if sheet_name is not None:
            self.sheet_name = sheet_name
        if xlsx is not None:
            self.xlsx = xlsx

    @property
    def complex_relation_type_id(self):
        """Gets the complex_relation_type_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        The Id of the ComplexRelationType for which the export will be executed.  # noqa: E501

        :return: The complex_relation_type_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: str
        """
        return self._complex_relation_type_id

    @complex_relation_type_id.setter
    def complex_relation_type_id(self, complex_relation_type_id):
        """Sets the complex_relation_type_id of this ExportComplexRelationsToExcelRequest.

        The Id of the ComplexRelationType for which the export will be executed.  # noqa: E501

        :param complex_relation_type_id: The complex_relation_type_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and complex_relation_type_id is None:  # noqa: E501
            raise ValueError("Invalid value for `complex_relation_type_id`, must not be `None`")  # noqa: E501

        self._complex_relation_type_id = complex_relation_type_id

    @property
    def domain_id(self):
        """Gets the domain_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        The Id of the Domain to filter on (optional).  # noqa: E501

        :return: The domain_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: str
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id):
        """Sets the domain_id of this ExportComplexRelationsToExcelRequest.

        The Id of the Domain to filter on (optional).  # noqa: E501

        :param domain_id: The domain_id of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: str
        """

        self._domain_id = domain_id

    @property
    def store_as_attachment(self):
        """Gets the store_as_attachment of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        Sets if the export should be stored as an attachment (<code>true</code>) or not (<code>false</code>)<br/>of the provided {@link #domainId}.  # noqa: E501

        :return: The store_as_attachment of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._store_as_attachment

    @store_as_attachment.setter
    def store_as_attachment(self, store_as_attachment):
        """Sets the store_as_attachment of this ExportComplexRelationsToExcelRequest.

        Sets if the export should be stored as an attachment (<code>true</code>) or not (<code>false</code>)<br/>of the provided {@link #domainId}.  # noqa: E501

        :param store_as_attachment: The store_as_attachment of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: bool
        """

        self._store_as_attachment = store_as_attachment

    @property
    def file_name(self):
        """Gets the file_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        The name of the file. (optional) if not provided a name is generated.  # noqa: E501

        :return: The file_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this ExportComplexRelationsToExcelRequest.

        The name of the file. (optional) if not provided a name is generated.  # noqa: E501

        :param file_name: The file_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: str
        """

        self._file_name = file_name

    @property
    def include_header_row(self):
        """Gets the include_header_row of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        Set if the file will include a header (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :return: The include_header_row of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._include_header_row

    @include_header_row.setter
    def include_header_row(self, include_header_row):
        """Sets the include_header_row of this ExportComplexRelationsToExcelRequest.

        Set if the file will include a header (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :param include_header_row: The include_header_row of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: bool
        """

        self._include_header_row = include_header_row

    @property
    def support_roundtrip(self):
        """Gets the support_roundtrip of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        Adds characteristics to support reimport (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :return: The support_roundtrip of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._support_roundtrip

    @support_roundtrip.setter
    def support_roundtrip(self, support_roundtrip):
        """Sets the support_roundtrip of this ExportComplexRelationsToExcelRequest.

        Adds characteristics to support reimport (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :param support_roundtrip: The support_roundtrip of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: bool
        """

        self._support_roundtrip = support_roundtrip

    @property
    def remove_formatting(self):
        """Gets the remove_formatting of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        Remove text formatting (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :return: The remove_formatting of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._remove_formatting

    @remove_formatting.setter
    def remove_formatting(self, remove_formatting):
        """Sets the remove_formatting of this ExportComplexRelationsToExcelRequest.

        Remove text formatting (<code>true</code>) or not (<code>false</code>)<br/>Default value is <code>false</code>.  # noqa: E501

        :param remove_formatting: The remove_formatting of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: bool
        """

        self._remove_formatting = remove_formatting

    @property
    def sheet_name(self):
        """Gets the sheet_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        The name of the sheet.  # noqa: E501

        :return: The sheet_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: str
        """
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name):
        """Sets the sheet_name of this ExportComplexRelationsToExcelRequest.

        The name of the sheet.  # noqa: E501

        :param sheet_name: The sheet_name of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: str
        """

        self._sheet_name = sheet_name

    @property
    def xlsx(self):
        """Gets the xlsx of this ExportComplexRelationsToExcelRequest.  # noqa: E501

        Set if the Excel file to export will be '.xlsx' file (<code>true</code>) or a '.xls' file (<code>false</code>)<br/>Default value is (<code>true</code>).  # noqa: E501

        :return: The xlsx of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._xlsx

    @xlsx.setter
    def xlsx(self, xlsx):
        """Sets the xlsx of this ExportComplexRelationsToExcelRequest.

        Set if the Excel file to export will be '.xlsx' file (<code>true</code>) or a '.xls' file (<code>false</code>)<br/>Default value is (<code>true</code>).  # noqa: E501

        :param xlsx: The xlsx of this ExportComplexRelationsToExcelRequest.  # noqa: E501
        :type: bool
        """

        self._xlsx = xlsx

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
        if not isinstance(other, ExportComplexRelationsToExcelRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ExportComplexRelationsToExcelRequest):
            return True

        return self.to_dict() != other.to_dict()
