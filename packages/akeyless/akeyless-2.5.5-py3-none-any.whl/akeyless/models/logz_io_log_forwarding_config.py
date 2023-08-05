# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class LogzIoLogForwardingConfig(object):
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
        'target_logz_io_protocol': 'str',
        'target_logz_io_token': 'str'
    }

    attribute_map = {
        'target_logz_io_protocol': 'target_logz_io_protocol',
        'target_logz_io_token': 'target_logz_io_token'
    }

    def __init__(self, target_logz_io_protocol=None, target_logz_io_token=None, local_vars_configuration=None):  # noqa: E501
        """LogzIoLogForwardingConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._target_logz_io_protocol = None
        self._target_logz_io_token = None
        self.discriminator = None

        if target_logz_io_protocol is not None:
            self.target_logz_io_protocol = target_logz_io_protocol
        if target_logz_io_token is not None:
            self.target_logz_io_token = target_logz_io_token

    @property
    def target_logz_io_protocol(self):
        """Gets the target_logz_io_protocol of this LogzIoLogForwardingConfig.  # noqa: E501


        :return: The target_logz_io_protocol of this LogzIoLogForwardingConfig.  # noqa: E501
        :rtype: str
        """
        return self._target_logz_io_protocol

    @target_logz_io_protocol.setter
    def target_logz_io_protocol(self, target_logz_io_protocol):
        """Sets the target_logz_io_protocol of this LogzIoLogForwardingConfig.


        :param target_logz_io_protocol: The target_logz_io_protocol of this LogzIoLogForwardingConfig.  # noqa: E501
        :type: str
        """

        self._target_logz_io_protocol = target_logz_io_protocol

    @property
    def target_logz_io_token(self):
        """Gets the target_logz_io_token of this LogzIoLogForwardingConfig.  # noqa: E501


        :return: The target_logz_io_token of this LogzIoLogForwardingConfig.  # noqa: E501
        :rtype: str
        """
        return self._target_logz_io_token

    @target_logz_io_token.setter
    def target_logz_io_token(self, target_logz_io_token):
        """Sets the target_logz_io_token of this LogzIoLogForwardingConfig.


        :param target_logz_io_token: The target_logz_io_token of this LogzIoLogForwardingConfig.  # noqa: E501
        :type: str
        """

        self._target_logz_io_token = target_logz_io_token

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
        if not isinstance(other, LogzIoLogForwardingConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogzIoLogForwardingConfig):
            return True

        return self.to_dict() != other.to_dict()
