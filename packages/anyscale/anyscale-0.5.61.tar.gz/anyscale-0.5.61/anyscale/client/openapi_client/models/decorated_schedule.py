# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class DecoratedSchedule(object):
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
        'name': 'str',
        'description': 'str',
        'project_id': 'str',
        'config': 'ProductionJobConfig',
        'schedule': 'ScheduleConfig',
        'id': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'creator_id': 'str',
        'next_trigger_at': 'datetime',
        'project': 'MiniProject',
        'creator': 'MiniUser',
        'last_executions': 'list[MiniProductionJob]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'project_id': 'project_id',
        'config': 'config',
        'schedule': 'schedule',
        'id': 'id',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'creator_id': 'creator_id',
        'next_trigger_at': 'next_trigger_at',
        'project': 'project',
        'creator': 'creator',
        'last_executions': 'last_executions'
    }

    def __init__(self, name=None, description=None, project_id=None, config=None, schedule=None, id=None, created_at=None, updated_at=None, creator_id=None, next_trigger_at=None, project=None, creator=None, last_executions=None, local_vars_configuration=None):  # noqa: E501
        """DecoratedSchedule - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._project_id = None
        self._config = None
        self._schedule = None
        self._id = None
        self._created_at = None
        self._updated_at = None
        self._creator_id = None
        self._next_trigger_at = None
        self._project = None
        self._creator = None
        self._last_executions = None
        self.discriminator = None

        self.name = name
        if description is not None:
            self.description = description
        self.project_id = project_id
        self.config = config
        self.schedule = schedule
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.creator_id = creator_id
        if next_trigger_at is not None:
            self.next_trigger_at = next_trigger_at
        self.project = project
        self.creator = creator
        self.last_executions = last_executions

    @property
    def name(self):
        """Gets the name of this DecoratedSchedule.  # noqa: E501

        Name of the job  # noqa: E501

        :return: The name of this DecoratedSchedule.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DecoratedSchedule.

        Name of the job  # noqa: E501

        :param name: The name of this DecoratedSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this DecoratedSchedule.  # noqa: E501

        Description of the job  # noqa: E501

        :return: The description of this DecoratedSchedule.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DecoratedSchedule.

        Description of the job  # noqa: E501

        :param description: The description of this DecoratedSchedule.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_id(self):
        """Gets the project_id of this DecoratedSchedule.  # noqa: E501

        Id of the project this job will start clusters in  # noqa: E501

        :return: The project_id of this DecoratedSchedule.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this DecoratedSchedule.

        Id of the project this job will start clusters in  # noqa: E501

        :param project_id: The project_id of this DecoratedSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def config(self):
        """Gets the config of this DecoratedSchedule.  # noqa: E501

        The config that was used to create this job  # noqa: E501

        :return: The config of this DecoratedSchedule.  # noqa: E501
        :rtype: ProductionJobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this DecoratedSchedule.

        The config that was used to create this job  # noqa: E501

        :param config: The config of this DecoratedSchedule.  # noqa: E501
        :type: ProductionJobConfig
        """
        if self.local_vars_configuration.client_side_validation and config is None:  # noqa: E501
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

    @property
    def schedule(self):
        """Gets the schedule of this DecoratedSchedule.  # noqa: E501

        The configuration for this schedule  # noqa: E501

        :return: The schedule of this DecoratedSchedule.  # noqa: E501
        :rtype: ScheduleConfig
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this DecoratedSchedule.

        The configuration for this schedule  # noqa: E501

        :param schedule: The schedule of this DecoratedSchedule.  # noqa: E501
        :type: ScheduleConfig
        """
        if self.local_vars_configuration.client_side_validation and schedule is None:  # noqa: E501
            raise ValueError("Invalid value for `schedule`, must not be `None`")  # noqa: E501

        self._schedule = schedule

    @property
    def id(self):
        """Gets the id of this DecoratedSchedule.  # noqa: E501

        The id of this job  # noqa: E501

        :return: The id of this DecoratedSchedule.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DecoratedSchedule.

        The id of this job  # noqa: E501

        :param id: The id of this DecoratedSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this DecoratedSchedule.  # noqa: E501

        The time this job was created  # noqa: E501

        :return: The created_at of this DecoratedSchedule.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DecoratedSchedule.

        The time this job was created  # noqa: E501

        :param created_at: The created_at of this DecoratedSchedule.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this DecoratedSchedule.  # noqa: E501

        The time this job was last updated  # noqa: E501

        :return: The updated_at of this DecoratedSchedule.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DecoratedSchedule.

        The time this job was last updated  # noqa: E501

        :param updated_at: The updated_at of this DecoratedSchedule.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_at is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at

    @property
    def creator_id(self):
        """Gets the creator_id of this DecoratedSchedule.  # noqa: E501

        The id of the user who created this job  # noqa: E501

        :return: The creator_id of this DecoratedSchedule.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this DecoratedSchedule.

        The id of the user who created this job  # noqa: E501

        :param creator_id: The creator_id of this DecoratedSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def next_trigger_at(self):
        """Gets the next_trigger_at of this DecoratedSchedule.  # noqa: E501

        The next UTC timestamp at which this cron job will trigger.  # noqa: E501

        :return: The next_trigger_at of this DecoratedSchedule.  # noqa: E501
        :rtype: datetime
        """
        return self._next_trigger_at

    @next_trigger_at.setter
    def next_trigger_at(self, next_trigger_at):
        """Sets the next_trigger_at of this DecoratedSchedule.

        The next UTC timestamp at which this cron job will trigger.  # noqa: E501

        :param next_trigger_at: The next_trigger_at of this DecoratedSchedule.  # noqa: E501
        :type: datetime
        """

        self._next_trigger_at = next_trigger_at

    @property
    def project(self):
        """Gets the project of this DecoratedSchedule.  # noqa: E501

        The project in which this production job lives  # noqa: E501

        :return: The project of this DecoratedSchedule.  # noqa: E501
        :rtype: MiniProject
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this DecoratedSchedule.

        The project in which this production job lives  # noqa: E501

        :param project: The project of this DecoratedSchedule.  # noqa: E501
        :type: MiniProject
        """
        if self.local_vars_configuration.client_side_validation and project is None:  # noqa: E501
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

    @property
    def creator(self):
        """Gets the creator of this DecoratedSchedule.  # noqa: E501

        The creator of this job  # noqa: E501

        :return: The creator of this DecoratedSchedule.  # noqa: E501
        :rtype: MiniUser
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this DecoratedSchedule.

        The creator of this job  # noqa: E501

        :param creator: The creator of this DecoratedSchedule.  # noqa: E501
        :type: MiniUser
        """
        if self.local_vars_configuration.client_side_validation and creator is None:  # noqa: E501
            raise ValueError("Invalid value for `creator`, must not be `None`")  # noqa: E501

        self._creator = creator

    @property
    def last_executions(self):
        """Gets the last_executions of this DecoratedSchedule.  # noqa: E501


        :return: The last_executions of this DecoratedSchedule.  # noqa: E501
        :rtype: list[MiniProductionJob]
        """
        return self._last_executions

    @last_executions.setter
    def last_executions(self, last_executions):
        """Sets the last_executions of this DecoratedSchedule.


        :param last_executions: The last_executions of this DecoratedSchedule.  # noqa: E501
        :type: list[MiniProductionJob]
        """
        if self.local_vars_configuration.client_side_validation and last_executions is None:  # noqa: E501
            raise ValueError("Invalid value for `last_executions`, must not be `None`")  # noqa: E501

        self._last_executions = last_executions

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
        if not isinstance(other, DecoratedSchedule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DecoratedSchedule):
            return True

        return self.to_dict() != other.to_dict()
