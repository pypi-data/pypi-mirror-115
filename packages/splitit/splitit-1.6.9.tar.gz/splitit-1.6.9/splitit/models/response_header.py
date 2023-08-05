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


class ResponseHeader(object):
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
        'succeeded': 'bool',
        'errors': 'list[Error]',
        'trace_id': 'str'
    }

    attribute_map = {
        'succeeded': 'Succeeded',
        'errors': 'Errors',
        'trace_id': 'TraceId'
    }

    def __init__(self, succeeded=None, errors=None, trace_id=None):  # noqa: E501
        """ResponseHeader - a model defined in Swagger"""  # noqa: E501

        self._succeeded = None
        self._errors = None
        self._trace_id = None
        self.discriminator = None

        self._succeeded = succeeded
        if errors is not None:
            self._errors = errors
        if trace_id is not None:
            self._trace_id = trace_id

    @property
    def succeeded(self):
        """Gets the succeeded of this ResponseHeader.  # noqa: E501


        :return: The succeeded of this ResponseHeader.  # noqa: E501
        :rtype: bool
        """
        return self._succeeded

    @succeeded.setter
    def succeeded(self, succeeded):
        """Sets the succeeded of this ResponseHeader.


        :param succeeded: The succeeded of this ResponseHeader.  # noqa: E501
        :type: bool
        """
        succeeded = bool(succeeded)
        if succeeded is None:
            raise ValueError("Invalid value for `succeeded`, must not be `None`")  # noqa: E501

        self._succeeded = succeeded

    @property
    def errors(self):
        """Gets the errors of this ResponseHeader.  # noqa: E501


        :return: The errors of this ResponseHeader.  # noqa: E501
        :rtype: list[Error]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this ResponseHeader.


        :param errors: The errors of this ResponseHeader.  # noqa: E501
        :type: list[Error]
        """

        self._errors = errors

    @property
    def trace_id(self):
        """Gets the trace_id of this ResponseHeader.  # noqa: E501


        :return: The trace_id of this ResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._trace_id

    @trace_id.setter
    def trace_id(self, trace_id):
        """Sets the trace_id of this ResponseHeader.


        :param trace_id: The trace_id of this ResponseHeader.  # noqa: E501
        :type: str
        """

        self._trace_id = trace_id

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
        if issubclass(ResponseHeader, dict):
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
        if not isinstance(other, ResponseHeader):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
