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


class WorkerNodeType(object):
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
        'instance_type': 'str',
        'resources': 'Resources',
        'aws_advanced_configurations': 'AWSNodeOptions',
        'gcp_advanced_configurations': 'GCPNodeOptions',
        'min_workers': 'int',
        'max_workers': 'int',
        'use_spot': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'instance_type': 'instance_type',
        'resources': 'resources',
        'aws_advanced_configurations': 'aws_advanced_configurations',
        'gcp_advanced_configurations': 'gcp_advanced_configurations',
        'min_workers': 'min_workers',
        'max_workers': 'max_workers',
        'use_spot': 'use_spot'
    }

    def __init__(self, name=None, instance_type=None, resources=None, aws_advanced_configurations=None, gcp_advanced_configurations=None, min_workers=None, max_workers=None, use_spot=False, local_vars_configuration=None):  # noqa: E501
        """WorkerNodeType - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._instance_type = None
        self._resources = None
        self._aws_advanced_configurations = None
        self._gcp_advanced_configurations = None
        self._min_workers = None
        self._max_workers = None
        self._use_spot = None
        self.discriminator = None

        self.name = name
        self.instance_type = instance_type
        if resources is not None:
            self.resources = resources
        if aws_advanced_configurations is not None:
            self.aws_advanced_configurations = aws_advanced_configurations
        if gcp_advanced_configurations is not None:
            self.gcp_advanced_configurations = gcp_advanced_configurations
        if min_workers is not None:
            self.min_workers = min_workers
        if max_workers is not None:
            self.max_workers = max_workers
        if use_spot is not None:
            self.use_spot = use_spot

    @property
    def name(self):
        """Gets the name of this WorkerNodeType.  # noqa: E501

        An arbitrary name for this node type, which will be registered with OSS available_node_types.   # noqa: E501

        :return: The name of this WorkerNodeType.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkerNodeType.

        An arbitrary name for this node type, which will be registered with OSS available_node_types.   # noqa: E501

        :param name: The name of this WorkerNodeType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def instance_type(self):
        """Gets the instance_type of this WorkerNodeType.  # noqa: E501

        The cloud provider instance type to use for this node.  # noqa: E501

        :return: The instance_type of this WorkerNodeType.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this WorkerNodeType.

        The cloud provider instance type to use for this node.  # noqa: E501

        :param instance_type: The instance_type of this WorkerNodeType.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and instance_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instance_type`, must not be `None`")  # noqa: E501

        self._instance_type = instance_type

    @property
    def resources(self):
        """Gets the resources of this WorkerNodeType.  # noqa: E501

        Declaration of node resources for Autoscaler.  # noqa: E501

        :return: The resources of this WorkerNodeType.  # noqa: E501
        :rtype: Resources
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this WorkerNodeType.

        Declaration of node resources for Autoscaler.  # noqa: E501

        :param resources: The resources of this WorkerNodeType.  # noqa: E501
        :type: Resources
        """

        self._resources = resources

    @property
    def aws_advanced_configurations(self):
        """Gets the aws_advanced_configurations of this WorkerNodeType.  # noqa: E501

        Additional AWS-specific configurations can be specified per node type and they will override the configuration specified for the whole cloud.  # noqa: E501

        :return: The aws_advanced_configurations of this WorkerNodeType.  # noqa: E501
        :rtype: AWSNodeOptions
        """
        return self._aws_advanced_configurations

    @aws_advanced_configurations.setter
    def aws_advanced_configurations(self, aws_advanced_configurations):
        """Sets the aws_advanced_configurations of this WorkerNodeType.

        Additional AWS-specific configurations can be specified per node type and they will override the configuration specified for the whole cloud.  # noqa: E501

        :param aws_advanced_configurations: The aws_advanced_configurations of this WorkerNodeType.  # noqa: E501
        :type: AWSNodeOptions
        """

        self._aws_advanced_configurations = aws_advanced_configurations

    @property
    def gcp_advanced_configurations(self):
        """Gets the gcp_advanced_configurations of this WorkerNodeType.  # noqa: E501

        Additional GCP-specific configurations can be specified per node type and they will override the configuration specified for the whole cloud.  # noqa: E501

        :return: The gcp_advanced_configurations of this WorkerNodeType.  # noqa: E501
        :rtype: GCPNodeOptions
        """
        return self._gcp_advanced_configurations

    @gcp_advanced_configurations.setter
    def gcp_advanced_configurations(self, gcp_advanced_configurations):
        """Sets the gcp_advanced_configurations of this WorkerNodeType.

        Additional GCP-specific configurations can be specified per node type and they will override the configuration specified for the whole cloud.  # noqa: E501

        :param gcp_advanced_configurations: The gcp_advanced_configurations of this WorkerNodeType.  # noqa: E501
        :type: GCPNodeOptions
        """

        self._gcp_advanced_configurations = gcp_advanced_configurations

    @property
    def min_workers(self):
        """Gets the min_workers of this WorkerNodeType.  # noqa: E501

        The minimum number of nodes of this type that Anyscale should spin up.  # noqa: E501

        :return: The min_workers of this WorkerNodeType.  # noqa: E501
        :rtype: int
        """
        return self._min_workers

    @min_workers.setter
    def min_workers(self, min_workers):
        """Sets the min_workers of this WorkerNodeType.

        The minimum number of nodes of this type that Anyscale should spin up.  # noqa: E501

        :param min_workers: The min_workers of this WorkerNodeType.  # noqa: E501
        :type: int
        """

        self._min_workers = min_workers

    @property
    def max_workers(self):
        """Gets the max_workers of this WorkerNodeType.  # noqa: E501

        The maximum number of nodes of this type that Anyscale should spin up.  # noqa: E501

        :return: The max_workers of this WorkerNodeType.  # noqa: E501
        :rtype: int
        """
        return self._max_workers

    @max_workers.setter
    def max_workers(self, max_workers):
        """Sets the max_workers of this WorkerNodeType.

        The maximum number of nodes of this type that Anyscale should spin up.  # noqa: E501

        :param max_workers: The max_workers of this WorkerNodeType.  # noqa: E501
        :type: int
        """

        self._max_workers = max_workers

    @property
    def use_spot(self):
        """Gets the use_spot of this WorkerNodeType.  # noqa: E501

        Whether or not to use spot instances for this node type.  # noqa: E501

        :return: The use_spot of this WorkerNodeType.  # noqa: E501
        :rtype: bool
        """
        return self._use_spot

    @use_spot.setter
    def use_spot(self, use_spot):
        """Sets the use_spot of this WorkerNodeType.

        Whether or not to use spot instances for this node type.  # noqa: E501

        :param use_spot: The use_spot of this WorkerNodeType.  # noqa: E501
        :type: bool
        """

        self._use_spot = use_spot

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
        if not isinstance(other, WorkerNodeType):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkerNodeType):
            return True

        return self.to_dict() != other.to_dict()
