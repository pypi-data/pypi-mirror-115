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


class RepresentativeStory(object):
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
        'id': 'int',
        'permalink': 'str',
        'published_at': 'datetime',
        'title': 'str'
    }

    attribute_map = {
        'id': 'id',
        'permalink': 'permalink',
        'published_at': 'published_at',
        'title': 'title'
    }

    def __init__(self, id=None, permalink=None, published_at=None, title=None, local_vars_configuration=None):  # noqa: E501
        """RepresentativeStory - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._permalink = None
        self._published_at = None
        self._title = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if permalink is not None:
            self.permalink = permalink
        if published_at is not None:
            self.published_at = published_at
        if title is not None:
            self.title = title

    @property
    def id(self):
        """Gets the id of this RepresentativeStory.  # noqa: E501

        ID of the story which is a unique identification  # noqa: E501

        :return: The id of this RepresentativeStory.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RepresentativeStory.

        ID of the story which is a unique identification  # noqa: E501

        :param id: The id of this RepresentativeStory.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def permalink(self):
        """Gets the permalink of this RepresentativeStory.  # noqa: E501

        The story permalink URL  # noqa: E501

        :return: The permalink of this RepresentativeStory.  # noqa: E501
        :rtype: str
        """
        return self._permalink

    @permalink.setter
    def permalink(self, permalink):
        """Sets the permalink of this RepresentativeStory.

        The story permalink URL  # noqa: E501

        :param permalink: The permalink of this RepresentativeStory.  # noqa: E501
        :type permalink: str
        """

        self._permalink = permalink

    @property
    def published_at(self):
        """Gets the published_at of this RepresentativeStory.  # noqa: E501

        Published date of the story  # noqa: E501

        :return: The published_at of this RepresentativeStory.  # noqa: E501
        :rtype: datetime
        """
        return self._published_at

    @published_at.setter
    def published_at(self, published_at):
        """Sets the published_at of this RepresentativeStory.

        Published date of the story  # noqa: E501

        :param published_at: The published_at of this RepresentativeStory.  # noqa: E501
        :type published_at: datetime
        """

        self._published_at = published_at

    @property
    def title(self):
        """Gets the title of this RepresentativeStory.  # noqa: E501

        Title of the story  # noqa: E501

        :return: The title of this RepresentativeStory.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this RepresentativeStory.

        Title of the story  # noqa: E501

        :param title: The title of this RepresentativeStory.  # noqa: E501
        :type title: str
        """

        self._title = title

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
        if not isinstance(other, RepresentativeStory):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RepresentativeStory):
            return True

        return self.to_dict() != other.to_dict()
