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


class Project(object):
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
        'cloud_id': 'str',
        'initial_cluster_config': 'str',
        'id': 'str',
        'created_at': 'datetime',
        'creator_id': 'str',
        'is_owner': 'bool',
        'directory_name': 'str',
        'cloud': 'str',
        'last_used_cloud_id': 'str',
        'active_sessions': 'int',
        'last_activity_at': 'datetime',
        'owners': 'list[MiniUser]',
        'is_default': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'cloud_id': 'cloud_id',
        'initial_cluster_config': 'initial_cluster_config',
        'id': 'id',
        'created_at': 'created_at',
        'creator_id': 'creator_id',
        'is_owner': 'is_owner',
        'directory_name': 'directory_name',
        'cloud': 'cloud',
        'last_used_cloud_id': 'last_used_cloud_id',
        'active_sessions': 'active_sessions',
        'last_activity_at': 'last_activity_at',
        'owners': 'owners',
        'is_default': 'is_default'
    }

    def __init__(self, name=None, description=None, cloud_id=None, initial_cluster_config=None, id=None, created_at=None, creator_id=None, is_owner=None, directory_name=None, cloud=None, last_used_cloud_id=None, active_sessions=None, last_activity_at=None, owners=[], is_default=None, local_vars_configuration=None):  # noqa: E501
        """Project - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._cloud_id = None
        self._initial_cluster_config = None
        self._id = None
        self._created_at = None
        self._creator_id = None
        self._is_owner = None
        self._directory_name = None
        self._cloud = None
        self._last_used_cloud_id = None
        self._active_sessions = None
        self._last_activity_at = None
        self._owners = None
        self._is_default = None
        self.discriminator = None

        self.name = name
        self.description = description
        if cloud_id is not None:
            self.cloud_id = cloud_id
        if initial_cluster_config is not None:
            self.initial_cluster_config = initial_cluster_config
        self.id = id
        self.created_at = created_at
        if creator_id is not None:
            self.creator_id = creator_id
        self.is_owner = is_owner
        self.directory_name = directory_name
        if cloud is not None:
            self.cloud = cloud
        if last_used_cloud_id is not None:
            self.last_used_cloud_id = last_used_cloud_id
        self.active_sessions = active_sessions
        self.last_activity_at = last_activity_at
        if owners is not None:
            self.owners = owners
        self.is_default = is_default

    @property
    def name(self):
        """Gets the name of this Project.  # noqa: E501


        :return: The name of this Project.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Project.


        :param name: The name of this Project.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Project.  # noqa: E501


        :return: The description of this Project.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Project.


        :param description: The description of this Project.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def cloud_id(self):
        """Gets the cloud_id of this Project.  # noqa: E501


        :return: The cloud_id of this Project.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this Project.


        :param cloud_id: The cloud_id of this Project.  # noqa: E501
        :type: str
        """

        self._cloud_id = cloud_id

    @property
    def initial_cluster_config(self):
        """Gets the initial_cluster_config of this Project.  # noqa: E501


        :return: The initial_cluster_config of this Project.  # noqa: E501
        :rtype: str
        """
        return self._initial_cluster_config

    @initial_cluster_config.setter
    def initial_cluster_config(self, initial_cluster_config):
        """Sets the initial_cluster_config of this Project.


        :param initial_cluster_config: The initial_cluster_config of this Project.  # noqa: E501
        :type: str
        """

        self._initial_cluster_config = initial_cluster_config

    @property
    def id(self):
        """Gets the id of this Project.  # noqa: E501


        :return: The id of this Project.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Project.


        :param id: The id of this Project.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this Project.  # noqa: E501


        :return: The created_at of this Project.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Project.


        :param created_at: The created_at of this Project.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def creator_id(self):
        """Gets the creator_id of this Project.  # noqa: E501


        :return: The creator_id of this Project.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this Project.


        :param creator_id: The creator_id of this Project.  # noqa: E501
        :type: str
        """

        self._creator_id = creator_id

    @property
    def is_owner(self):
        """Gets the is_owner of this Project.  # noqa: E501


        :return: The is_owner of this Project.  # noqa: E501
        :rtype: bool
        """
        return self._is_owner

    @is_owner.setter
    def is_owner(self, is_owner):
        """Sets the is_owner of this Project.


        :param is_owner: The is_owner of this Project.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and is_owner is None:  # noqa: E501
            raise ValueError("Invalid value for `is_owner`, must not be `None`")  # noqa: E501

        self._is_owner = is_owner

    @property
    def directory_name(self):
        """Gets the directory_name of this Project.  # noqa: E501


        :return: The directory_name of this Project.  # noqa: E501
        :rtype: str
        """
        return self._directory_name

    @directory_name.setter
    def directory_name(self, directory_name):
        """Sets the directory_name of this Project.


        :param directory_name: The directory_name of this Project.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and directory_name is None:  # noqa: E501
            raise ValueError("Invalid value for `directory_name`, must not be `None`")  # noqa: E501

        self._directory_name = directory_name

    @property
    def cloud(self):
        """Gets the cloud of this Project.  # noqa: E501


        :return: The cloud of this Project.  # noqa: E501
        :rtype: str
        """
        return self._cloud

    @cloud.setter
    def cloud(self, cloud):
        """Sets the cloud of this Project.


        :param cloud: The cloud of this Project.  # noqa: E501
        :type: str
        """

        self._cloud = cloud

    @property
    def last_used_cloud_id(self):
        """Gets the last_used_cloud_id of this Project.  # noqa: E501


        :return: The last_used_cloud_id of this Project.  # noqa: E501
        :rtype: str
        """
        return self._last_used_cloud_id

    @last_used_cloud_id.setter
    def last_used_cloud_id(self, last_used_cloud_id):
        """Sets the last_used_cloud_id of this Project.


        :param last_used_cloud_id: The last_used_cloud_id of this Project.  # noqa: E501
        :type: str
        """

        self._last_used_cloud_id = last_used_cloud_id

    @property
    def active_sessions(self):
        """Gets the active_sessions of this Project.  # noqa: E501

        Read only. Number of active sessions for this project.  # noqa: E501

        :return: The active_sessions of this Project.  # noqa: E501
        :rtype: int
        """
        return self._active_sessions

    @active_sessions.setter
    def active_sessions(self, active_sessions):
        """Sets the active_sessions of this Project.

        Read only. Number of active sessions for this project.  # noqa: E501

        :param active_sessions: The active_sessions of this Project.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and active_sessions is None:  # noqa: E501
            raise ValueError("Invalid value for `active_sessions`, must not be `None`")  # noqa: E501

        self._active_sessions = active_sessions

    @property
    def last_activity_at(self):
        """Gets the last_activity_at of this Project.  # noqa: E501

        Read only. The most recent activity for this project. This is based on the most recently created sessions  # noqa: E501

        :return: The last_activity_at of this Project.  # noqa: E501
        :rtype: datetime
        """
        return self._last_activity_at

    @last_activity_at.setter
    def last_activity_at(self, last_activity_at):
        """Sets the last_activity_at of this Project.

        Read only. The most recent activity for this project. This is based on the most recently created sessions  # noqa: E501

        :param last_activity_at: The last_activity_at of this Project.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and last_activity_at is None:  # noqa: E501
            raise ValueError("Invalid value for `last_activity_at`, must not be `None`")  # noqa: E501

        self._last_activity_at = last_activity_at

    @property
    def owners(self):
        """Gets the owners of this Project.  # noqa: E501

        List of Users who have Owner level permissions for this Project.  # noqa: E501

        :return: The owners of this Project.  # noqa: E501
        :rtype: list[MiniUser]
        """
        return self._owners

    @owners.setter
    def owners(self, owners):
        """Sets the owners of this Project.

        List of Users who have Owner level permissions for this Project.  # noqa: E501

        :param owners: The owners of this Project.  # noqa: E501
        :type: list[MiniUser]
        """

        self._owners = owners

    @property
    def is_default(self):
        """Gets the is_default of this Project.  # noqa: E501

        True if this project is the default project for the organization.  # noqa: E501

        :return: The is_default of this Project.  # noqa: E501
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """Sets the is_default of this Project.

        True if this project is the default project for the organization.  # noqa: E501

        :param is_default: The is_default of this Project.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and is_default is None:  # noqa: E501
            raise ValueError("Invalid value for `is_default`, must not be `None`")  # noqa: E501

        self._is_default = is_default

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
        if not isinstance(other, Project):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Project):
            return True

        return self.to_dict() != other.to_dict()
