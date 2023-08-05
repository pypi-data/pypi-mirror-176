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


class CloudConfig(object):
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
        'max_stopped_instances': 'int',
        'vpc_peering_ip_range': 'str',
        'vpc_peering_target_project_id': 'str',
        'vpc_peering_target_vpc_id': 'str'
    }

    attribute_map = {
        'max_stopped_instances': 'max_stopped_instances',
        'vpc_peering_ip_range': 'vpc_peering_ip_range',
        'vpc_peering_target_project_id': 'vpc_peering_target_project_id',
        'vpc_peering_target_vpc_id': 'vpc_peering_target_vpc_id'
    }

    def __init__(self, max_stopped_instances=0, vpc_peering_ip_range=None, vpc_peering_target_project_id=None, vpc_peering_target_vpc_id=None, local_vars_configuration=None):  # noqa: E501
        """CloudConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._max_stopped_instances = None
        self._vpc_peering_ip_range = None
        self._vpc_peering_target_project_id = None
        self._vpc_peering_target_vpc_id = None
        self.discriminator = None

        if max_stopped_instances is not None:
            self.max_stopped_instances = max_stopped_instances
        if vpc_peering_ip_range is not None:
            self.vpc_peering_ip_range = vpc_peering_ip_range
        if vpc_peering_target_project_id is not None:
            self.vpc_peering_target_project_id = vpc_peering_target_project_id
        if vpc_peering_target_vpc_id is not None:
            self.vpc_peering_target_vpc_id = vpc_peering_target_vpc_id

    @property
    def max_stopped_instances(self):
        """Gets the max_stopped_instances of this CloudConfig.  # noqa: E501

        Maximum number of instances that can be retained for reuse after a Cluster has terminated. This may help Clusters start up faster, but stopped instances will accrue some costs. Defaults to 0, which means no instances will be retained for reuse. A value of -1 means all instances will be retained.  # noqa: E501

        :return: The max_stopped_instances of this CloudConfig.  # noqa: E501
        :rtype: int
        """
        return self._max_stopped_instances

    @max_stopped_instances.setter
    def max_stopped_instances(self, max_stopped_instances):
        """Sets the max_stopped_instances of this CloudConfig.

        Maximum number of instances that can be retained for reuse after a Cluster has terminated. This may help Clusters start up faster, but stopped instances will accrue some costs. Defaults to 0, which means no instances will be retained for reuse. A value of -1 means all instances will be retained.  # noqa: E501

        :param max_stopped_instances: The max_stopped_instances of this CloudConfig.  # noqa: E501
        :type: int
        """

        self._max_stopped_instances = max_stopped_instances

    @property
    def vpc_peering_ip_range(self):
        """Gets the vpc_peering_ip_range of this CloudConfig.  # noqa: E501

        VPC IP range for this Cloud.  # noqa: E501

        :return: The vpc_peering_ip_range of this CloudConfig.  # noqa: E501
        :rtype: str
        """
        return self._vpc_peering_ip_range

    @vpc_peering_ip_range.setter
    def vpc_peering_ip_range(self, vpc_peering_ip_range):
        """Sets the vpc_peering_ip_range of this CloudConfig.

        VPC IP range for this Cloud.  # noqa: E501

        :param vpc_peering_ip_range: The vpc_peering_ip_range of this CloudConfig.  # noqa: E501
        :type: str
        """

        self._vpc_peering_ip_range = vpc_peering_ip_range

    @property
    def vpc_peering_target_project_id(self):
        """Gets the vpc_peering_target_project_id of this CloudConfig.  # noqa: E501

        Project ID of the VPC to peer with.  # noqa: E501

        :return: The vpc_peering_target_project_id of this CloudConfig.  # noqa: E501
        :rtype: str
        """
        return self._vpc_peering_target_project_id

    @vpc_peering_target_project_id.setter
    def vpc_peering_target_project_id(self, vpc_peering_target_project_id):
        """Sets the vpc_peering_target_project_id of this CloudConfig.

        Project ID of the VPC to peer with.  # noqa: E501

        :param vpc_peering_target_project_id: The vpc_peering_target_project_id of this CloudConfig.  # noqa: E501
        :type: str
        """

        self._vpc_peering_target_project_id = vpc_peering_target_project_id

    @property
    def vpc_peering_target_vpc_id(self):
        """Gets the vpc_peering_target_vpc_id of this CloudConfig.  # noqa: E501

        ID of the VPC to peer with.  # noqa: E501

        :return: The vpc_peering_target_vpc_id of this CloudConfig.  # noqa: E501
        :rtype: str
        """
        return self._vpc_peering_target_vpc_id

    @vpc_peering_target_vpc_id.setter
    def vpc_peering_target_vpc_id(self, vpc_peering_target_vpc_id):
        """Sets the vpc_peering_target_vpc_id of this CloudConfig.

        ID of the VPC to peer with.  # noqa: E501

        :param vpc_peering_target_vpc_id: The vpc_peering_target_vpc_id of this CloudConfig.  # noqa: E501
        :type: str
        """

        self._vpc_peering_target_vpc_id = vpc_peering_target_vpc_id

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
        if not isinstance(other, CloudConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CloudConfig):
            return True

        return self.to_dict() != other.to_dict()
