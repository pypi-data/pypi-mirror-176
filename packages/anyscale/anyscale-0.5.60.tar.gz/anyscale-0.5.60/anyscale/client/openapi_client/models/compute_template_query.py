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


class ComputeTemplateQuery(object):
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
        'orgwide': 'bool',
        'project_id': 'str',
        'creator_id': 'str',
        'name': 'TextQuery',
        'include_anonymous': 'bool',
        'archive_status': 'ArchiveStatus'
    }

    attribute_map = {
        'orgwide': 'orgwide',
        'project_id': 'project_id',
        'creator_id': 'creator_id',
        'name': 'name',
        'include_anonymous': 'include_anonymous',
        'archive_status': 'archive_status'
    }

    def __init__(self, orgwide=False, project_id=None, creator_id=None, name=None, include_anonymous=False, archive_status=None, local_vars_configuration=None):  # noqa: E501
        """ComputeTemplateQuery - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._orgwide = None
        self._project_id = None
        self._creator_id = None
        self._name = None
        self._include_anonymous = None
        self._archive_status = None
        self.discriminator = None

        if orgwide is not None:
            self.orgwide = orgwide
        if project_id is not None:
            self.project_id = project_id
        if creator_id is not None:
            self.creator_id = creator_id
        if name is not None:
            self.name = name
        if include_anonymous is not None:
            self.include_anonymous = include_anonymous
        if archive_status is not None:
            self.archive_status = archive_status

    @property
    def orgwide(self):
        """Gets the orgwide of this ComputeTemplateQuery.  # noqa: E501


        :return: The orgwide of this ComputeTemplateQuery.  # noqa: E501
        :rtype: bool
        """
        return self._orgwide

    @orgwide.setter
    def orgwide(self, orgwide):
        """Sets the orgwide of this ComputeTemplateQuery.


        :param orgwide: The orgwide of this ComputeTemplateQuery.  # noqa: E501
        :type: bool
        """

        self._orgwide = orgwide

    @property
    def project_id(self):
        """Gets the project_id of this ComputeTemplateQuery.  # noqa: E501


        :return: The project_id of this ComputeTemplateQuery.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ComputeTemplateQuery.


        :param project_id: The project_id of this ComputeTemplateQuery.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def creator_id(self):
        """Gets the creator_id of this ComputeTemplateQuery.  # noqa: E501

        Filters Compute Templates by creator. This is only supported when `orgwide` is True.  # noqa: E501

        :return: The creator_id of this ComputeTemplateQuery.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this ComputeTemplateQuery.

        Filters Compute Templates by creator. This is only supported when `orgwide` is True.  # noqa: E501

        :param creator_id: The creator_id of this ComputeTemplateQuery.  # noqa: E501
        :type: str
        """

        self._creator_id = creator_id

    @property
    def name(self):
        """Gets the name of this ComputeTemplateQuery.  # noqa: E501

        Filters ComputeTemplates by name. If this field is absent, no filtering is done. For now, only equals match is supported when `orgwide` is False.  # noqa: E501

        :return: The name of this ComputeTemplateQuery.  # noqa: E501
        :rtype: TextQuery
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ComputeTemplateQuery.

        Filters ComputeTemplates by name. If this field is absent, no filtering is done. For now, only equals match is supported when `orgwide` is False.  # noqa: E501

        :param name: The name of this ComputeTemplateQuery.  # noqa: E501
        :type: TextQuery
        """

        self._name = name

    @property
    def include_anonymous(self):
        """Gets the include_anonymous of this ComputeTemplateQuery.  # noqa: E501

        Whether to include anonymous compute templates in the search. Anonymous compute templates are usually not shown in list views.  # noqa: E501

        :return: The include_anonymous of this ComputeTemplateQuery.  # noqa: E501
        :rtype: bool
        """
        return self._include_anonymous

    @include_anonymous.setter
    def include_anonymous(self, include_anonymous):
        """Sets the include_anonymous of this ComputeTemplateQuery.

        Whether to include anonymous compute templates in the search. Anonymous compute templates are usually not shown in list views.  # noqa: E501

        :param include_anonymous: The include_anonymous of this ComputeTemplateQuery.  # noqa: E501
        :type: bool
        """

        self._include_anonymous = include_anonymous

    @property
    def archive_status(self):
        """Gets the archive_status of this ComputeTemplateQuery.  # noqa: E501

        The archive status to filter by. Defaults to unarchived.  # noqa: E501

        :return: The archive_status of this ComputeTemplateQuery.  # noqa: E501
        :rtype: ArchiveStatus
        """
        return self._archive_status

    @archive_status.setter
    def archive_status(self, archive_status):
        """Sets the archive_status of this ComputeTemplateQuery.

        The archive status to filter by. Defaults to unarchived.  # noqa: E501

        :param archive_status: The archive_status of this ComputeTemplateQuery.  # noqa: E501
        :type: ArchiveStatus
        """

        self._archive_status = archive_status

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
        if not isinstance(other, ComputeTemplateQuery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComputeTemplateQuery):
            return True

        return self.to_dict() != other.to_dict()
