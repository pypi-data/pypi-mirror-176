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


class AddressDefinition(object):
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
        'display_name': 'str',
        'type': 'str',
        'description': 'str',
        'life_cycle_status': 'str',
        'removal_date': 'datetime',
        'documentation_link': 'str'
    }

    attribute_map = {
        'display_name': 'displayName',
        'type': 'type',
        'description': 'description',
        'life_cycle_status': 'lifeCycleStatus',
        'removal_date': 'removalDate',
        'documentation_link': 'documentationLink'
    }

    required_map = {
        'display_name': 'optional',
        'type': 'optional',
        'description': 'optional',
        'life_cycle_status': 'optional',
        'removal_date': 'optional',
        'documentation_link': 'optional'
    }

    def __init__(self, display_name=None, type=None, description=None, life_cycle_status=None, removal_date=None, documentation_link=None, local_vars_configuration=None):  # noqa: E501
        """AddressDefinition - a model defined in OpenAPI"
        
        :param display_name:  The display name of the address key.
        :type display_name: str
        :param type:  The available values are: String, Int, Decimal, DateTime, Boolean, ResultValue, Result0D, Json
        :type type: str
        :param description:  The description for this result.
        :type description: str
        :param life_cycle_status:  What is the status of the address path. If it is not Production then it might be removed at some point in the future.  See the removal date for the likely timing of that if any.
        :type life_cycle_status: str
        :param removal_date:  If the life-cycle status of the address is Deprecated then this is the date at which support of the address will be suspended.  After that date it will be removed at the earliest possible point subject to any specific contractual support and development constraints.
        :type removal_date: datetime
        :param documentation_link:  Contains a link to the documentation for this AddressDefinition in KnowledgeBase.
        :type documentation_link: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._display_name = None
        self._type = None
        self._description = None
        self._life_cycle_status = None
        self._removal_date = None
        self._documentation_link = None
        self.discriminator = None

        self.display_name = display_name
        if type is not None:
            self.type = type
        self.description = description
        self.life_cycle_status = life_cycle_status
        self.removal_date = removal_date
        self.documentation_link = documentation_link

    @property
    def display_name(self):
        """Gets the display_name of this AddressDefinition.  # noqa: E501

        The display name of the address key.  # noqa: E501

        :return: The display_name of this AddressDefinition.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this AddressDefinition.

        The display name of the address key.  # noqa: E501

        :param display_name: The display_name of this AddressDefinition.  # noqa: E501
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def type(self):
        """Gets the type of this AddressDefinition.  # noqa: E501

        The available values are: String, Int, Decimal, DateTime, Boolean, ResultValue, Result0D, Json  # noqa: E501

        :return: The type of this AddressDefinition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AddressDefinition.

        The available values are: String, Int, Decimal, DateTime, Boolean, ResultValue, Result0D, Json  # noqa: E501

        :param type: The type of this AddressDefinition.  # noqa: E501
        :type type: str
        """
        allowed_values = ["String", "Int", "Decimal", "DateTime", "Boolean", "ResultValue", "Result0D", "Json"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def description(self):
        """Gets the description of this AddressDefinition.  # noqa: E501

        The description for this result.  # noqa: E501

        :return: The description of this AddressDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AddressDefinition.

        The description for this result.  # noqa: E501

        :param description: The description of this AddressDefinition.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def life_cycle_status(self):
        """Gets the life_cycle_status of this AddressDefinition.  # noqa: E501

        What is the status of the address path. If it is not Production then it might be removed at some point in the future.  See the removal date for the likely timing of that if any.  # noqa: E501

        :return: The life_cycle_status of this AddressDefinition.  # noqa: E501
        :rtype: str
        """
        return self._life_cycle_status

    @life_cycle_status.setter
    def life_cycle_status(self, life_cycle_status):
        """Sets the life_cycle_status of this AddressDefinition.

        What is the status of the address path. If it is not Production then it might be removed at some point in the future.  See the removal date for the likely timing of that if any.  # noqa: E501

        :param life_cycle_status: The life_cycle_status of this AddressDefinition.  # noqa: E501
        :type life_cycle_status: str
        """

        self._life_cycle_status = life_cycle_status

    @property
    def removal_date(self):
        """Gets the removal_date of this AddressDefinition.  # noqa: E501

        If the life-cycle status of the address is Deprecated then this is the date at which support of the address will be suspended.  After that date it will be removed at the earliest possible point subject to any specific contractual support and development constraints.  # noqa: E501

        :return: The removal_date of this AddressDefinition.  # noqa: E501
        :rtype: datetime
        """
        return self._removal_date

    @removal_date.setter
    def removal_date(self, removal_date):
        """Sets the removal_date of this AddressDefinition.

        If the life-cycle status of the address is Deprecated then this is the date at which support of the address will be suspended.  After that date it will be removed at the earliest possible point subject to any specific contractual support and development constraints.  # noqa: E501

        :param removal_date: The removal_date of this AddressDefinition.  # noqa: E501
        :type removal_date: datetime
        """

        self._removal_date = removal_date

    @property
    def documentation_link(self):
        """Gets the documentation_link of this AddressDefinition.  # noqa: E501

        Contains a link to the documentation for this AddressDefinition in KnowledgeBase.  # noqa: E501

        :return: The documentation_link of this AddressDefinition.  # noqa: E501
        :rtype: str
        """
        return self._documentation_link

    @documentation_link.setter
    def documentation_link(self, documentation_link):
        """Sets the documentation_link of this AddressDefinition.

        Contains a link to the documentation for this AddressDefinition in KnowledgeBase.  # noqa: E501

        :param documentation_link: The documentation_link of this AddressDefinition.  # noqa: E501
        :type documentation_link: str
        """

        self._documentation_link = documentation_link

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
        if not isinstance(other, AddressDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddressDefinition):
            return True

        return self.to_dict() != other.to_dict()
