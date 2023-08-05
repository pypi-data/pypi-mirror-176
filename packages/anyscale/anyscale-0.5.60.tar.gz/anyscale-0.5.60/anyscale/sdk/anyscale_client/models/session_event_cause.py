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


class SessionEventCause(object):
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
        'cause_user': 'str',
        'cause_system': 'str'
    }

    attribute_map = {
        'cause_user': 'cause_user',
        'cause_system': 'cause_system'
    }

    def __init__(self, cause_user=None, cause_system=None, local_vars_configuration=None):  # noqa: E501
        """SessionEventCause - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._cause_user = None
        self._cause_system = None
        self.discriminator = None

        if cause_user is not None:
            self.cause_user = cause_user
        if cause_system is not None:
            self.cause_system = cause_system

    @property
    def cause_user(self):
        """Gets the cause_user of this SessionEventCause.  # noqa: E501

        The username of the user who caused the session event.  # noqa: E501

        :return: The cause_user of this SessionEventCause.  # noqa: E501
        :rtype: str
        """
        return self._cause_user

    @cause_user.setter
    def cause_user(self, cause_user):
        """Sets the cause_user of this SessionEventCause.

        The username of the user who caused the session event.  # noqa: E501

        :param cause_user: The cause_user of this SessionEventCause.  # noqa: E501
        :type: str
        """

        self._cause_user = cause_user

    @property
    def cause_system(self):
        """Gets the cause_system of this SessionEventCause.  # noqa: E501

        The name of the internal anyscale system that caused the session event.  # noqa: E501

        :return: The cause_system of this SessionEventCause.  # noqa: E501
        :rtype: str
        """
        return self._cause_system

    @cause_system.setter
    def cause_system(self, cause_system):
        """Sets the cause_system of this SessionEventCause.

        The name of the internal anyscale system that caused the session event.  # noqa: E501

        :param cause_system: The cause_system of this SessionEventCause.  # noqa: E501
        :type: str
        """

        self._cause_system = cause_system

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
        if not isinstance(other, SessionEventCause):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SessionEventCause):
            return True

        return self.to_dict() != other.to_dict()
