# coding: utf-8

"""
    AYLIEN News API

    The AYLIEN News API is the most powerful way of sourcing, searching and syndicating analyzed and enriched news content. It is accessed by sending HTTP requests to our server, which returns information to your client.   # noqa: E501

    The version of the OpenAPI document: 3.0
    Contact: support@aylien.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from aylien_news_api.configuration import Configuration


class Coverages(object):
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
        'coverages': 'list[Story]',
        'story_body': 'str',
        'story_language': 'str',
        'story_published_at': 'datetime',
        'story_title': 'str'
    }

    attribute_map = {
        'coverages': 'coverages',
        'story_body': 'story_body',
        'story_language': 'story_language',
        'story_published_at': 'story_published_at',
        'story_title': 'story_title'
    }

    def __init__(self, coverages=None, story_body=None, story_language=None, story_published_at=None, story_title=None, local_vars_configuration=None):  # noqa: E501
        """Coverages - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._coverages = None
        self._story_body = None
        self._story_language = None
        self._story_published_at = None
        self._story_title = None
        self.discriminator = None

        if coverages is not None:
            self.coverages = coverages
        if story_body is not None:
            self.story_body = story_body
        if story_language is not None:
            self.story_language = story_language
        if story_published_at is not None:
            self.story_published_at = story_published_at
        if story_title is not None:
            self.story_title = story_title

    @property
    def coverages(self):
        """Gets the coverages of this Coverages.  # noqa: E501

        An array of coverages for the input story  # noqa: E501

        :return: The coverages of this Coverages.  # noqa: E501
        :rtype: list[Story]
        """
        return self._coverages

    @coverages.setter
    def coverages(self, coverages):
        """Sets the coverages of this Coverages.

        An array of coverages for the input story  # noqa: E501

        :param coverages: The coverages of this Coverages.  # noqa: E501
        :type: list[Story]
        """

        self._coverages = coverages

    @property
    def story_body(self):
        """Gets the story_body of this Coverages.  # noqa: E501

        The input story body  # noqa: E501

        :return: The story_body of this Coverages.  # noqa: E501
        :rtype: str
        """
        return self._story_body

    @story_body.setter
    def story_body(self, story_body):
        """Sets the story_body of this Coverages.

        The input story body  # noqa: E501

        :param story_body: The story_body of this Coverages.  # noqa: E501
        :type: str
        """

        self._story_body = story_body

    @property
    def story_language(self):
        """Gets the story_language of this Coverages.  # noqa: E501

        The input story language  # noqa: E501

        :return: The story_language of this Coverages.  # noqa: E501
        :rtype: str
        """
        return self._story_language

    @story_language.setter
    def story_language(self, story_language):
        """Sets the story_language of this Coverages.

        The input story language  # noqa: E501

        :param story_language: The story_language of this Coverages.  # noqa: E501
        :type: str
        """

        self._story_language = story_language

    @property
    def story_published_at(self):
        """Gets the story_published_at of this Coverages.  # noqa: E501

        The input story published date  # noqa: E501

        :return: The story_published_at of this Coverages.  # noqa: E501
        :rtype: datetime
        """
        return self._story_published_at

    @story_published_at.setter
    def story_published_at(self, story_published_at):
        """Sets the story_published_at of this Coverages.

        The input story published date  # noqa: E501

        :param story_published_at: The story_published_at of this Coverages.  # noqa: E501
        :type: datetime
        """

        self._story_published_at = story_published_at

    @property
    def story_title(self):
        """Gets the story_title of this Coverages.  # noqa: E501

        The input story title  # noqa: E501

        :return: The story_title of this Coverages.  # noqa: E501
        :rtype: str
        """
        return self._story_title

    @story_title.setter
    def story_title(self, story_title):
        """Sets the story_title of this Coverages.

        The input story title  # noqa: E501

        :param story_title: The story_title of this Coverages.  # noqa: E501
        :type: str
        """

        self._story_title = story_title

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
        if not isinstance(other, Coverages):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Coverages):
            return True

        return self.to_dict() != other.to_dict()
