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


class TimestampedLogsOutput(object):
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
        'lines': 'list[str]',
        'last_timestamp_ns': 'int'
    }

    attribute_map = {
        'lines': 'lines',
        'last_timestamp_ns': 'last_timestamp_ns'
    }

    def __init__(self, lines=None, last_timestamp_ns=None, local_vars_configuration=None):  # noqa: E501
        """TimestampedLogsOutput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._lines = None
        self._last_timestamp_ns = None
        self.discriminator = None

        self.lines = lines
        self.last_timestamp_ns = last_timestamp_ns

    @property
    def lines(self):
        """Gets the lines of this TimestampedLogsOutput.  # noqa: E501


        :return: The lines of this TimestampedLogsOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._lines

    @lines.setter
    def lines(self, lines):
        """Sets the lines of this TimestampedLogsOutput.


        :param lines: The lines of this TimestampedLogsOutput.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and lines is None:  # noqa: E501
            raise ValueError("Invalid value for `lines`, must not be `None`")  # noqa: E501

        self._lines = lines

    @property
    def last_timestamp_ns(self):
        """Gets the last_timestamp_ns of this TimestampedLogsOutput.  # noqa: E501


        :return: The last_timestamp_ns of this TimestampedLogsOutput.  # noqa: E501
        :rtype: int
        """
        return self._last_timestamp_ns

    @last_timestamp_ns.setter
    def last_timestamp_ns(self, last_timestamp_ns):
        """Sets the last_timestamp_ns of this TimestampedLogsOutput.


        :param last_timestamp_ns: The last_timestamp_ns of this TimestampedLogsOutput.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and last_timestamp_ns is None:  # noqa: E501
            raise ValueError("Invalid value for `last_timestamp_ns`, must not be `None`")  # noqa: E501

        self._last_timestamp_ns = last_timestamp_ns

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
        if not isinstance(other, TimestampedLogsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TimestampedLogsOutput):
            return True

        return self.to_dict() != other.to_dict()
