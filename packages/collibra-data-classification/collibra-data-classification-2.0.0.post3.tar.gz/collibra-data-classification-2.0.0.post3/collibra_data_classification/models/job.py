# coding: utf-8

"""
    Collibra Catalog classification API

    <p>The Catalog API offers functionality related to the catalog product.<br/> It is mainly focused on facilitating the ingestion of information into Catalog. The API enables users to more easily connect Catalog to sources that are not necessarily natively supported in the product. </p>  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from collibra_data_classification.configuration import Configuration


class Job(object):
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
        'created_by': 'str',
        'created_on': 'int',
        'last_modified_by': 'str',
        'last_modified_on': 'int',
        'system': 'bool',
        'resource_type': 'str',
        'name': 'str',
        'type': 'str',
        'user_id': 'str',
        'visibility': 'int',
        'progress_percentage': 'float',
        'cancelable': 'bool',
        'start_date': 'int',
        'end_date': 'int',
        'state': 'str',
        'result': 'str',
        'message': 'str'
    }

    attribute_map = {
        'id': 'id',
        'created_by': 'createdBy',
        'created_on': 'createdOn',
        'last_modified_by': 'lastModifiedBy',
        'last_modified_on': 'lastModifiedOn',
        'system': 'system',
        'resource_type': 'resourceType',
        'name': 'name',
        'type': 'type',
        'user_id': 'userId',
        'visibility': 'visibility',
        'progress_percentage': 'progressPercentage',
        'cancelable': 'cancelable',
        'start_date': 'startDate',
        'end_date': 'endDate',
        'state': 'state',
        'result': 'result',
        'message': 'message'
    }

    def __init__(self, id=None, created_by=None, created_on=None, last_modified_by=None, last_modified_on=None, system=None, resource_type=None, name=None, type=None, user_id=None, visibility=None, progress_percentage=None, cancelable=None, start_date=None, end_date=None, state=None, result=None, message=None, local_vars_configuration=None):  # noqa: E501
        """Job - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_by = None
        self._created_on = None
        self._last_modified_by = None
        self._last_modified_on = None
        self._system = None
        self._resource_type = None
        self._name = None
        self._type = None
        self._user_id = None
        self._visibility = None
        self._progress_percentage = None
        self._cancelable = None
        self._start_date = None
        self._end_date = None
        self._state = None
        self._result = None
        self._message = None
        self.discriminator = None

        self.id = id
        if created_by is not None:
            self.created_by = created_by
        if created_on is not None:
            self.created_on = created_on
        if last_modified_by is not None:
            self.last_modified_by = last_modified_by
        if last_modified_on is not None:
            self.last_modified_on = last_modified_on
        if system is not None:
            self.system = system
        self.resource_type = resource_type
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if user_id is not None:
            self.user_id = user_id
        if visibility is not None:
            self.visibility = visibility
        if progress_percentage is not None:
            self.progress_percentage = progress_percentage
        if cancelable is not None:
            self.cancelable = cancelable
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if state is not None:
            self.state = state
        if result is not None:
            self.result = result
        if message is not None:
            self.message = message

    @property
    def id(self):
        """Gets the id of this Job.  # noqa: E501

        The id of the represented object (entity).  # noqa: E501

        :return: The id of this Job.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Job.

        The id of the represented object (entity).  # noqa: E501

        :param id: The id of this Job.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_by(self):
        """Gets the created_by of this Job.  # noqa: E501

        The id of the user that created this resource.  # noqa: E501

        :return: The created_by of this Job.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Job.

        The id of the user that created this resource.  # noqa: E501

        :param created_by: The created_by of this Job.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_on(self):
        """Gets the created_on of this Job.  # noqa: E501

        The timestamp (in UTC time standard) of the creation of this resource.  # noqa: E501

        :return: The created_on of this Job.  # noqa: E501
        :rtype: int
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """Sets the created_on of this Job.

        The timestamp (in UTC time standard) of the creation of this resource.  # noqa: E501

        :param created_on: The created_on of this Job.  # noqa: E501
        :type: int
        """

        self._created_on = created_on

    @property
    def last_modified_by(self):
        """Gets the last_modified_by of this Job.  # noqa: E501

        The id of the user who modified this resource the last time.  # noqa: E501

        :return: The last_modified_by of this Job.  # noqa: E501
        :rtype: str
        """
        return self._last_modified_by

    @last_modified_by.setter
    def last_modified_by(self, last_modified_by):
        """Sets the last_modified_by of this Job.

        The id of the user who modified this resource the last time.  # noqa: E501

        :param last_modified_by: The last_modified_by of this Job.  # noqa: E501
        :type: str
        """

        self._last_modified_by = last_modified_by

    @property
    def last_modified_on(self):
        """Gets the last_modified_on of this Job.  # noqa: E501

        The timestamp (in UTC time standard) of the last modification of this resource.  # noqa: E501

        :return: The last_modified_on of this Job.  # noqa: E501
        :rtype: int
        """
        return self._last_modified_on

    @last_modified_on.setter
    def last_modified_on(self, last_modified_on):
        """Sets the last_modified_on of this Job.

        The timestamp (in UTC time standard) of the last modification of this resource.  # noqa: E501

        :param last_modified_on: The last_modified_on of this Job.  # noqa: E501
        :type: int
        """

        self._last_modified_on = last_modified_on

    @property
    def system(self):
        """Gets the system of this Job.  # noqa: E501

        Whether this is a system resource or not.  # noqa: E501

        :return: The system of this Job.  # noqa: E501
        :rtype: bool
        """
        return self._system

    @system.setter
    def system(self, system):
        """Sets the system of this Job.

        Whether this is a system resource or not.  # noqa: E501

        :param system: The system of this Job.  # noqa: E501
        :type: bool
        """

        self._system = system

    @property
    def resource_type(self):
        """Gets the resource_type of this Job.  # noqa: E501

        The type of this resource, i.e. [Community, Asset, Domain, Attribute, Relation, WorkflowInstance].  # noqa: E501

        :return: The resource_type of this Job.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this Job.

        The type of this resource, i.e. [Community, Asset, Domain, Attribute, Relation, WorkflowInstance].  # noqa: E501

        :param resource_type: The resource_type of this Job.  # noqa: E501
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
        """Gets the name of this Job.  # noqa: E501

        The name of the resource.  # noqa: E501

        :return: The name of this Job.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Job.

        The name of the resource.  # noqa: E501

        :param name: The name of this Job.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this Job.  # noqa: E501

        The type of the job.  # noqa: E501

        :return: The type of this Job.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Job.

        The type of the job.  # noqa: E501

        :param type: The type of this Job.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def user_id(self):
        """Gets the user_id of this Job.  # noqa: E501

        The ID of the user that initiated this job.  # noqa: E501

        :return: The user_id of this Job.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this Job.

        The ID of the user that initiated this job.  # noqa: E501

        :param user_id: The user_id of this Job.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def visibility(self):
        """Gets the visibility of this Job.  # noqa: E501

        The visibility of the job.  # noqa: E501

        :return: The visibility of this Job.  # noqa: E501
        :rtype: int
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """Sets the visibility of this Job.

        The visibility of the job.  # noqa: E501

        :param visibility: The visibility of this Job.  # noqa: E501
        :type: int
        """

        self._visibility = visibility

    @property
    def progress_percentage(self):
        """Gets the progress_percentage of this Job.  # noqa: E501

        The progress percentage of the job.  # noqa: E501

        :return: The progress_percentage of this Job.  # noqa: E501
        :rtype: float
        """
        return self._progress_percentage

    @progress_percentage.setter
    def progress_percentage(self, progress_percentage):
        """Sets the progress_percentage of this Job.

        The progress percentage of the job.  # noqa: E501

        :param progress_percentage: The progress_percentage of this Job.  # noqa: E501
        :type: float
        """

        self._progress_percentage = progress_percentage

    @property
    def cancelable(self):
        """Gets the cancelable of this Job.  # noqa: E501

        Whether this job is cancelable or not. If set to false it will not be possible to cancel the job once submitted.  # noqa: E501

        :return: The cancelable of this Job.  # noqa: E501
        :rtype: bool
        """
        return self._cancelable

    @cancelable.setter
    def cancelable(self, cancelable):
        """Sets the cancelable of this Job.

        Whether this job is cancelable or not. If set to false it will not be possible to cancel the job once submitted.  # noqa: E501

        :param cancelable: The cancelable of this Job.  # noqa: E501
        :type: bool
        """

        self._cancelable = cancelable

    @property
    def start_date(self):
        """Gets the start_date of this Job.  # noqa: E501

        The start date of the job.  # noqa: E501

        :return: The start_date of this Job.  # noqa: E501
        :rtype: int
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this Job.

        The start date of the job.  # noqa: E501

        :param start_date: The start_date of this Job.  # noqa: E501
        :type: int
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this Job.  # noqa: E501

        The end date of the job.  # noqa: E501

        :return: The end_date of this Job.  # noqa: E501
        :rtype: int
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this Job.

        The end date of the job.  # noqa: E501

        :param end_date: The end_date of this Job.  # noqa: E501
        :type: int
        """

        self._end_date = end_date

    @property
    def state(self):
        """Gets the state of this Job.  # noqa: E501

        The state of the job.  # noqa: E501

        :return: The state of this Job.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Job.

        The state of the job.  # noqa: E501

        :param state: The state of this Job.  # noqa: E501
        :type: str
        """
        allowed_values = ["WAITING", "RUNNING", "CANCELING", "COMPLETED", "CANCELED", "ERROR"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and state not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def result(self):
        """Gets the result of this Job.  # noqa: E501

        The result of the job.  # noqa: E501

        :return: The result of this Job.  # noqa: E501
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this Job.

        The result of the job.  # noqa: E501

        :param result: The result of this Job.  # noqa: E501
        :type: str
        """
        allowed_values = ["NOT_SET", "SUCCESS", "COMPLETED_WITH_ERROR", "FAILURE", "ABORTED"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and result not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `result` ({0}), must be one of {1}"  # noqa: E501
                .format(result, allowed_values)
            )

        self._result = result

    @property
    def message(self):
        """Gets the message of this Job.  # noqa: E501

        The message of the job.  # noqa: E501

        :return: The message of this Job.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Job.

        The message of the job.  # noqa: E501

        :param message: The message of this Job.  # noqa: E501
        :type: str
        """

        self._message = message

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
        if not isinstance(other, Job):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Job):
            return True

        return self.to_dict() != other.to_dict()
