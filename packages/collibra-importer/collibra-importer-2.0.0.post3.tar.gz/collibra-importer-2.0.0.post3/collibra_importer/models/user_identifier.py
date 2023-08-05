# coding: utf-8

"""
    Collibra Import API

    <p>The Import API is an efficient way to load large volumes of data into the Collibra Data Governance Center. The API can automatically differentiate between creating and updating data.</p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from collibra_importer.configuration import Configuration


class UserIdentifier(object):
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
    """
    openapi_types = {
        'id': 'str',
        'indexes': 'list[int]'
    }

    attribute_map = {
        'id': 'id',
        'indexes': 'indexes'
    }

    def __init__(self, id=None, indexes=None, local_vars_configuration=None):  # noqa: E501
        """UserIdentifier - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._indexes = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if indexes is not None:
            self.indexes = indexes

    @property
    def id(self):
        """Gets the id of this UserIdentifier.  # noqa: E501


        :return: The id of this UserIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UserIdentifier.


        :param id: The id of this UserIdentifier.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def indexes(self):
        """Gets the indexes of this UserIdentifier.  # noqa: E501


        :return: The indexes of this UserIdentifier.  # noqa: E501
        :rtype: list[int]
        """
        return self._indexes

    @indexes.setter
    def indexes(self, indexes):
        """Sets the indexes of this UserIdentifier.


        :param indexes: The indexes of this UserIdentifier.  # noqa: E501
        :type: list[int]
        """

        self._indexes = indexes

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
        if not isinstance(other, UserIdentifier):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserIdentifier):
            return True

        return self.to_dict() != other.to_dict()
