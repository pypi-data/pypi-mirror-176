# coding: utf-8

# flake8: noqa
"""
    Collibra Data Governance Center Core API

    <p>The Core REST API allows you to create your own integrations with Collibra Data Governance Center.</p><p><i>Create custom applications to help users get access to the right data.</i></p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from collibra_core.models.activity_impl import ActivityImpl
from collibra_core.models.activity_paged_response import ActivityPagedResponse
from collibra_core.models.add_asset_request import AddAssetRequest
from collibra_core.models.add_asset_tags_request import AddAssetTagsRequest
from collibra_core.models.add_asset_type_assignment_rule_request import AddAssetTypeAssignmentRuleRequest
from collibra_core.models.add_asset_type_request import AddAssetTypeRequest
from collibra_core.models.add_assignment_request import AddAssignmentRequest
from collibra_core.models.add_attribute_request import AddAttributeRequest
from collibra_core.models.add_attribute_type_request import AddAttributeTypeRequest
from collibra_core.models.add_comment_request import AddCommentRequest
from collibra_core.models.add_community_request import AddCommunityRequest
from collibra_core.models.add_complex_relation_request import AddComplexRelationRequest
from collibra_core.models.add_complex_relation_type_request import AddComplexRelationTypeRequest
from collibra_core.models.add_data_quality_rule_request import AddDataQualityRuleRequest
from collibra_core.models.add_diagram_picture_request import AddDiagramPictureRequest
from collibra_core.models.add_domain_request import AddDomainRequest
from collibra_core.models.add_domain_type_assignment_rule_request import AddDomainTypeAssignmentRuleRequest
from collibra_core.models.add_domain_type_request import AddDomainTypeRequest
from collibra_core.models.add_issue_request import AddIssueRequest
from collibra_core.models.add_mapping_request import AddMappingRequest
from collibra_core.models.add_rating_request import AddRatingRequest
from collibra_core.models.add_relation_request import AddRelationRequest
from collibra_core.models.add_relation_type_request import AddRelationTypeRequest
from collibra_core.models.add_responsibility_request import AddResponsibilityRequest
from collibra_core.models.add_role_request import AddRoleRequest
from collibra_core.models.add_scope_request import AddScopeRequest
from collibra_core.models.add_status_request import AddStatusRequest
from collibra_core.models.add_user_group_request import AddUserGroupRequest
from collibra_core.models.add_user_request import AddUserRequest
from collibra_core.models.add_user_to_user_groups_request import AddUserToUserGroupsRequest
from collibra_core.models.add_users_to_user_group_request import AddUsersToUserGroupRequest
from collibra_core.models.add_view_permission_request import AddViewPermissionRequest
from collibra_core.models.address import Address
from collibra_core.models.application_info import ApplicationInfo
from collibra_core.models.application_version_impl import ApplicationVersionImpl
from collibra_core.models.articulation_rule_impl import ArticulationRuleImpl
from collibra_core.models.articulation_rule_request import ArticulationRuleRequest
from collibra_core.models.asset_assignment_rule_impl import AssetAssignmentRuleImpl
from collibra_core.models.asset_impl import AssetImpl
from collibra_core.models.asset_paged_response import AssetPagedResponse
from collibra_core.models.asset_reference_impl import AssetReferenceImpl
from collibra_core.models.asset_type_impl import AssetTypeImpl
from collibra_core.models.asset_type_paged_response import AssetTypePagedResponse
from collibra_core.models.assigned_attribute_type import AssignedAttributeType
from collibra_core.models.assigned_attribute_type_all_of import AssignedAttributeTypeAllOf
from collibra_core.models.assigned_characteristic_type import AssignedCharacteristicType
from collibra_core.models.assigned_complex_relation_type import AssignedComplexRelationType
from collibra_core.models.assigned_complex_relation_type_all_of import AssignedComplexRelationTypeAllOf
from collibra_core.models.assigned_relation_type import AssignedRelationType
from collibra_core.models.assigned_relation_type_all_of import AssignedRelationTypeAllOf
from collibra_core.models.assignment_impl import AssignmentImpl
from collibra_core.models.attachment_impl import AttachmentImpl
from collibra_core.models.attachment_paged_response import AttachmentPagedResponse
from collibra_core.models.attribute import Attribute
from collibra_core.models.attribute_paged_response import AttributePagedResponse
from collibra_core.models.attribute_type import AttributeType
from collibra_core.models.attribute_type_paged_response import AttributeTypePagedResponse
from collibra_core.models.attribute_value import AttributeValue
from collibra_core.models.boolean_attribute import BooleanAttribute
from collibra_core.models.boolean_attribute_all_of import BooleanAttributeAllOf
from collibra_core.models.boolean_attribute_type import BooleanAttributeType
from collibra_core.models.boolean_attribute_type_all_of import BooleanAttributeTypeAllOf
from collibra_core.models.cancel_job_request import CancelJobRequest
from collibra_core.models.change_asset_request import ChangeAssetRequest
from collibra_core.models.change_asset_type_assignment_rule_request import ChangeAssetTypeAssignmentRuleRequest
from collibra_core.models.change_asset_type_request import ChangeAssetTypeRequest
from collibra_core.models.change_assignment_request import ChangeAssignmentRequest
from collibra_core.models.change_attribute_request import ChangeAttributeRequest
from collibra_core.models.change_attribute_type_request import ChangeAttributeTypeRequest
from collibra_core.models.change_comment_request import ChangeCommentRequest
from collibra_core.models.change_community_request import ChangeCommunityRequest
from collibra_core.models.change_complex_relation_request import ChangeComplexRelationRequest
from collibra_core.models.change_complex_relation_type_request import ChangeComplexRelationTypeRequest
from collibra_core.models.change_data_quality_rule_request import ChangeDataQualityRuleRequest
from collibra_core.models.change_domain_request import ChangeDomainRequest
from collibra_core.models.change_domain_type_assignment_rule_request import ChangeDomainTypeAssignmentRuleRequest
from collibra_core.models.change_domain_type_request import ChangeDomainTypeRequest
from collibra_core.models.change_mapping_by_external_entity_request import ChangeMappingByExternalEntityRequest
from collibra_core.models.change_mapping_by_mapped_resource_request import ChangeMappingByMappedResourceRequest
from collibra_core.models.change_mapping_request import ChangeMappingRequest
from collibra_core.models.change_rating_request import ChangeRatingRequest
from collibra_core.models.change_relation_request import ChangeRelationRequest
from collibra_core.models.change_relation_type_request import ChangeRelationTypeRequest
from collibra_core.models.change_role_request import ChangeRoleRequest
from collibra_core.models.change_scope_request import ChangeScopeRequest
from collibra_core.models.change_status_request import ChangeStatusRequest
from collibra_core.models.change_tag_request import ChangeTagRequest
from collibra_core.models.change_user_avatar_request import ChangeUserAvatarRequest
from collibra_core.models.change_user_group_request import ChangeUserGroupRequest
from collibra_core.models.change_user_request import ChangeUserRequest
from collibra_core.models.change_workflow_definition_request import ChangeWorkflowDefinitionRequest
from collibra_core.models.characteristic_type_assignment_reference import CharacteristicTypeAssignmentReference
from collibra_core.models.comment import Comment
from collibra_core.models.comment_paged_response import CommentPagedResponse
from collibra_core.models.community_impl import CommunityImpl
from collibra_core.models.community_paged_response import CommunityPagedResponse
from collibra_core.models.complete_workflow_tasks_request import CompleteWorkflowTasksRequest
from collibra_core.models.complex_relation_attribute_type_impl import ComplexRelationAttributeTypeImpl
from collibra_core.models.complex_relation_attribute_type_request import ComplexRelationAttributeTypeRequest
from collibra_core.models.complex_relation_impl import ComplexRelationImpl
from collibra_core.models.complex_relation_leg_impl import ComplexRelationLegImpl
from collibra_core.models.complex_relation_leg_request import ComplexRelationLegRequest
from collibra_core.models.complex_relation_leg_type_impl import ComplexRelationLegTypeImpl
from collibra_core.models.complex_relation_leg_type_request import ComplexRelationLegTypeRequest
from collibra_core.models.complex_relation_type_impl import ComplexRelationTypeImpl
from collibra_core.models.complex_relation_type_paged_response import ComplexRelationTypePagedResponse
from collibra_core.models.connection_string_parameter import ConnectionStringParameter
from collibra_core.models.cursor_paged_response_asset import CursorPagedResponseAsset
from collibra_core.models.cursor_paged_response_attribute import CursorPagedResponseAttribute
from collibra_core.models.cursor_paged_response_community import CursorPagedResponseCommunity
from collibra_core.models.cursor_paged_response_complex_relation import CursorPagedResponseComplexRelation
from collibra_core.models.cursor_paged_response_domain import CursorPagedResponseDomain
from collibra_core.models.cursor_paged_response_relation import CursorPagedResponseRelation
from collibra_core.models.dgc_session import DGCSession
from collibra_core.models.data_quality_metric_impl import DataQualityMetricImpl
from collibra_core.models.data_quality_metric_request import DataQualityMetricRequest
from collibra_core.models.data_quality_rule_impl import DataQualityRuleImpl
from collibra_core.models.data_quality_rule_paged_response import DataQualityRulePagedResponse
from collibra_core.models.date_attribute import DateAttribute
from collibra_core.models.date_attribute_all_of import DateAttributeAllOf
from collibra_core.models.date_attribute_type import DateAttributeType
from collibra_core.models.domain_impl import DomainImpl
from collibra_core.models.domain_paged_response import DomainPagedResponse
from collibra_core.models.domain_type_impl import DomainTypeImpl
from collibra_core.models.domain_type_paged_response import DomainTypePagedResponse
from collibra_core.models.dropdown_value import DropdownValue
from collibra_core.models.email import Email
from collibra_core.models.export_complex_relations_to_csv_request import ExportComplexRelationsToCSVRequest
from collibra_core.models.export_complex_relations_to_excel_request import ExportComplexRelationsToExcelRequest
from collibra_core.models.file_info_impl import FileInfoImpl
from collibra_core.models.file_reference_impl import FileReferenceImpl
from collibra_core.models.file_upload import FileUpload
from collibra_core.models.form_property import FormProperty
from collibra_core.models.inline_object import InlineObject
from collibra_core.models.inline_object1 import InlineObject1
from collibra_core.models.inline_object2 import InlineObject2
from collibra_core.models.instant_messaging_account import InstantMessagingAccount
from collibra_core.models.jdbc_driver import JdbcDriver
from collibra_core.models.jdbc_driver_file import JdbcDriverFile
from collibra_core.models.jdbc_driver_paged_response import JdbcDriverPagedResponse
from collibra_core.models.job import Job
from collibra_core.models.job_paged_response import JobPagedResponse
from collibra_core.models.login_request import LoginRequest
from collibra_core.models.mapping import Mapping
from collibra_core.models.mapping_paged_response import MappingPagedResponse
from collibra_core.models.merge_tags_request import MergeTagsRequest
from collibra_core.models.message_event_received_request import MessageEventReceivedRequest
from collibra_core.models.multi_value_list_attribute import MultiValueListAttribute
from collibra_core.models.multi_value_list_attribute_all_of import MultiValueListAttributeAllOf
from collibra_core.models.multi_value_list_attribute_type import MultiValueListAttributeType
from collibra_core.models.multi_value_list_attribute_type_all_of import MultiValueListAttributeTypeAllOf
from collibra_core.models.named_described_resource_reference import NamedDescribedResourceReference
from collibra_core.models.named_described_workflow_start_event_type import NamedDescribedWorkflowStartEventType
from collibra_core.models.named_resource_reference_impl import NamedResourceReferenceImpl
from collibra_core.models.navigation_statistics_entry import NavigationStatisticsEntry
from collibra_core.models.navigation_statistics_entry_paged_response import NavigationStatisticsEntryPagedResponse
from collibra_core.models.numeric_attribute import NumericAttribute
from collibra_core.models.numeric_attribute_all_of import NumericAttributeAllOf
from collibra_core.models.numeric_attribute_type import NumericAttributeType
from collibra_core.models.numeric_attribute_type_all_of import NumericAttributeTypeAllOf
from collibra_core.models.option_value import OptionValue
from collibra_core.models.paged_response import PagedResponse
from collibra_core.models.paged_response_activity import PagedResponseActivity
from collibra_core.models.paged_response_asset import PagedResponseAsset
from collibra_core.models.paged_response_asset_type import PagedResponseAssetType
from collibra_core.models.paged_response_attachment import PagedResponseAttachment
from collibra_core.models.paged_response_attribute_type import PagedResponseAttributeType
from collibra_core.models.paged_response_comment import PagedResponseComment
from collibra_core.models.paged_response_complex_relation_type import PagedResponseComplexRelationType
from collibra_core.models.paged_response_data_quality_rule import PagedResponseDataQualityRule
from collibra_core.models.paged_response_domain_type import PagedResponseDomainType
from collibra_core.models.paged_response_jdbc_driver import PagedResponseJdbcDriver
from collibra_core.models.paged_response_job import PagedResponseJob
from collibra_core.models.paged_response_mapping import PagedResponseMapping
from collibra_core.models.paged_response_navigation_statistics_entry import PagedResponseNavigationStatisticsEntry
from collibra_core.models.paged_response_rating import PagedResponseRating
from collibra_core.models.paged_response_relation_type import PagedResponseRelationType
from collibra_core.models.paged_response_responsibility import PagedResponseResponsibility
from collibra_core.models.paged_response_role import PagedResponseRole
from collibra_core.models.paged_response_scope import PagedResponseScope
from collibra_core.models.paged_response_status import PagedResponseStatus
from collibra_core.models.paged_response_tag import PagedResponseTag
from collibra_core.models.paged_response_user import PagedResponseUser
from collibra_core.models.paged_response_user_group import PagedResponseUserGroup
from collibra_core.models.paged_response_validation_result import PagedResponseValidationResult
from collibra_core.models.paged_response_view_permission import PagedResponseViewPermission
from collibra_core.models.paged_response_workflow_definition import PagedResponseWorkflowDefinition
from collibra_core.models.paged_response_workflow_instance import PagedResponseWorkflowInstance
from collibra_core.models.paged_response_workflow_task import PagedResponseWorkflowTask
from collibra_core.models.phone_number import PhoneNumber
from collibra_core.models.rating import Rating
from collibra_core.models.ratings_paged_response import RatingsPagedResponse
from collibra_core.models.related_asset_id import RelatedAssetId
from collibra_core.models.related_asset_reference import RelatedAssetReference
from collibra_core.models.relation_impl import RelationImpl
from collibra_core.models.relation_paged_response import RelationPagedResponse
from collibra_core.models.relation_trace_entry_impl import RelationTraceEntryImpl
from collibra_core.models.relation_trace_entry_request import RelationTraceEntryRequest
from collibra_core.models.relation_trace_impl import RelationTraceImpl
from collibra_core.models.relation_type_impl import RelationTypeImpl
from collibra_core.models.relation_type_paged_response import RelationTypePagedResponse
from collibra_core.models.remove_asset_tags_request import RemoveAssetTagsRequest
from collibra_core.models.remove_user_from_user_groups_request import RemoveUserFromUserGroupsRequest
from collibra_core.models.remove_users_from_user_group_request import RemoveUsersFromUserGroupRequest
from collibra_core.models.resource_reference import ResourceReference
from collibra_core.models.responsibility_impl import ResponsibilityImpl
from collibra_core.models.role_impl import RoleImpl
from collibra_core.models.scope_impl import ScopeImpl
from collibra_core.models.scope_paged_response import ScopePagedResponse
from collibra_core.models.script_attribute import ScriptAttribute
from collibra_core.models.script_attribute_all_of import ScriptAttributeAllOf
from collibra_core.models.script_attribute_type import ScriptAttributeType
from collibra_core.models.script_attribute_type_all_of import ScriptAttributeTypeAllOf
from collibra_core.models.set_asset_attributes_request import SetAssetAttributesRequest
from collibra_core.models.set_asset_relations_request import SetAssetRelationsRequest
from collibra_core.models.set_asset_responsibilities_request import SetAssetResponsibilitiesRequest
from collibra_core.models.set_asset_tags_request import SetAssetTagsRequest
from collibra_core.models.set_user_groups_for_user_request import SetUserGroupsForUserRequest
from collibra_core.models.single_value_list_attribute import SingleValueListAttribute
from collibra_core.models.single_value_list_attribute_all_of import SingleValueListAttributeAllOf
from collibra_core.models.single_value_list_attribute_type import SingleValueListAttributeType
from collibra_core.models.solution_info import SolutionInfo
from collibra_core.models.start_form_data_impl import StartFormDataImpl
from collibra_core.models.start_workflow_instances_request import StartWorkflowInstancesRequest
from collibra_core.models.status_impl import StatusImpl
from collibra_core.models.status_paged_response import StatusPagedResponse
from collibra_core.models.string_attribute import StringAttribute
from collibra_core.models.string_attribute_type import StringAttributeType
from collibra_core.models.string_attribute_type_all_of import StringAttributeTypeAllOf
from collibra_core.models.symbol_data_impl import SymbolDataImpl
from collibra_core.models.tag import Tag
from collibra_core.models.tag_paged_response import TagPagedResponse
from collibra_core.models.task_form_data import TaskFormData
from collibra_core.models.user import User
from collibra_core.models.user_group_impl import UserGroupImpl
from collibra_core.models.user_group_paged_response import UserGroupPagedResponse
from collibra_core.models.user_paged_response import UserPagedResponse
from collibra_core.models.user_permissions import UserPermissions
from collibra_core.models.user_reference_impl import UserReferenceImpl
from collibra_core.models.validate_in_job_request import ValidateInJobRequest
from collibra_core.models.validation_result_impl import ValidationResultImpl
from collibra_core.models.validation_result_paged_response import ValidationResultPagedResponse
from collibra_core.models.view_permission_impl import ViewPermissionImpl
from collibra_core.models.website import Website
from collibra_core.models.workflow_definition_impl import WorkflowDefinitionImpl
from collibra_core.models.workflow_definition_paged_response import WorkflowDefinitionPagedResponse
from collibra_core.models.workflow_definition_reference import WorkflowDefinitionReference
from collibra_core.models.workflow_instance import WorkflowInstance
from collibra_core.models.workflow_task import WorkflowTask
from collibra_core.models.workflow_task_paged_response import WorkflowTaskPagedResponse
