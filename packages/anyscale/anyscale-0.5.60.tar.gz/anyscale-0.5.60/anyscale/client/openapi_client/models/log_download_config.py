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


class LogDownloadConfig(object):
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
        'next_page_token': 'str',
        'page_size': 'int',
        'ttl_seconds': 'int'
    }

    attribute_map = {
        'next_page_token': 'next_page_token',
        'page_size': 'page_size',
        'ttl_seconds': 'ttl_seconds'
    }

    def __init__(self, next_page_token=None, page_size=1000, ttl_seconds=600, local_vars_configuration=None):  # noqa: E501
        """LogDownloadConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._next_page_token = None
        self._page_size = None
        self._ttl_seconds = None
        self.discriminator = None

        if next_page_token is not None:
            self.next_page_token = next_page_token
        if page_size is not None:
            self.page_size = page_size
        if ttl_seconds is not None:
            self.ttl_seconds = ttl_seconds

    @property
    def next_page_token(self):
        """Gets the next_page_token of this LogDownloadConfig.  # noqa: E501

        The next page token (requests to the Log Download API are paginated).  # noqa: E501

        :return: The next_page_token of this LogDownloadConfig.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """Sets the next_page_token of this LogDownloadConfig.

        The next page token (requests to the Log Download API are paginated).  # noqa: E501

        :param next_page_token: The next_page_token of this LogDownloadConfig.  # noqa: E501
        :type: str
        """

        self._next_page_token = next_page_token

    @property
    def page_size(self):
        """Gets the page_size of this LogDownloadConfig.  # noqa: E501

        Page size (default: 1000 items/page).  # noqa: E501

        :return: The page_size of this LogDownloadConfig.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this LogDownloadConfig.

        Page size (default: 1000 items/page).  # noqa: E501

        :param page_size: The page_size of this LogDownloadConfig.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def ttl_seconds(self):
        """Gets the ttl_seconds of this LogDownloadConfig.  # noqa: E501

        The time-to-live of the presigned url in seconds (default: 600 seconds).  # noqa: E501

        :return: The ttl_seconds of this LogDownloadConfig.  # noqa: E501
        :rtype: int
        """
        return self._ttl_seconds

    @ttl_seconds.setter
    def ttl_seconds(self, ttl_seconds):
        """Sets the ttl_seconds of this LogDownloadConfig.

        The time-to-live of the presigned url in seconds (default: 600 seconds).  # noqa: E501

        :param ttl_seconds: The ttl_seconds of this LogDownloadConfig.  # noqa: E501
        :type: int
        """

        self._ttl_seconds = ttl_seconds

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
        if not isinstance(other, LogDownloadConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogDownloadConfig):
            return True

        return self.to_dict() != other.to_dict()
