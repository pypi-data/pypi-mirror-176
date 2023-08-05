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


class AllocationSetRequest(object):
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
        'allocation_requests': 'list[AllocationRequest]'
    }

    attribute_map = {
        'allocation_requests': 'allocationRequests'
    }

    required_map = {
        'allocation_requests': 'optional'
    }

    def __init__(self, allocation_requests=None, local_vars_configuration=None):  # noqa: E501
        """AllocationSetRequest - a model defined in OpenAPI"
        
        :param allocation_requests:  A collection of AllocationRequests.
        :type allocation_requests: list[lusid.AllocationRequest]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._allocation_requests = None
        self.discriminator = None

        self.allocation_requests = allocation_requests

    @property
    def allocation_requests(self):
        """Gets the allocation_requests of this AllocationSetRequest.  # noqa: E501

        A collection of AllocationRequests.  # noqa: E501

        :return: The allocation_requests of this AllocationSetRequest.  # noqa: E501
        :rtype: list[lusid.AllocationRequest]
        """
        return self._allocation_requests

    @allocation_requests.setter
    def allocation_requests(self, allocation_requests):
        """Sets the allocation_requests of this AllocationSetRequest.

        A collection of AllocationRequests.  # noqa: E501

        :param allocation_requests: The allocation_requests of this AllocationSetRequest.  # noqa: E501
        :type allocation_requests: list[lusid.AllocationRequest]
        """

        self._allocation_requests = allocation_requests

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
        if not isinstance(other, AllocationSetRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AllocationSetRequest):
            return True

        return self.to_dict() != other.to_dict()
