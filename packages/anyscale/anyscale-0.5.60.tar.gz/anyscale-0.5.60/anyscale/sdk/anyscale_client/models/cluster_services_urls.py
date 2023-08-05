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


class ClusterServicesUrls(object):
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
        'webterminal_auth_url': 'str',
        'metrics_dashboard_url': 'str',
        'persistent_metrics_url': 'str',
        'connect_url': 'str',
        'jupyter_notebook_url': 'str',
        'ray_dashboard_url': 'str',
        'service_proxy_url': 'str',
        'user_service_url': 'str'
    }

    attribute_map = {
        'webterminal_auth_url': 'webterminal_auth_url',
        'metrics_dashboard_url': 'metrics_dashboard_url',
        'persistent_metrics_url': 'persistent_metrics_url',
        'connect_url': 'connect_url',
        'jupyter_notebook_url': 'jupyter_notebook_url',
        'ray_dashboard_url': 'ray_dashboard_url',
        'service_proxy_url': 'service_proxy_url',
        'user_service_url': 'user_service_url'
    }

    def __init__(self, webterminal_auth_url=None, metrics_dashboard_url=None, persistent_metrics_url=None, connect_url=None, jupyter_notebook_url=None, ray_dashboard_url=None, service_proxy_url=None, user_service_url=None, local_vars_configuration=None):  # noqa: E501
        """ClusterServicesUrls - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._webterminal_auth_url = None
        self._metrics_dashboard_url = None
        self._persistent_metrics_url = None
        self._connect_url = None
        self._jupyter_notebook_url = None
        self._ray_dashboard_url = None
        self._service_proxy_url = None
        self._user_service_url = None
        self.discriminator = None

        if webterminal_auth_url is not None:
            self.webterminal_auth_url = webterminal_auth_url
        if metrics_dashboard_url is not None:
            self.metrics_dashboard_url = metrics_dashboard_url
        if persistent_metrics_url is not None:
            self.persistent_metrics_url = persistent_metrics_url
        if connect_url is not None:
            self.connect_url = connect_url
        if jupyter_notebook_url is not None:
            self.jupyter_notebook_url = jupyter_notebook_url
        if ray_dashboard_url is not None:
            self.ray_dashboard_url = ray_dashboard_url
        if service_proxy_url is not None:
            self.service_proxy_url = service_proxy_url
        if user_service_url is not None:
            self.user_service_url = user_service_url

    @property
    def webterminal_auth_url(self):
        """Gets the webterminal_auth_url of this ClusterServicesUrls.  # noqa: E501

        URL to authenticate with the webterminal  # noqa: E501

        :return: The webterminal_auth_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._webterminal_auth_url

    @webterminal_auth_url.setter
    def webterminal_auth_url(self, webterminal_auth_url):
        """Sets the webterminal_auth_url of this ClusterServicesUrls.

        URL to authenticate with the webterminal  # noqa: E501

        :param webterminal_auth_url: The webterminal_auth_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._webterminal_auth_url = webterminal_auth_url

    @property
    def metrics_dashboard_url(self):
        """Gets the metrics_dashboard_url of this ClusterServicesUrls.  # noqa: E501

        URL for Grafana (metrics) dashboard in the running cluster state.  # noqa: E501

        :return: The metrics_dashboard_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._metrics_dashboard_url

    @metrics_dashboard_url.setter
    def metrics_dashboard_url(self, metrics_dashboard_url):
        """Sets the metrics_dashboard_url of this ClusterServicesUrls.

        URL for Grafana (metrics) dashboard in the running cluster state.  # noqa: E501

        :param metrics_dashboard_url: The metrics_dashboard_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._metrics_dashboard_url = metrics_dashboard_url

    @property
    def persistent_metrics_url(self):
        """Gets the persistent_metrics_url of this ClusterServicesUrls.  # noqa: E501

        URL for the persistent Grafana (metrics) dashboard in the non-running cluster state.  # noqa: E501

        :return: The persistent_metrics_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._persistent_metrics_url

    @persistent_metrics_url.setter
    def persistent_metrics_url(self, persistent_metrics_url):
        """Sets the persistent_metrics_url of this ClusterServicesUrls.

        URL for the persistent Grafana (metrics) dashboard in the non-running cluster state.  # noqa: E501

        :param persistent_metrics_url: The persistent_metrics_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._persistent_metrics_url = persistent_metrics_url

    @property
    def connect_url(self):
        """Gets the connect_url of this ClusterServicesUrls.  # noqa: E501

        URL for Anyscale connect.  # noqa: E501

        :return: The connect_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._connect_url

    @connect_url.setter
    def connect_url(self, connect_url):
        """Sets the connect_url of this ClusterServicesUrls.

        URL for Anyscale connect.  # noqa: E501

        :param connect_url: The connect_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._connect_url = connect_url

    @property
    def jupyter_notebook_url(self):
        """Gets the jupyter_notebook_url of this ClusterServicesUrls.  # noqa: E501

        URL for Jupyter Lab.  # noqa: E501

        :return: The jupyter_notebook_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._jupyter_notebook_url

    @jupyter_notebook_url.setter
    def jupyter_notebook_url(self, jupyter_notebook_url):
        """Sets the jupyter_notebook_url of this ClusterServicesUrls.

        URL for Jupyter Lab.  # noqa: E501

        :param jupyter_notebook_url: The jupyter_notebook_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._jupyter_notebook_url = jupyter_notebook_url

    @property
    def ray_dashboard_url(self):
        """Gets the ray_dashboard_url of this ClusterServicesUrls.  # noqa: E501

        URL for Ray dashboard.  # noqa: E501

        :return: The ray_dashboard_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._ray_dashboard_url

    @ray_dashboard_url.setter
    def ray_dashboard_url(self, ray_dashboard_url):
        """Sets the ray_dashboard_url of this ClusterServicesUrls.

        URL for Ray dashboard.  # noqa: E501

        :param ray_dashboard_url: The ray_dashboard_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._ray_dashboard_url = ray_dashboard_url

    @property
    def service_proxy_url(self):
        """Gets the service_proxy_url of this ClusterServicesUrls.  # noqa: E501

        URL for web services proxy (e.g. jupyter, tensorboard, etc).  # noqa: E501

        :return: The service_proxy_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._service_proxy_url

    @service_proxy_url.setter
    def service_proxy_url(self, service_proxy_url):
        """Sets the service_proxy_url of this ClusterServicesUrls.

        URL for web services proxy (e.g. jupyter, tensorboard, etc).  # noqa: E501

        :param service_proxy_url: The service_proxy_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._service_proxy_url = service_proxy_url

    @property
    def user_service_url(self):
        """Gets the user_service_url of this ClusterServicesUrls.  # noqa: E501

        URL to access user services (e.g. Ray Serve)  # noqa: E501

        :return: The user_service_url of this ClusterServicesUrls.  # noqa: E501
        :rtype: str
        """
        return self._user_service_url

    @user_service_url.setter
    def user_service_url(self, user_service_url):
        """Sets the user_service_url of this ClusterServicesUrls.

        URL to access user services (e.g. Ray Serve)  # noqa: E501

        :param user_service_url: The user_service_url of this ClusterServicesUrls.  # noqa: E501
        :type: str
        """

        self._user_service_url = user_service_url

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
        if not isinstance(other, ClusterServicesUrls):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClusterServicesUrls):
            return True

        return self.to_dict() != other.to_dict()
