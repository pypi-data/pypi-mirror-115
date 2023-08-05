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


class GetPGTLResponse(object):
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
        'response_header': 'ResponseHeader',
        'payment_gatewaytransaction_responses': 'dict(str, list[PgtlDto])'
    }

    attribute_map = {
        'response_header': 'ResponseHeader',
        'payment_gatewaytransaction_responses': 'paymentGatewaytransactionResponses'
    }

    def __init__(self, response_header=None, payment_gatewaytransaction_responses=None):  # noqa: E501
        """GetPGTLResponse - a model defined in Swagger"""  # noqa: E501

        self._response_header = None
        self._payment_gatewaytransaction_responses = None
        self.discriminator = None

        if response_header is not None:
            self._response_header = response_header
        if payment_gatewaytransaction_responses is not None:
            self._payment_gatewaytransaction_responses = payment_gatewaytransaction_responses

    @property
    def response_header(self):
        """Gets the response_header of this GetPGTLResponse.  # noqa: E501


        :return: The response_header of this GetPGTLResponse.  # noqa: E501
        :rtype: ResponseHeader
        """
        return self._response_header

    @response_header.setter
    def response_header(self, response_header):
        """Sets the response_header of this GetPGTLResponse.


        :param response_header: The response_header of this GetPGTLResponse.  # noqa: E501
        :type: ResponseHeader
        """

        self._response_header = response_header

    @property
    def payment_gatewaytransaction_responses(self):
        """Gets the payment_gatewaytransaction_responses of this GetPGTLResponse.  # noqa: E501


        :return: The payment_gatewaytransaction_responses of this GetPGTLResponse.  # noqa: E501
        :rtype: dict(str, list[PgtlDto])
        """
        return self._payment_gatewaytransaction_responses

    @payment_gatewaytransaction_responses.setter
    def payment_gatewaytransaction_responses(self, payment_gatewaytransaction_responses):
        """Sets the payment_gatewaytransaction_responses of this GetPGTLResponse.


        :param payment_gatewaytransaction_responses: The payment_gatewaytransaction_responses of this GetPGTLResponse.  # noqa: E501
        :type: dict(str, list[PgtlDto])
        """

        self._payment_gatewaytransaction_responses = payment_gatewaytransaction_responses

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
        if issubclass(GetPGTLResponse, dict):
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
        if not isinstance(other, GetPGTLResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
