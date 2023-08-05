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


class LogDetail(object):
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
        'download_url': 'str',
        'size': 'int'
    }

    attribute_map = {
        'name': 'name',
        'download_url': 'download_url',
        'size': 'size'
    }

    def __init__(self, name=None, download_url=None, size=None, local_vars_configuration=None):  # noqa: E501
        """LogDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._download_url = None
        self._size = None
        self.discriminator = None

        self.name = name
        self.download_url = download_url
        self.size = size

    @property
    def name(self):
        """Gets the name of this LogDetail.  # noqa: E501

        name of the log file.  # noqa: E501

        :return: The name of this LogDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LogDetail.

        name of the log file.  # noqa: E501

        :param name: The name of this LogDetail.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def download_url(self):
        """Gets the download_url of this LogDetail.  # noqa: E501

        download link for logs.  # noqa: E501

        :return: The download_url of this LogDetail.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this LogDetail.

        download link for logs.  # noqa: E501

        :param download_url: The download_url of this LogDetail.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and download_url is None:  # noqa: E501
            raise ValueError("Invalid value for `download_url`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                download_url is not None and len(download_url) > 2083):
            raise ValueError("Invalid value for `download_url`, length must be less than or equal to `2083`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                download_url is not None and len(download_url) < 1):
            raise ValueError("Invalid value for `download_url`, length must be greater than or equal to `1`")  # noqa: E501

        self._download_url = download_url

    @property
    def size(self):
        """Gets the size of this LogDetail.  # noqa: E501

        size of the log file.  # noqa: E501

        :return: The size of this LogDetail.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this LogDetail.

        size of the log file.  # noqa: E501

        :param size: The size of this LogDetail.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and size is None:  # noqa: E501
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501

        self._size = size

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
        if not isinstance(other, LogDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogDetail):
            return True

        return self.to_dict() != other.to_dict()
