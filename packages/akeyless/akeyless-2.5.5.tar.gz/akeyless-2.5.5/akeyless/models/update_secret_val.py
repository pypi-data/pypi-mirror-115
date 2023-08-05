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


class UpdateSecretVal(object):
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
        'key': 'str',
        'multiline': 'bool',
        'name': 'str',
        'new_version': 'bool',
        'password': 'str',
        'token': 'str',
        'uid_token': 'str',
        'username': 'str',
        'value': 'str'
    }

    attribute_map = {
        'key': 'key',
        'multiline': 'multiline',
        'name': 'name',
        'new_version': 'new-version',
        'password': 'password',
        'token': 'token',
        'uid_token': 'uid-token',
        'username': 'username',
        'value': 'value'
    }

    def __init__(self, key=None, multiline=None, name=None, new_version=False, password=None, token=None, uid_token=None, username=None, value=None, local_vars_configuration=None):  # noqa: E501
        """UpdateSecretVal - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._multiline = None
        self._name = None
        self._new_version = None
        self._password = None
        self._token = None
        self._uid_token = None
        self._username = None
        self._value = None
        self.discriminator = None

        if key is not None:
            self.key = key
        if multiline is not None:
            self.multiline = multiline
        self.name = name
        if new_version is not None:
            self.new_version = new_version
        if password is not None:
            self.password = password
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if username is not None:
            self.username = username
        self.value = value

    @property
    def key(self):
        """Gets the key of this UpdateSecretVal.  # noqa: E501

        The name of a key that used to encrypt the secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :return: The key of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this UpdateSecretVal.

        The name of a key that used to encrypt the secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :param key: The key of this UpdateSecretVal.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def multiline(self):
        """Gets the multiline of this UpdateSecretVal.  # noqa: E501

        The provided value is a multiline value (separated by '\\n')  # noqa: E501

        :return: The multiline of this UpdateSecretVal.  # noqa: E501
        :rtype: bool
        """
        return self._multiline

    @multiline.setter
    def multiline(self, multiline):
        """Sets the multiline of this UpdateSecretVal.

        The provided value is a multiline value (separated by '\\n')  # noqa: E501

        :param multiline: The multiline of this UpdateSecretVal.  # noqa: E501
        :type: bool
        """

        self._multiline = multiline

    @property
    def name(self):
        """Gets the name of this UpdateSecretVal.  # noqa: E501

        Secret name  # noqa: E501

        :return: The name of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateSecretVal.

        Secret name  # noqa: E501

        :param name: The name of this UpdateSecretVal.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_version(self):
        """Gets the new_version of this UpdateSecretVal.  # noqa: E501

        Whether to create a new version of not  # noqa: E501

        :return: The new_version of this UpdateSecretVal.  # noqa: E501
        :rtype: bool
        """
        return self._new_version

    @new_version.setter
    def new_version(self, new_version):
        """Sets the new_version of this UpdateSecretVal.

        Whether to create a new version of not  # noqa: E501

        :param new_version: The new_version of this UpdateSecretVal.  # noqa: E501
        :type: bool
        """

        self._new_version = new_version

    @property
    def password(self):
        """Gets the password of this UpdateSecretVal.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The password of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this UpdateSecretVal.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param password: The password of this UpdateSecretVal.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def token(self):
        """Gets the token of this UpdateSecretVal.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateSecretVal.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateSecretVal.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateSecretVal.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateSecretVal.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateSecretVal.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def username(self):
        """Gets the username of this UpdateSecretVal.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The username of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UpdateSecretVal.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param username: The username of this UpdateSecretVal.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def value(self):
        """Gets the value of this UpdateSecretVal.  # noqa: E501

        The new secret value  # noqa: E501

        :return: The value of this UpdateSecretVal.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this UpdateSecretVal.

        The new secret value  # noqa: E501

        :param value: The value of this UpdateSecretVal.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

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
        if not isinstance(other, UpdateSecretVal):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateSecretVal):
            return True

        return self.to_dict() != other.to_dict()
