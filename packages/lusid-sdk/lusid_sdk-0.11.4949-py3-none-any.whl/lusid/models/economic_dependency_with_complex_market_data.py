# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.4949
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class EconomicDependencyWithComplexMarketData(object):
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
        'economic_dependency': 'EconomicDependency',
        'complex_market_data': 'ComplexMarketData'
    }

    attribute_map = {
        'economic_dependency': 'economicDependency',
        'complex_market_data': 'complexMarketData'
    }

    required_map = {
        'economic_dependency': 'required',
        'complex_market_data': 'required'
    }

    def __init__(self, economic_dependency=None, complex_market_data=None, local_vars_configuration=None):  # noqa: E501
        """EconomicDependencyWithComplexMarketData - a model defined in OpenAPI"
        
        :param economic_dependency:  (required)
        :type economic_dependency: lusid.EconomicDependency
        :param complex_market_data:  (required)
        :type complex_market_data: lusid.ComplexMarketData

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._economic_dependency = None
        self._complex_market_data = None
        self.discriminator = None

        self.economic_dependency = economic_dependency
        self.complex_market_data = complex_market_data

    @property
    def economic_dependency(self):
        """Gets the economic_dependency of this EconomicDependencyWithComplexMarketData.  # noqa: E501


        :return: The economic_dependency of this EconomicDependencyWithComplexMarketData.  # noqa: E501
        :rtype: lusid.EconomicDependency
        """
        return self._economic_dependency

    @economic_dependency.setter
    def economic_dependency(self, economic_dependency):
        """Sets the economic_dependency of this EconomicDependencyWithComplexMarketData.


        :param economic_dependency: The economic_dependency of this EconomicDependencyWithComplexMarketData.  # noqa: E501
        :type economic_dependency: lusid.EconomicDependency
        """
        if self.local_vars_configuration.client_side_validation and economic_dependency is None:  # noqa: E501
            raise ValueError("Invalid value for `economic_dependency`, must not be `None`")  # noqa: E501

        self._economic_dependency = economic_dependency

    @property
    def complex_market_data(self):
        """Gets the complex_market_data of this EconomicDependencyWithComplexMarketData.  # noqa: E501


        :return: The complex_market_data of this EconomicDependencyWithComplexMarketData.  # noqa: E501
        :rtype: lusid.ComplexMarketData
        """
        return self._complex_market_data

    @complex_market_data.setter
    def complex_market_data(self, complex_market_data):
        """Sets the complex_market_data of this EconomicDependencyWithComplexMarketData.


        :param complex_market_data: The complex_market_data of this EconomicDependencyWithComplexMarketData.  # noqa: E501
        :type complex_market_data: lusid.ComplexMarketData
        """
        if self.local_vars_configuration.client_side_validation and complex_market_data is None:  # noqa: E501
            raise ValueError("Invalid value for `complex_market_data`, must not be `None`")  # noqa: E501

        self._complex_market_data = complex_market_data

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EconomicDependencyWithComplexMarketData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EconomicDependencyWithComplexMarketData):
            return True

        return self.to_dict() != other.to_dict()
