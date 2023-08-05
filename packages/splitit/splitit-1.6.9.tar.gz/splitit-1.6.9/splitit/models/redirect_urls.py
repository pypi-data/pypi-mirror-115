# coding: utf-8

"""
    splitit-web-api-public-sdk

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class RedirectUrls(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'succeeded': 'str',
        'canceled': 'str',
        'failed': 'str'
    }

    attribute_map = {
        'succeeded': 'Succeeded',
        'canceled': 'Canceled',
        'failed': 'Failed'
    }

    def __init__(self, succeeded=None, canceled=None, failed=None):  # noqa: E501
        """RedirectUrls - a model defined in Swagger"""  # noqa: E501

        self._succeeded = None
        self._canceled = None
        self._failed = None
        self.discriminator = None

        if succeeded is not None:
            self._succeeded = succeeded
        if canceled is not None:
            self._canceled = canceled
        if failed is not None:
            self._failed = failed

    @property
    def succeeded(self):
        """Gets the succeeded of this RedirectUrls.  # noqa: E501


        :return: The succeeded of this RedirectUrls.  # noqa: E501
        :rtype: str
        """
        return self._succeeded

    @succeeded.setter
    def succeeded(self, succeeded):
        """Sets the succeeded of this RedirectUrls.


        :param succeeded: The succeeded of this RedirectUrls.  # noqa: E501
        :type: str
        """

        self._succeeded = succeeded

    @property
    def canceled(self):
        """Gets the canceled of this RedirectUrls.  # noqa: E501


        :return: The canceled of this RedirectUrls.  # noqa: E501
        :rtype: str
        """
        return self._canceled

    @canceled.setter
    def canceled(self, canceled):
        """Sets the canceled of this RedirectUrls.


        :param canceled: The canceled of this RedirectUrls.  # noqa: E501
        :type: str
        """

        self._canceled = canceled

    @property
    def failed(self):
        """Gets the failed of this RedirectUrls.  # noqa: E501


        :return: The failed of this RedirectUrls.  # noqa: E501
        :rtype: str
        """
        return self._failed

    @failed.setter
    def failed(self, failed):
        """Sets the failed of this RedirectUrls.


        :param failed: The failed of this RedirectUrls.  # noqa: E501
        :type: str
        """

        self._failed = failed

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(RedirectUrls, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RedirectUrls):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
