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


class GatewayCreateProducerSnowflake(object):
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
        'account': 'str',
        'db_name': 'str',
        'name': 'str',
        'password': 'str',
        'role': 'str',
        'token': 'str',
        'uid_token': 'str',
        'user_ttl': 'str',
        'username': 'str',
        'warehouse': 'str'
    }

    attribute_map = {
        'account': 'account',
        'db_name': 'db-name',
        'name': 'name',
        'password': 'password',
        'role': 'role',
        'token': 'token',
        'uid_token': 'uid-token',
        'user_ttl': 'user-ttl',
        'username': 'username',
        'warehouse': 'warehouse'
    }

    def __init__(self, account=None, db_name=None, name=None, password=None, role=None, token=None, uid_token=None, user_ttl='24h', username=None, warehouse=None, local_vars_configuration=None):  # noqa: E501
        """GatewayCreateProducerSnowflake - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account = None
        self._db_name = None
        self._name = None
        self._password = None
        self._role = None
        self._token = None
        self._uid_token = None
        self._user_ttl = None
        self._username = None
        self._warehouse = None
        self.discriminator = None

        self.account = account
        self.db_name = db_name
        self.name = name
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if user_ttl is not None:
            self.user_ttl = user_ttl
        if username is not None:
            self.username = username
        if warehouse is not None:
            self.warehouse = warehouse

    @property
    def account(self):
        """Gets the account of this GatewayCreateProducerSnowflake.  # noqa: E501

        Account name  # noqa: E501

        :return: The account of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this GatewayCreateProducerSnowflake.

        Account name  # noqa: E501

        :param account: The account of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and account is None:  # noqa: E501
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def db_name(self):
        """Gets the db_name of this GatewayCreateProducerSnowflake.  # noqa: E501

        Database name  # noqa: E501

        :return: The db_name of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        """Sets the db_name of this GatewayCreateProducerSnowflake.

        Database name  # noqa: E501

        :param db_name: The db_name of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and db_name is None:  # noqa: E501
            raise ValueError("Invalid value for `db_name`, must not be `None`")  # noqa: E501

        self._db_name = db_name

    @property
    def name(self):
        """Gets the name of this GatewayCreateProducerSnowflake.  # noqa: E501

        Producer name  # noqa: E501

        :return: The name of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayCreateProducerSnowflake.

        Producer name  # noqa: E501

        :param name: The name of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def password(self):
        """Gets the password of this GatewayCreateProducerSnowflake.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The password of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this GatewayCreateProducerSnowflake.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param password: The password of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def role(self):
        """Gets the role of this GatewayCreateProducerSnowflake.  # noqa: E501

        User role  # noqa: E501

        :return: The role of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this GatewayCreateProducerSnowflake.

        User role  # noqa: E501

        :param role: The role of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._role = role

    @property
    def token(self):
        """Gets the token of this GatewayCreateProducerSnowflake.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayCreateProducerSnowflake.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayCreateProducerSnowflake.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayCreateProducerSnowflake.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_ttl(self):
        """Gets the user_ttl of this GatewayCreateProducerSnowflake.  # noqa: E501

        User TTL  # noqa: E501

        :return: The user_ttl of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._user_ttl

    @user_ttl.setter
    def user_ttl(self, user_ttl):
        """Sets the user_ttl of this GatewayCreateProducerSnowflake.

        User TTL  # noqa: E501

        :param user_ttl: The user_ttl of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._user_ttl = user_ttl

    @property
    def username(self):
        """Gets the username of this GatewayCreateProducerSnowflake.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The username of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this GatewayCreateProducerSnowflake.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param username: The username of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def warehouse(self):
        """Gets the warehouse of this GatewayCreateProducerSnowflake.  # noqa: E501

        Warehouse name  # noqa: E501

        :return: The warehouse of this GatewayCreateProducerSnowflake.  # noqa: E501
        :rtype: str
        """
        return self._warehouse

    @warehouse.setter
    def warehouse(self, warehouse):
        """Sets the warehouse of this GatewayCreateProducerSnowflake.

        Warehouse name  # noqa: E501

        :param warehouse: The warehouse of this GatewayCreateProducerSnowflake.  # noqa: E501
        :type: str
        """

        self._warehouse = warehouse

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
        if not isinstance(other, GatewayCreateProducerSnowflake):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayCreateProducerSnowflake):
            return True

        return self.to_dict() != other.to_dict()
