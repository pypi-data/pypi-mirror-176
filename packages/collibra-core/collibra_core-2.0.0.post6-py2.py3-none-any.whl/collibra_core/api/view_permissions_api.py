# coding: utf-8

"""
    Collibra Data Governance Center Core API

    <p>The Core REST API allows you to create your own integrations with Collibra Data Governance Center.</p><p><i>Create custom applications to help users get access to the right data.</i></p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from collibra_core.api_client import ApiClient
from collibra_core.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ViewPermissionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_view_permission(self, **kwargs):  # noqa: E501
        """Adds a view permission. It can be applied only to 'Community' and 'Domain' resource types.  # noqa: E501

        Adds a view permission. It can be applied only to 'Community' and 'Domain' resource types.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_view_permission(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param AddViewPermissionRequest add_view_permission_request: Properties of the new view permission. Valid resource types are: 'Community', 'Domain'.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ViewPermissionImpl
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.add_view_permission_with_http_info(**kwargs)  # noqa: E501

    def add_view_permission_with_http_info(self, **kwargs):  # noqa: E501
        """Adds a view permission. It can be applied only to 'Community' and 'Domain' resource types.  # noqa: E501

        Adds a view permission. It can be applied only to 'Community' and 'Domain' resource types.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_view_permission_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param AddViewPermissionRequest add_view_permission_request: Properties of the new view permission. Valid resource types are: 'Community', 'Domain'.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ViewPermissionImpl, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'add_view_permission_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_view_permission" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'add_view_permission_request' in local_var_params:
            body_params = local_var_params['add_view_permission_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/viewPermissions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViewPermissionImpl',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_view_permissions(self, **kwargs):  # noqa: E501
        """Finds view permissions with given criteria.  # noqa: E501

        Finds view permissions with given criteria.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_view_permissions(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int offset: The first result to retrieve. If not set (offset = <code>0</code>), results will be retrieved starting from row <code>0</code>.
        :param int limit: The maximum number of results to retrieve. If not set (limit = <code>0</code>), the default limit will be used.
        :param int count_limit: Allows to limit the number of elements that will be counted. -1 will count everything and 0 will cause the count to be skipped
        :param str user_id: The ID of the user for whom the view permission applies.
        :param str user_group_id: The ID of the user group for whose members the view permission applies.
        :param str resource_id: The ID of the resource to which the view permission applies.
        :param str resource_type: The type of resource addressed by the view permission.
        :param bool include_inherited: Whether to include inherited permissions in search results.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PagedResponseViewPermission
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.find_view_permissions_with_http_info(**kwargs)  # noqa: E501

    def find_view_permissions_with_http_info(self, **kwargs):  # noqa: E501
        """Finds view permissions with given criteria.  # noqa: E501

        Finds view permissions with given criteria.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_view_permissions_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int offset: The first result to retrieve. If not set (offset = <code>0</code>), results will be retrieved starting from row <code>0</code>.
        :param int limit: The maximum number of results to retrieve. If not set (limit = <code>0</code>), the default limit will be used.
        :param int count_limit: Allows to limit the number of elements that will be counted. -1 will count everything and 0 will cause the count to be skipped
        :param str user_id: The ID of the user for whom the view permission applies.
        :param str user_group_id: The ID of the user group for whose members the view permission applies.
        :param str resource_id: The ID of the resource to which the view permission applies.
        :param str resource_type: The type of resource addressed by the view permission.
        :param bool include_inherited: Whether to include inherited permissions in search results.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PagedResponseViewPermission, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'offset',
            'limit',
            'count_limit',
            'user_id',
            'user_group_id',
            'resource_id',
            'resource_type',
            'include_inherited'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_view_permissions" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'count_limit' in local_var_params and local_var_params['count_limit'] is not None:  # noqa: E501
            query_params.append(('countLimit', local_var_params['count_limit']))  # noqa: E501
        if 'user_id' in local_var_params and local_var_params['user_id'] is not None:  # noqa: E501
            query_params.append(('userId', local_var_params['user_id']))  # noqa: E501
        if 'user_group_id' in local_var_params and local_var_params['user_group_id'] is not None:  # noqa: E501
            query_params.append(('userGroupId', local_var_params['user_group_id']))  # noqa: E501
        if 'resource_id' in local_var_params and local_var_params['resource_id'] is not None:  # noqa: E501
            query_params.append(('resourceId', local_var_params['resource_id']))  # noqa: E501
        if 'resource_type' in local_var_params and local_var_params['resource_type'] is not None:  # noqa: E501
            query_params.append(('resourceType', local_var_params['resource_type']))  # noqa: E501
        if 'include_inherited' in local_var_params and local_var_params['include_inherited'] is not None:  # noqa: E501
            query_params.append(('includeInherited', local_var_params['include_inherited']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/viewPermissions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PagedResponseViewPermission',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_view_permission(self, view_permission_id, **kwargs):  # noqa: E501
        """Retrieves a view permission.  # noqa: E501

        Retrieves a view permission.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_view_permission(view_permission_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str view_permission_id: Identifier of the view permission to retrieve. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ViewPermissionImpl
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_view_permission_with_http_info(view_permission_id, **kwargs)  # noqa: E501

    def get_view_permission_with_http_info(self, view_permission_id, **kwargs):  # noqa: E501
        """Retrieves a view permission.  # noqa: E501

        Retrieves a view permission.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_view_permission_with_http_info(view_permission_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str view_permission_id: Identifier of the view permission to retrieve. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ViewPermissionImpl, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'view_permission_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_view_permission" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'view_permission_id' is set
        if self.api_client.client_side_validation and ('view_permission_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['view_permission_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `view_permission_id` when calling `get_view_permission`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'view_permission_id' in local_var_params:
            path_params['viewPermissionId'] = local_var_params['view_permission_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/viewPermissions/{viewPermissionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ViewPermissionImpl',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_view_permission(self, view_permission_id, **kwargs):  # noqa: E501
        """Removes a view permission.  # noqa: E501

        Removes a view permission.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_view_permission(view_permission_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str view_permission_id: Identifier of the view permission to remove. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.remove_view_permission_with_http_info(view_permission_id, **kwargs)  # noqa: E501

    def remove_view_permission_with_http_info(self, view_permission_id, **kwargs):  # noqa: E501
        """Removes a view permission.  # noqa: E501

        Removes a view permission.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_view_permission_with_http_info(view_permission_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str view_permission_id: Identifier of the view permission to remove. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'view_permission_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_view_permission" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'view_permission_id' is set
        if self.api_client.client_side_validation and ('view_permission_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['view_permission_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `view_permission_id` when calling `remove_view_permission`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'view_permission_id' in local_var_params:
            path_params['viewPermissionId'] = local_var_params['view_permission_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/viewPermissions/{viewPermissionId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
