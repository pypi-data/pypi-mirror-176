'''
# `consul_acl_auth_method`

Refer to the Terraform Registory for docs: [`consul_acl_auth_method`](https://www.terraform.io/docs/providers/consul/r/acl_auth_method).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class AclAuthMethod(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-consul.aclAuthMethod.AclAuthMethod",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method consul_acl_auth_method}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        config_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_token_ttl: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        namespace_rule: typing.Optional[typing.Union[typing.Sequence[typing.Union["AclAuthMethodNamespaceRule", typing.Dict[str, typing.Any]]], cdktf.IResolvable]] = None,
        partition: typing.Optional[builtins.str] = None,
        token_locality: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method consul_acl_auth_method} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#name AclAuthMethod#name}
        :param type: The type of the ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#type AclAuthMethod#type}
        :param config: The raw configuration for this ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config AclAuthMethod#config}
        :param config_json: The raw configuration for this ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config_json AclAuthMethod#config_json}
        :param description: A free form human readable description of the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#description AclAuthMethod#description}
        :param display_name: An optional name to use instead of the name attribute when displaying information about this auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#display_name AclAuthMethod#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#id AclAuthMethod#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_token_ttl: The maximum life of any token created by this auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#max_token_ttl AclAuthMethod#max_token_ttl}
        :param namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace AclAuthMethod#namespace}.
        :param namespace_rule: namespace_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace_rule AclAuthMethod#namespace_rule}
        :param partition: The partition the ACL auth method is associated with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#partition AclAuthMethod#partition}
        :param token_locality: The kind of token that this auth method produces. This can be either 'local' or 'global'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#token_locality AclAuthMethod#token_locality}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                name: builtins.str,
                type: builtins.str,
                config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                config_json: typing.Optional[builtins.str] = None,
                description: typing.Optional[builtins.str] = None,
                display_name: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                max_token_ttl: typing.Optional[builtins.str] = None,
                namespace: typing.Optional[builtins.str] = None,
                namespace_rule: typing.Optional[typing.Union[typing.Sequence[typing.Union[AclAuthMethodNamespaceRule, typing.Dict[str, typing.Any]]], cdktf.IResolvable]] = None,
                partition: typing.Optional[builtins.str] = None,
                token_locality: typing.Optional[builtins.str] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = AclAuthMethodConfig(
            name=name,
            type=type,
            config=config,
            config_json=config_json,
            description=description,
            display_name=display_name,
            id=id,
            max_token_ttl=max_token_ttl,
            namespace=namespace,
            namespace_rule=namespace_rule,
            partition=partition,
            token_locality=token_locality,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="putNamespaceRule")
    def put_namespace_rule(
        self,
        value: typing.Union[typing.Sequence[typing.Union["AclAuthMethodNamespaceRule", typing.Dict[str, typing.Any]]], cdktf.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[typing.Sequence[typing.Union[AclAuthMethodNamespaceRule, typing.Dict[str, typing.Any]]], cdktf.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespaceRule", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetConfigJson")
    def reset_config_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigJson", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxTokenTtl")
    def reset_max_token_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTokenTtl", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetNamespaceRule")
    def reset_namespace_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceRule", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetTokenLocality")
    def reset_token_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenLocality", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="namespaceRule")
    def namespace_rule(self) -> "AclAuthMethodNamespaceRuleList":
        return typing.cast("AclAuthMethodNamespaceRuleList", jsii.get(self, "namespaceRule"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="configJsonInput")
    def config_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTokenTtlInput")
    def max_token_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTokenTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceRuleInput")
    def namespace_rule_input(
        self,
    ) -> typing.Optional[typing.Union[typing.List["AclAuthMethodNamespaceRule"], cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[typing.List["AclAuthMethodNamespaceRule"], cdktf.IResolvable]], jsii.get(self, "namespaceRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenLocalityInput")
    def token_locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenLocalityInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "config"))

    @config.setter
    def config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="configJson")
    def config_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configJson"))

    @config_json.setter
    def config_json(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configJson", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maxTokenTtl")
    def max_token_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTokenTtl"))

    @max_token_ttl.setter
    def max_token_ttl(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTokenTtl", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value)

    @builtins.property
    @jsii.member(jsii_name="tokenLocality")
    def token_locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenLocality"))

    @token_locality.setter
    def token_locality(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenLocality", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-consul.aclAuthMethod.AclAuthMethodConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "type": "type",
        "config": "config",
        "config_json": "configJson",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "max_token_ttl": "maxTokenTtl",
        "namespace": "namespace",
        "namespace_rule": "namespaceRule",
        "partition": "partition",
        "token_locality": "tokenLocality",
    },
)
class AclAuthMethodConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        name: builtins.str,
        type: builtins.str,
        config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        config_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_token_ttl: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        namespace_rule: typing.Optional[typing.Union[typing.Sequence[typing.Union["AclAuthMethodNamespaceRule", typing.Dict[str, typing.Any]]], cdktf.IResolvable]] = None,
        partition: typing.Optional[builtins.str] = None,
        token_locality: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#name AclAuthMethod#name}
        :param type: The type of the ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#type AclAuthMethod#type}
        :param config: The raw configuration for this ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config AclAuthMethod#config}
        :param config_json: The raw configuration for this ACL auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config_json AclAuthMethod#config_json}
        :param description: A free form human readable description of the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#description AclAuthMethod#description}
        :param display_name: An optional name to use instead of the name attribute when displaying information about this auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#display_name AclAuthMethod#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#id AclAuthMethod#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_token_ttl: The maximum life of any token created by this auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#max_token_ttl AclAuthMethod#max_token_ttl}
        :param namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace AclAuthMethod#namespace}.
        :param namespace_rule: namespace_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace_rule AclAuthMethod#namespace_rule}
        :param partition: The partition the ACL auth method is associated with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#partition AclAuthMethod#partition}
        :param token_locality: The kind of token that this auth method produces. This can be either 'local' or 'global'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#token_locality AclAuthMethod#token_locality}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                name: builtins.str,
                type: builtins.str,
                config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                config_json: typing.Optional[builtins.str] = None,
                description: typing.Optional[builtins.str] = None,
                display_name: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                max_token_ttl: typing.Optional[builtins.str] = None,
                namespace: typing.Optional[builtins.str] = None,
                namespace_rule: typing.Optional[typing.Union[typing.Sequence[typing.Union[AclAuthMethodNamespaceRule, typing.Dict[str, typing.Any]]], cdktf.IResolvable]] = None,
                partition: typing.Optional[builtins.str] = None,
                token_locality: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument config_json", value=config_json, expected_type=type_hints["config_json"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_token_ttl", value=max_token_ttl, expected_type=type_hints["max_token_ttl"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument namespace_rule", value=namespace_rule, expected_type=type_hints["namespace_rule"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument token_locality", value=token_locality, expected_type=type_hints["token_locality"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if config is not None:
            self._values["config"] = config
        if config_json is not None:
            self._values["config_json"] = config_json
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if max_token_ttl is not None:
            self._values["max_token_ttl"] = max_token_ttl
        if namespace is not None:
            self._values["namespace"] = namespace
        if namespace_rule is not None:
            self._values["namespace_rule"] = namespace_rule
        if partition is not None:
            self._values["partition"] = partition
        if token_locality is not None:
            self._values["token_locality"] = token_locality

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ACL auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#name AclAuthMethod#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the ACL auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#type AclAuthMethod#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The raw configuration for this ACL auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config AclAuthMethod#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def config_json(self) -> typing.Optional[builtins.str]:
        '''The raw configuration for this ACL auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#config_json AclAuthMethod#config_json}
        '''
        result = self._values.get("config_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free form human readable description of the auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#description AclAuthMethod#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''An optional name to use instead of the name attribute when displaying information about this auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#display_name AclAuthMethod#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#id AclAuthMethod#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_token_ttl(self) -> typing.Optional[builtins.str]:
        '''The maximum life of any token created by this auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#max_token_ttl AclAuthMethod#max_token_ttl}
        '''
        result = self._values.get("max_token_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace AclAuthMethod#namespace}.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_rule(
        self,
    ) -> typing.Optional[typing.Union[typing.List["AclAuthMethodNamespaceRule"], cdktf.IResolvable]]:
        '''namespace_rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#namespace_rule AclAuthMethod#namespace_rule}
        '''
        result = self._values.get("namespace_rule")
        return typing.cast(typing.Optional[typing.Union[typing.List["AclAuthMethodNamespaceRule"], cdktf.IResolvable]], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''The partition the ACL auth method is associated with.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#partition AclAuthMethod#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_locality(self) -> typing.Optional[builtins.str]:
        '''The kind of token that this auth method produces. This can be either 'local' or 'global'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#token_locality AclAuthMethod#token_locality}
        '''
        result = self._values.get("token_locality")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AclAuthMethodConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-consul.aclAuthMethod.AclAuthMethodNamespaceRule",
    jsii_struct_bases=[],
    name_mapping={"bind_namespace": "bindNamespace", "selector": "selector"},
)
class AclAuthMethodNamespaceRule:
    def __init__(
        self,
        *,
        bind_namespace: builtins.str,
        selector: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bind_namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#bind_namespace AclAuthMethod#bind_namespace}.
        :param selector: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#selector AclAuthMethod#selector}.
        '''
        if __debug__:
            def stub(
                *,
                bind_namespace: builtins.str,
                selector: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bind_namespace", value=bind_namespace, expected_type=type_hints["bind_namespace"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[str, typing.Any] = {
            "bind_namespace": bind_namespace,
        }
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def bind_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#bind_namespace AclAuthMethod#bind_namespace}.'''
        result = self._values.get("bind_namespace")
        assert result is not None, "Required property 'bind_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/consul/r/acl_auth_method#selector AclAuthMethod#selector}.'''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AclAuthMethodNamespaceRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AclAuthMethodNamespaceRuleList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-consul.aclAuthMethod.AclAuthMethodNamespaceRuleList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AclAuthMethodNamespaceRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AclAuthMethodNamespaceRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[typing.List[AclAuthMethodNamespaceRule], cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[typing.List[AclAuthMethodNamespaceRule], cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[typing.List[AclAuthMethodNamespaceRule], cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[typing.List[AclAuthMethodNamespaceRule], cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AclAuthMethodNamespaceRuleOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-consul.aclAuthMethod.AclAuthMethodNamespaceRuleOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="bindNamespaceInput")
    def bind_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="bindNamespace")
    def bind_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bindNamespace"))

    @bind_namespace.setter
    def bind_namespace(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AclAuthMethodNamespaceRule, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AclAuthMethodNamespaceRule, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AclAuthMethodNamespaceRule, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[AclAuthMethodNamespaceRule, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AclAuthMethod",
    "AclAuthMethodConfig",
    "AclAuthMethodNamespaceRule",
    "AclAuthMethodNamespaceRuleList",
    "AclAuthMethodNamespaceRuleOutputReference",
]

publication.publish()
