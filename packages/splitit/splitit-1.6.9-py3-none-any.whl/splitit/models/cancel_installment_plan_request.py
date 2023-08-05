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


from .installment_plan_cancelation_reason import InstallmentPlanCancelationReason


class CancelInstallmentPlanRequest(object):
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
        'installment_plan_number': 'str',
        'refund_under_cancelation': 'RefundUnderCancelation',
        'cancelation_reason': 'InstallmentPlanCancelationReason',
        'partial_response_mapping': 'bool'
    }

    attribute_map = {
        'installment_plan_number': 'InstallmentPlanNumber',
        'refund_under_cancelation': 'RefundUnderCancelation',
        'cancelation_reason': 'CancelationReason',
        'partial_response_mapping': 'PartialResponseMapping'
    }

    def __init__(self, installment_plan_number=None, refund_under_cancelation=None, cancelation_reason=InstallmentPlanCancelationReason.OTHER, partial_response_mapping=None):  # noqa: E501
        """CancelInstallmentPlanRequest - a model defined in Swagger"""  # noqa: E501

        self._installment_plan_number = None
        self._refund_under_cancelation = None
        self._cancelation_reason = None
        self._partial_response_mapping = None
        self.discriminator = None

        if installment_plan_number is not None:
            self._installment_plan_number = installment_plan_number
        self._refund_under_cancelation = refund_under_cancelation
        if cancelation_reason is not None:
            self._cancelation_reason = cancelation_reason
        self._partial_response_mapping = partial_response_mapping

    @property
    def installment_plan_number(self):
        """Gets the installment_plan_number of this CancelInstallmentPlanRequest.  # noqa: E501


        :return: The installment_plan_number of this CancelInstallmentPlanRequest.  # noqa: E501
        :rtype: str
        """
        return self._installment_plan_number

    @installment_plan_number.setter
    def installment_plan_number(self, installment_plan_number):
        """Sets the installment_plan_number of this CancelInstallmentPlanRequest.


        :param installment_plan_number: The installment_plan_number of this CancelInstallmentPlanRequest.  # noqa: E501
        :type: str
        """

        self._installment_plan_number = installment_plan_number

    @property
    def refund_under_cancelation(self):
        """Gets the refund_under_cancelation of this CancelInstallmentPlanRequest.  # noqa: E501


        :return: The refund_under_cancelation of this CancelInstallmentPlanRequest.  # noqa: E501
        :rtype: RefundUnderCancelation
        """
        return self._refund_under_cancelation

    @refund_under_cancelation.setter
    def refund_under_cancelation(self, refund_under_cancelation):
        """Sets the refund_under_cancelation of this CancelInstallmentPlanRequest.


        :param refund_under_cancelation: The refund_under_cancelation of this CancelInstallmentPlanRequest.  # noqa: E501
        :type: RefundUnderCancelation
        """
        
        if refund_under_cancelation is None:
            raise ValueError("Invalid value for `refund_under_cancelation`, must not be `None`")  # noqa: E501

        self._refund_under_cancelation = refund_under_cancelation

    @property
    def cancelation_reason(self):
        """Gets the cancelation_reason of this CancelInstallmentPlanRequest.  # noqa: E501


        :return: The cancelation_reason of this CancelInstallmentPlanRequest.  # noqa: E501
        :rtype: InstallmentPlanCancelationReason
        """
        return self._cancelation_reason

    @cancelation_reason.setter
    def cancelation_reason(self, cancelation_reason):
        """Sets the cancelation_reason of this CancelInstallmentPlanRequest.


        :param cancelation_reason: The cancelation_reason of this CancelInstallmentPlanRequest.  # noqa: E501
        :type: InstallmentPlanCancelationReason
        """

        self._cancelation_reason = cancelation_reason

    @property
    def partial_response_mapping(self):
        """Gets the partial_response_mapping of this CancelInstallmentPlanRequest.  # noqa: E501


        :return: The partial_response_mapping of this CancelInstallmentPlanRequest.  # noqa: E501
        :rtype: bool
        """
        return self._partial_response_mapping

    @partial_response_mapping.setter
    def partial_response_mapping(self, partial_response_mapping):
        """Sets the partial_response_mapping of this CancelInstallmentPlanRequest.


        :param partial_response_mapping: The partial_response_mapping of this CancelInstallmentPlanRequest.  # noqa: E501
        :type: bool
        """
        partial_response_mapping = bool(partial_response_mapping)
        if partial_response_mapping is None:
            raise ValueError("Invalid value for `partial_response_mapping`, must not be `None`")  # noqa: E501

        self._partial_response_mapping = partial_response_mapping

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
        if issubclass(CancelInstallmentPlanRequest, dict):
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
        if not isinstance(other, CancelInstallmentPlanRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
