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


class RequestHeader(object):
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
        'touch_point': 'TouchPoint',
        'session_id': 'str',
        'api_key': 'str',
        'culture_name': 'str',
        'authentication_type': 'AuthenticationType'
    }

    attribute_map = {
        'touch_point': 'TouchPoint',
        'session_id': 'SessionId',
        'api_key': 'ApiKey',
        'culture_name': 'CultureName',
        'authentication_type': 'AuthenticationType'
    }

    def __init__(self, touch_point=None, session_id=None, api_key=None, culture_name=None, authentication_type=None):  # noqa: E501
        """RequestHeader - a model defined in Swagger"""  # noqa: E501

        self._touch_point = None
        self._session_id = None
        self._api_key = None
        self._culture_name = None
        self._authentication_type = None
        self.discriminator = None

        if touch_point is not None:
            self._touch_point = touch_point
        if session_id is not None:
            self._session_id = session_id
        if api_key is not None:
            self._api_key = api_key
        if culture_name is not None:
            self._culture_name = culture_name
        if authentication_type is not None:
            self._authentication_type = authentication_type

    @property
    def touch_point(self):
        """Gets the touch_point of this RequestHeader.  # noqa: E501


        :return: The touch_point of this RequestHeader.  # noqa: E501
        :rtype: TouchPoint
        """
        return self._touch_point

    @touch_point.setter
    def touch_point(self, touch_point):
        """Sets the touch_point of this RequestHeader.


        :param touch_point: The touch_point of this RequestHeader.  # noqa: E501
        :type: TouchPoint
        """

        self._touch_point = touch_point

    @property
    def session_id(self):
        """Gets the session_id of this RequestHeader.  # noqa: E501


        :return: The session_id of this RequestHeader.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this RequestHeader.


        :param session_id: The session_id of this RequestHeader.  # noqa: E501
        :type: str
        """

        self._session_id = session_id

    @property
    def api_key(self):
        """Gets the api_key of this RequestHeader.  # noqa: E501


        :return: The api_key of this RequestHeader.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this RequestHeader.


        :param api_key: The api_key of this RequestHeader.  # noqa: E501
        :type: str
        """

        self._api_key = api_key

    @property
    def culture_name(self):
        """Gets the culture_name of this RequestHeader.  # noqa: E501


        :return: The culture_name of this RequestHeader.  # noqa: E501
        :rtype: str
        """
        return self._culture_name

    @culture_name.setter
    def culture_name(self, culture_name):
        """Sets the culture_name of this RequestHeader.


        :param culture_name: The culture_name of this RequestHeader.  # noqa: E501
        :type: str
        """

        self._culture_name = culture_name

    @property
    def authentication_type(self):
        """Gets the authentication_type of this RequestHeader.  # noqa: E501


        :return: The authentication_type of this RequestHeader.  # noqa: E501
        :rtype: AuthenticationType
        """
        return self._authentication_type

    @authentication_type.setter
    def authentication_type(self, authentication_type):
        """Sets the authentication_type of this RequestHeader.


        :param authentication_type: The authentication_type of this RequestHeader.  # noqa: E501
        :type: AuthenticationType
        """

        self._authentication_type = authentication_type

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
        if issubclass(RequestHeader, dict):
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
        if not isinstance(other, RequestHeader):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
