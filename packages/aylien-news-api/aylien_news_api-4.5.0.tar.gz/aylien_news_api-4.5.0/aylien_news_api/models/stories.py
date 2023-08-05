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


class Stories(object):
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
        'next_page_cursor': 'str',
        'stories': 'list[Story]',
        'published_at_end': 'datetime',
        'published_at_start': 'datetime',
        'warnings': 'list[Warning]'
    }

    attribute_map = {
        'next_page_cursor': 'next_page_cursor',
        'stories': 'stories',
        'published_at_end': 'published_at.end',
        'published_at_start': 'published_at.start',
        'warnings': 'warnings'
    }

    def __init__(self, next_page_cursor=None, stories=None, published_at_end=None, published_at_start=None, warnings=None, local_vars_configuration=None):  # noqa: E501
        """Stories - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._next_page_cursor = None
        self._stories = None
        self._published_at_end = None
        self._published_at_start = None
        self._warnings = None
        self.discriminator = None

        if next_page_cursor is not None:
            self.next_page_cursor = next_page_cursor
        if stories is not None:
            self.stories = stories
        if published_at_end is not None:
            self.published_at_end = published_at_end
        if published_at_start is not None:
            self.published_at_start = published_at_start
        if warnings is not None:
            self.warnings = warnings

    @property
    def next_page_cursor(self):
        """Gets the next_page_cursor of this Stories.  # noqa: E501

        The next page cursor  # noqa: E501

        :return: The next_page_cursor of this Stories.  # noqa: E501
        :rtype: str
        """
        return self._next_page_cursor

    @next_page_cursor.setter
    def next_page_cursor(self, next_page_cursor):
        """Sets the next_page_cursor of this Stories.

        The next page cursor  # noqa: E501

        :param next_page_cursor: The next_page_cursor of this Stories.  # noqa: E501
        :type next_page_cursor: str
        """

        self._next_page_cursor = next_page_cursor

    @property
    def stories(self):
        """Gets the stories of this Stories.  # noqa: E501

        An array of stories  # noqa: E501

        :return: The stories of this Stories.  # noqa: E501
        :rtype: list[Story]
        """
        return self._stories

    @stories.setter
    def stories(self, stories):
        """Sets the stories of this Stories.

        An array of stories  # noqa: E501

        :param stories: The stories of this Stories.  # noqa: E501
        :type stories: list[Story]
        """

        self._stories = stories

    @property
    def published_at_end(self):
        """Gets the published_at_end of this Stories.  # noqa: E501

        The end of a period in which searched stories were published  # noqa: E501

        :return: The published_at_end of this Stories.  # noqa: E501
        :rtype: datetime
        """
        return self._published_at_end

    @published_at_end.setter
    def published_at_end(self, published_at_end):
        """Sets the published_at_end of this Stories.

        The end of a period in which searched stories were published  # noqa: E501

        :param published_at_end: The published_at_end of this Stories.  # noqa: E501
        :type published_at_end: datetime
        """

        self._published_at_end = published_at_end

    @property
    def published_at_start(self):
        """Gets the published_at_start of this Stories.  # noqa: E501

        The start of a period in which searched stories were published  # noqa: E501

        :return: The published_at_start of this Stories.  # noqa: E501
        :rtype: datetime
        """
        return self._published_at_start

    @published_at_start.setter
    def published_at_start(self, published_at_start):
        """Sets the published_at_start of this Stories.

        The start of a period in which searched stories were published  # noqa: E501

        :param published_at_start: The published_at_start of this Stories.  # noqa: E501
        :type published_at_start: datetime
        """

        self._published_at_start = published_at_start

    @property
    def warnings(self):
        """Gets the warnings of this Stories.  # noqa: E501

        Notifies about possible issues that occurred when searching for stories  # noqa: E501

        :return: The warnings of this Stories.  # noqa: E501
        :rtype: list[Warning]
        """
        return self._warnings

    @warnings.setter
    def warnings(self, warnings):
        """Sets the warnings of this Stories.

        Notifies about possible issues that occurred when searching for stories  # noqa: E501

        :param warnings: The warnings of this Stories.  # noqa: E501
        :type warnings: list[Warning]
        """

        self._warnings = warnings

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
        if not isinstance(other, Stories):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Stories):
            return True

        return self.to_dict() != other.to_dict()
