# coding: utf-8

"""
    Anyscale API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from anyscale_client.configuration import Configuration


class CreateSchedule(object):
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
        'config': 'CreateProductionJobConfig',
        'schedule': 'ScheduleConfig'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'project_id': 'project_id',
        'config': 'config',
        'schedule': 'schedule'
    }

    def __init__(self, name=None, description=None, project_id=None, config=None, schedule=None, local_vars_configuration=None):  # noqa: E501
        """CreateSchedule - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._project_id = None
        self._config = None
        self._schedule = None
        self.discriminator = None

        self.name = name
        if description is not None:
            self.description = description
        self.project_id = project_id
        self.config = config
        self.schedule = schedule

    @property
    def name(self):
        """Gets the name of this CreateSchedule.  # noqa: E501

        Name of the job  # noqa: E501

        :return: The name of this CreateSchedule.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateSchedule.

        Name of the job  # noqa: E501

        :param name: The name of this CreateSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateSchedule.  # noqa: E501

        Description of the job  # noqa: E501

        :return: The description of this CreateSchedule.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateSchedule.

        Description of the job  # noqa: E501

        :param description: The description of this CreateSchedule.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_id(self):
        """Gets the project_id of this CreateSchedule.  # noqa: E501

        Id of the project this job will start clusters in  # noqa: E501

        :return: The project_id of this CreateSchedule.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this CreateSchedule.

        Id of the project this job will start clusters in  # noqa: E501

        :param project_id: The project_id of this CreateSchedule.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def config(self):
        """Gets the config of this CreateSchedule.  # noqa: E501


        :return: The config of this CreateSchedule.  # noqa: E501
        :rtype: CreateProductionJobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this CreateSchedule.


        :param config: The config of this CreateSchedule.  # noqa: E501
        :type: CreateProductionJobConfig
        """
        if self.local_vars_configuration.client_side_validation and config is None:  # noqa: E501
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

    @property
    def schedule(self):
        """Gets the schedule of this CreateSchedule.  # noqa: E501

        The configuration for this schedule  # noqa: E501

        :return: The schedule of this CreateSchedule.  # noqa: E501
        :rtype: ScheduleConfig
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this CreateSchedule.

        The configuration for this schedule  # noqa: E501

        :param schedule: The schedule of this CreateSchedule.  # noqa: E501
        :type: ScheduleConfig
        """
        if self.local_vars_configuration.client_side_validation and schedule is None:  # noqa: E501
            raise ValueError("Invalid value for `schedule`, must not be `None`")  # noqa: E501

        self._schedule = schedule

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
        if not isinstance(other, CreateSchedule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateSchedule):
            return True

        return self.to_dict() != other.to_dict()
