# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.1296
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class AddPolicyCollectionToRoleRequest(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'policy_collections': 'list[PolicyCollectionId]'
    }

    attribute_map = {
        'policy_collections': 'policyCollections'
    }

    required_map = {
        'policy_collections': 'required'
    }

    def __init__(self, policy_collections=None):  # noqa: E501
        """
        AddPolicyCollectionToRoleRequest - a model defined in OpenAPI

        :param policy_collections:  Identifiers of policy collections to add to a role (required)
        :type policy_collections: list[finbourne_access.PolicyCollectionId]

        """  # noqa: E501

        self._policy_collections = None
        self.discriminator = None

        self.policy_collections = policy_collections

    @property
    def policy_collections(self):
        """Gets the policy_collections of this AddPolicyCollectionToRoleRequest.  # noqa: E501

        Identifiers of policy collections to add to a role  # noqa: E501

        :return: The policy_collections of this AddPolicyCollectionToRoleRequest.  # noqa: E501
        :rtype: list[PolicyCollectionId]
        """
        return self._policy_collections

    @policy_collections.setter
    def policy_collections(self, policy_collections):
        """Sets the policy_collections of this AddPolicyCollectionToRoleRequest.

        Identifiers of policy collections to add to a role  # noqa: E501

        :param policy_collections: The policy_collections of this AddPolicyCollectionToRoleRequest.  # noqa: E501
        :type: list[PolicyCollectionId]
        """
        if policy_collections is None:
            raise ValueError("Invalid value for `policy_collections`, must not be `None`")  # noqa: E501

        self._policy_collections = policy_collections

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
        if not isinstance(other, AddPolicyCollectionToRoleRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
