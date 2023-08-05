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

class EffectiveDateHasQuality(object):
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
        'quality': 'DateQuality'
    }

    attribute_map = {
        'quality': 'quality'
    }

    required_map = {
        'quality': 'optional'
    }

    def __init__(self, quality=None):  # noqa: E501
        """
        EffectiveDateHasQuality - a model defined in OpenAPI

        :param quality: 
        :type quality: finbourne_access.DateQuality

        """  # noqa: E501

        self._quality = None
        self.discriminator = None

        if quality is not None:
            self.quality = quality

    @property
    def quality(self):
        """Gets the quality of this EffectiveDateHasQuality.  # noqa: E501


        :return: The quality of this EffectiveDateHasQuality.  # noqa: E501
        :rtype: DateQuality
        """
        return self._quality

    @quality.setter
    def quality(self, quality):
        """Sets the quality of this EffectiveDateHasQuality.


        :param quality: The quality of this EffectiveDateHasQuality.  # noqa: E501
        :type: DateQuality
        """

        self._quality = quality

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
        if not isinstance(other, EffectiveDateHasQuality):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
