# coding: utf-8

"""
    Collibra Search API

    <p>The Search API allows you to create your own integration with the Collibra Search Engine.<br /> Find your data!</p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from collibra_search.configuration import Configuration


class SearchHighlight(object):
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
        'pre_tag': 'str',
        'post_tag': 'str'
    }

    attribute_map = {
        'pre_tag': 'preTag',
        'post_tag': 'postTag'
    }

    def __init__(self, pre_tag=None, post_tag=None, local_vars_configuration=None):  # noqa: E501
        """SearchHighlight - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pre_tag = None
        self._post_tag = None
        self.discriminator = None

        self.pre_tag = pre_tag
        self.post_tag = post_tag

    @property
    def pre_tag(self):
        """Gets the pre_tag of this SearchHighlight.  # noqa: E501

        Optional string to insert before the highlighted fragment. If set, you must also provide a value for `postTag`.  # noqa: E501

        :return: The pre_tag of this SearchHighlight.  # noqa: E501
        :rtype: str
        """
        return self._pre_tag

    @pre_tag.setter
    def pre_tag(self, pre_tag):
        """Sets the pre_tag of this SearchHighlight.

        Optional string to insert before the highlighted fragment. If set, you must also provide a value for `postTag`.  # noqa: E501

        :param pre_tag: The pre_tag of this SearchHighlight.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                pre_tag is not None and len(pre_tag) > 1000):
            raise ValueError("Invalid value for `pre_tag`, length must be less than or equal to `1000`")  # noqa: E501

        self._pre_tag = pre_tag

    @property
    def post_tag(self):
        """Gets the post_tag of this SearchHighlight.  # noqa: E501

        Optional string to insert after the highlighted fragment. If set, you must also provide a value for `preTag`.  # noqa: E501

        :return: The post_tag of this SearchHighlight.  # noqa: E501
        :rtype: str
        """
        return self._post_tag

    @post_tag.setter
    def post_tag(self, post_tag):
        """Sets the post_tag of this SearchHighlight.

        Optional string to insert after the highlighted fragment. If set, you must also provide a value for `preTag`.  # noqa: E501

        :param post_tag: The post_tag of this SearchHighlight.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                post_tag is not None and len(post_tag) > 1000):
            raise ValueError("Invalid value for `post_tag`, length must be less than or equal to `1000`")  # noqa: E501

        self._post_tag = post_tag

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
        if not isinstance(other, SearchHighlight):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SearchHighlight):
            return True

        return self.to_dict() != other.to_dict()
