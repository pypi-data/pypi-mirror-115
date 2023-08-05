# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class InfraEnv(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'kind': 'str',
        'id': 'str',
        'href': 'str',
        'openshift_version': 'str',
        'name': 'str',
        'proxy': 'Proxy',
        'additional_ntp_sources': 'str',
        'ssh_authorized_key': 'str',
        'pull_secret_set': 'bool',
        'static_network_config': 'str',
        'type': 'ImageType',
        'ignition_config_override': 'str',
        'cluster_id': 'str',
        'size_bytes': 'int',
        'download_url': 'str',
        'generator_version': 'str',
        'created_at': 'datetime',
        'expires_at': 'datetime'
    }

    attribute_map = {
        'kind': 'kind',
        'id': 'id',
        'href': 'href',
        'openshift_version': 'openshift_version',
        'name': 'name',
        'proxy': 'proxy',
        'additional_ntp_sources': 'additional_ntp_sources',
        'ssh_authorized_key': 'ssh_authorized_key',
        'pull_secret_set': 'pull_secret_set',
        'static_network_config': 'static_network_config',
        'type': 'type',
        'ignition_config_override': 'ignition_config_override',
        'cluster_id': 'cluster_id',
        'size_bytes': 'size_bytes',
        'download_url': 'download_url',
        'generator_version': 'generator_version',
        'created_at': 'created_at',
        'expires_at': 'expires_at'
    }

    def __init__(self, kind=None, id=None, href=None, openshift_version=None, name=None, proxy=None, additional_ntp_sources=None, ssh_authorized_key=None, pull_secret_set=None, static_network_config=None, type=None, ignition_config_override=None, cluster_id=None, size_bytes=None, download_url=None, generator_version=None, created_at=None, expires_at=None):  # noqa: E501
        """InfraEnv - a model defined in Swagger"""  # noqa: E501

        self._kind = None
        self._id = None
        self._href = None
        self._openshift_version = None
        self._name = None
        self._proxy = None
        self._additional_ntp_sources = None
        self._ssh_authorized_key = None
        self._pull_secret_set = None
        self._static_network_config = None
        self._type = None
        self._ignition_config_override = None
        self._cluster_id = None
        self._size_bytes = None
        self._download_url = None
        self._generator_version = None
        self._created_at = None
        self._expires_at = None
        self.discriminator = None

        if kind is not None:
            self.kind = kind
        if id is not None:
            self.id = id
        if href is not None:
            self.href = href
        if openshift_version is not None:
            self.openshift_version = openshift_version
        if name is not None:
            self.name = name
        if proxy is not None:
            self.proxy = proxy
        if additional_ntp_sources is not None:
            self.additional_ntp_sources = additional_ntp_sources
        if ssh_authorized_key is not None:
            self.ssh_authorized_key = ssh_authorized_key
        if pull_secret_set is not None:
            self.pull_secret_set = pull_secret_set
        if static_network_config is not None:
            self.static_network_config = static_network_config
        if type is not None:
            self.type = type
        if ignition_config_override is not None:
            self.ignition_config_override = ignition_config_override
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if size_bytes is not None:
            self.size_bytes = size_bytes
        if download_url is not None:
            self.download_url = download_url
        if generator_version is not None:
            self.generator_version = generator_version
        if created_at is not None:
            self.created_at = created_at
        if expires_at is not None:
            self.expires_at = expires_at

    @property
    def kind(self):
        """Gets the kind of this InfraEnv.  # noqa: E501

        Indicates the type of this object.  # noqa: E501

        :return: The kind of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this InfraEnv.

        Indicates the type of this object.  # noqa: E501

        :param kind: The kind of this InfraEnv.  # noqa: E501
        :type: str
        """
        allowed_values = ["InfraEnv"]  # noqa: E501
        if kind not in allowed_values:
            raise ValueError(
                "Invalid value for `kind` ({0}), must be one of {1}"  # noqa: E501
                .format(kind, allowed_values)
            )

        self._kind = kind

    @property
    def id(self):
        """Gets the id of this InfraEnv.  # noqa: E501

        Unique identifier of the object.  # noqa: E501

        :return: The id of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InfraEnv.

        Unique identifier of the object.  # noqa: E501

        :param id: The id of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def href(self):
        """Gets the href of this InfraEnv.  # noqa: E501

        Self link.  # noqa: E501

        :return: The href of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this InfraEnv.

        Self link.  # noqa: E501

        :param href: The href of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def openshift_version(self):
        """Gets the openshift_version of this InfraEnv.  # noqa: E501

        Version of the OpenShift cluster (used to infer the RHCOS version - temporary until generic logic implemented).  # noqa: E501

        :return: The openshift_version of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._openshift_version

    @openshift_version.setter
    def openshift_version(self, openshift_version):
        """Sets the openshift_version of this InfraEnv.

        Version of the OpenShift cluster (used to infer the RHCOS version - temporary until generic logic implemented).  # noqa: E501

        :param openshift_version: The openshift_version of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._openshift_version = openshift_version

    @property
    def name(self):
        """Gets the name of this InfraEnv.  # noqa: E501

        Name of the InfraEnv.  # noqa: E501

        :return: The name of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InfraEnv.

        Name of the InfraEnv.  # noqa: E501

        :param name: The name of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def proxy(self):
        """Gets the proxy of this InfraEnv.  # noqa: E501


        :return: The proxy of this InfraEnv.  # noqa: E501
        :rtype: Proxy
        """
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        """Sets the proxy of this InfraEnv.


        :param proxy: The proxy of this InfraEnv.  # noqa: E501
        :type: Proxy
        """

        self._proxy = proxy

    @property
    def additional_ntp_sources(self):
        """Gets the additional_ntp_sources of this InfraEnv.  # noqa: E501

        A comma-separated list of NTP sources (name or IP) going to be added to all the hosts.  # noqa: E501

        :return: The additional_ntp_sources of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._additional_ntp_sources

    @additional_ntp_sources.setter
    def additional_ntp_sources(self, additional_ntp_sources):
        """Sets the additional_ntp_sources of this InfraEnv.

        A comma-separated list of NTP sources (name or IP) going to be added to all the hosts.  # noqa: E501

        :param additional_ntp_sources: The additional_ntp_sources of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._additional_ntp_sources = additional_ntp_sources

    @property
    def ssh_authorized_key(self):
        """Gets the ssh_authorized_key of this InfraEnv.  # noqa: E501

        SSH public key for debugging the installation.  # noqa: E501

        :return: The ssh_authorized_key of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._ssh_authorized_key

    @ssh_authorized_key.setter
    def ssh_authorized_key(self, ssh_authorized_key):
        """Sets the ssh_authorized_key of this InfraEnv.

        SSH public key for debugging the installation.  # noqa: E501

        :param ssh_authorized_key: The ssh_authorized_key of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._ssh_authorized_key = ssh_authorized_key

    @property
    def pull_secret_set(self):
        """Gets the pull_secret_set of this InfraEnv.  # noqa: E501

        True if the pull secret has been added to the cluster.  # noqa: E501

        :return: The pull_secret_set of this InfraEnv.  # noqa: E501
        :rtype: bool
        """
        return self._pull_secret_set

    @pull_secret_set.setter
    def pull_secret_set(self, pull_secret_set):
        """Sets the pull_secret_set of this InfraEnv.

        True if the pull secret has been added to the cluster.  # noqa: E501

        :param pull_secret_set: The pull_secret_set of this InfraEnv.  # noqa: E501
        :type: bool
        """

        self._pull_secret_set = pull_secret_set

    @property
    def static_network_config(self):
        """Gets the static_network_config of this InfraEnv.  # noqa: E501

        static network configuration string in the format expected by discovery ignition generation.  # noqa: E501

        :return: The static_network_config of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._static_network_config

    @static_network_config.setter
    def static_network_config(self, static_network_config):
        """Sets the static_network_config of this InfraEnv.

        static network configuration string in the format expected by discovery ignition generation.  # noqa: E501

        :param static_network_config: The static_network_config of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._static_network_config = static_network_config

    @property
    def type(self):
        """Gets the type of this InfraEnv.  # noqa: E501


        :return: The type of this InfraEnv.  # noqa: E501
        :rtype: ImageType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this InfraEnv.


        :param type: The type of this InfraEnv.  # noqa: E501
        :type: ImageType
        """

        self._type = type

    @property
    def ignition_config_override(self):
        """Gets the ignition_config_override of this InfraEnv.  # noqa: E501

        Json formatted string containing the user overrides for the initial ignition config.  # noqa: E501

        :return: The ignition_config_override of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._ignition_config_override

    @ignition_config_override.setter
    def ignition_config_override(self, ignition_config_override):
        """Sets the ignition_config_override of this InfraEnv.

        Json formatted string containing the user overrides for the initial ignition config.  # noqa: E501

        :param ignition_config_override: The ignition_config_override of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._ignition_config_override = ignition_config_override

    @property
    def cluster_id(self):
        """Gets the cluster_id of this InfraEnv.  # noqa: E501

        If set, all hosts that register will be associated with the specified cluster.  # noqa: E501

        :return: The cluster_id of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this InfraEnv.

        If set, all hosts that register will be associated with the specified cluster.  # noqa: E501

        :param cluster_id: The cluster_id of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def size_bytes(self):
        """Gets the size_bytes of this InfraEnv.  # noqa: E501


        :return: The size_bytes of this InfraEnv.  # noqa: E501
        :rtype: int
        """
        return self._size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes):
        """Sets the size_bytes of this InfraEnv.


        :param size_bytes: The size_bytes of this InfraEnv.  # noqa: E501
        :type: int
        """
        if size_bytes is not None and size_bytes < 0:  # noqa: E501
            raise ValueError("Invalid value for `size_bytes`, must be a value greater than or equal to `0`")  # noqa: E501

        self._size_bytes = size_bytes

    @property
    def download_url(self):
        """Gets the download_url of this InfraEnv.  # noqa: E501


        :return: The download_url of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this InfraEnv.


        :param download_url: The download_url of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._download_url = download_url

    @property
    def generator_version(self):
        """Gets the generator_version of this InfraEnv.  # noqa: E501

        Image generator version.  # noqa: E501

        :return: The generator_version of this InfraEnv.  # noqa: E501
        :rtype: str
        """
        return self._generator_version

    @generator_version.setter
    def generator_version(self, generator_version):
        """Sets the generator_version of this InfraEnv.

        Image generator version.  # noqa: E501

        :param generator_version: The generator_version of this InfraEnv.  # noqa: E501
        :type: str
        """

        self._generator_version = generator_version

    @property
    def created_at(self):
        """Gets the created_at of this InfraEnv.  # noqa: E501


        :return: The created_at of this InfraEnv.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InfraEnv.


        :param created_at: The created_at of this InfraEnv.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def expires_at(self):
        """Gets the expires_at of this InfraEnv.  # noqa: E501


        :return: The expires_at of this InfraEnv.  # noqa: E501
        :rtype: datetime
        """
        return self._expires_at

    @expires_at.setter
    def expires_at(self, expires_at):
        """Sets the expires_at of this InfraEnv.


        :param expires_at: The expires_at of this InfraEnv.  # noqa: E501
        :type: datetime
        """

        self._expires_at = expires_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(InfraEnv, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InfraEnv):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
