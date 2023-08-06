'''
## Aliyun ROS PVTZ Construct Library

This module is part of the AliCloud ROS Cloud Development Kit (ROS CDK) project.

```python
import * as PVTZ from '@alicloud/ros-cdk-pvtz';
```
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

from ._jsii import *

import ros_cdk_core


class RosUserVpcAuthorization(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.RosUserVpcAuthorization",
):
    '''A ROS template type:  ``ALIYUN::PVTZ::UserVpcAuthorization``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosUserVpcAuthorizationProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::UserVpcAuthorization``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosUserVpcAuthorizationProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            def stub(props: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAuthorizedUserId")
    def attr_authorized_user_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AuthorizedUserId: The account ID of the user who authorizes the resource.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAuthorizedUserId"))

    @builtins.property
    @jsii.member(jsii_name="attrAuthType")
    def attr_auth_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AuthType: Authorization type.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAuthType"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="authorizedUserId")
    def authorized_user_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: authorizedUserId: The account ID of the user who authorizes the resource.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "authorizedUserId"))

    @authorized_user_id.setter
    def authorized_user_id(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedUserId", value)

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="authChannel")
    def auth_channel(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        authChannel: Authorization channel. Valid values:
        AUTH_CODE: Verification code authorization, to verify whether the verification code passed in by AuthCode is correct.
        RESOURCE_DIRECTORY: Resource directory authorization, verify whether the AuthorizedUserId and the current account have resource directory credit.When it is empty, it is the same as AUTH_CODE, that is, verification code authorization.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "authChannel"))

    @auth_channel.setter
    def auth_channel(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authChannel", value)

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: authCode: Verification code, if AuthChannel takes "AUTH_CODE" or is empty, it is mandatory.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: authType: Authorization type.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreDeletionForbidden")
    def ignore_deletion_forbidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: ignoreDeletionForbidden: Whether to ignore following deletion forbidden errors when deleting:- UserAuth.DeleteForbidden.ZoneVpcExists
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], jsii.get(self, "ignoreDeletionForbidden"))

    @ignore_deletion_forbidden.setter
    def ignore_deletion_forbidden(
        self,
        value: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreDeletionForbidden", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.RosUserVpcAuthorizationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_user_id": "authorizedUserId",
        "auth_channel": "authChannel",
        "auth_code": "authCode",
        "auth_type": "authType",
        "ignore_deletion_forbidden": "ignoreDeletionForbidden",
    },
)
class RosUserVpcAuthorizationProps:
    def __init__(
        self,
        *,
        authorized_user_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        auth_channel: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auth_code: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ignore_deletion_forbidden: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::UserVpcAuthorization``.

        :param authorized_user_id: 
        :param auth_channel: 
        :param auth_code: 
        :param auth_type: 
        :param ignore_deletion_forbidden: 
        '''
        if __debug__:
            def stub(
                *,
                authorized_user_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                auth_channel: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auth_code: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ignore_deletion_forbidden: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument authorized_user_id", value=authorized_user_id, expected_type=type_hints["authorized_user_id"])
            check_type(argname="argument auth_channel", value=auth_channel, expected_type=type_hints["auth_channel"])
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument ignore_deletion_forbidden", value=ignore_deletion_forbidden, expected_type=type_hints["ignore_deletion_forbidden"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorized_user_id": authorized_user_id,
        }
        if auth_channel is not None:
            self._values["auth_channel"] = auth_channel
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if ignore_deletion_forbidden is not None:
            self._values["ignore_deletion_forbidden"] = ignore_deletion_forbidden

    @builtins.property
    def authorized_user_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: authorizedUserId: The account ID of the user who authorizes the resource.
        '''
        result = self._values.get("authorized_user_id")
        assert result is not None, "Required property 'authorized_user_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def auth_channel(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        authChannel: Authorization channel. Valid values:
        AUTH_CODE: Verification code authorization, to verify whether the verification code passed in by AuthCode is correct.
        RESOURCE_DIRECTORY: Resource directory authorization, verify whether the AuthorizedUserId and the current account have resource directory credit.When it is empty, it is the same as AUTH_CODE, that is, verification code authorization.
        '''
        result = self._values.get("auth_channel")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auth_code(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: authCode: Verification code, if AuthChannel takes "AUTH_CODE" or is empty, it is mandatory.
        '''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: authType: Authorization type.
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ignore_deletion_forbidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: ignoreDeletionForbidden: Whether to ignore following deletion forbidden errors when deleting:- UserAuth.DeleteForbidden.ZoneVpcExists
        '''
        result = self._values.get("ignore_deletion_forbidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosUserVpcAuthorizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosZone(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.RosZone",
):
    '''A ROS template type:  ``ALIYUN::PVTZ::Zone``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosZoneProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::Zone``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosZoneProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            def stub(props: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneId: Zone ID.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneName")
    def attr_zone_name(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneName: Zone name.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneName"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneTag")
    def attr_zone_tag(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneTag: Zone label.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneTag"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneType")
    def attr_zone_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneType: Zone type.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneType"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneName: Zone name
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "zoneName"))

    @zone_name.setter
    def zone_name(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneName", value)

    @builtins.property
    @jsii.member(jsii_name="ignoredStackTagKeys")
    def ignored_stack_tag_keys(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]]:
        '''
        :Property: ignoredStackTagKeys: Stack tag keys to ignore
        '''
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]], jsii.get(self, "ignoredStackTagKeys"))

    @ignored_stack_tag_keys.setter
    def ignored_stack_tag_keys(
        self,
        value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoredStackTagKeys", value)

    @builtins.property
    @jsii.member(jsii_name="proxyPattern")
    def proxy_pattern(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        proxyPattern: ZONE: completely hijack the entire zone.
        RECORD: Incomplete hijacking, recursive resolution agent.
        Default to ZONE.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "proxyPattern"))

    @proxy_pattern.setter
    def proxy_pattern(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyPattern", value)

    @builtins.property
    @jsii.member(jsii_name="remark")
    def remark(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: remark: 50 characters at most. It can only contain numbers, Chinese, English and special characters: "_-,.，。".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "remark"))

    @remark.setter
    def remark(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remark", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: resourceGroupId: Resource group id.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["RosZone.TagsProperty"]]:
        '''
        :Property: tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        return typing.cast(typing.Optional[typing.List["RosZone.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["RosZone.TagsProperty"]]) -> None:
        if __debug__:
            def stub(value: typing.Optional[typing.List[RosZone.TagsProperty]]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="zoneTag")
    def zone_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneTag: Zone label. It will be ignored when ZoneType is AUTH_ZONE.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "zoneTag"))

    @zone_tag.setter
    def zone_tag(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneTag", value)

    @builtins.property
    @jsii.member(jsii_name="zoneType")
    def zone_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneType: Zone type. For instance: AUTH_ZONE, CLOUD_PRODUCT_ZONE.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "zoneType"))

    @zone_type.setter
    def zone_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneType", value)

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-pvtz.RosZone.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ) -> None:
            '''
            :param key: 
            :param value: 
            '''
            if __debug__:
                def stub(
                    *,
                    key: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                    value: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
            }
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: key: undefined
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
            '''
            :Property: value: undefined
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.RosZoneProps",
    jsii_struct_bases=[],
    name_mapping={
        "zone_name": "zoneName",
        "ignored_stack_tag_keys": "ignoredStackTagKeys",
        "proxy_pattern": "proxyPattern",
        "remark": "remark",
        "resource_group_id": "resourceGroupId",
        "tags": "tags",
        "zone_tag": "zoneTag",
        "zone_type": "zoneType",
    },
)
class RosZoneProps:
    def __init__(
        self,
        *,
        zone_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        ignored_stack_tag_keys: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]] = None,
        proxy_pattern: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        remark: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[RosZone.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
        zone_tag: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        zone_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::Zone``.

        :param zone_name: 
        :param ignored_stack_tag_keys: 
        :param proxy_pattern: 
        :param remark: 
        :param resource_group_id: 
        :param tags: 
        :param zone_tag: 
        :param zone_type: 
        '''
        if __debug__:
            def stub(
                *,
                zone_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                ignored_stack_tag_keys: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]] = None,
                proxy_pattern: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                remark: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union[RosZone.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
                zone_tag: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                zone_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
            check_type(argname="argument ignored_stack_tag_keys", value=ignored_stack_tag_keys, expected_type=type_hints["ignored_stack_tag_keys"])
            check_type(argname="argument proxy_pattern", value=proxy_pattern, expected_type=type_hints["proxy_pattern"])
            check_type(argname="argument remark", value=remark, expected_type=type_hints["remark"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone_tag", value=zone_tag, expected_type=type_hints["zone_tag"])
            check_type(argname="argument zone_type", value=zone_type, expected_type=type_hints["zone_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "zone_name": zone_name,
        }
        if ignored_stack_tag_keys is not None:
            self._values["ignored_stack_tag_keys"] = ignored_stack_tag_keys
        if proxy_pattern is not None:
            self._values["proxy_pattern"] = proxy_pattern
        if remark is not None:
            self._values["remark"] = remark
        if resource_group_id is not None:
            self._values["resource_group_id"] = resource_group_id
        if tags is not None:
            self._values["tags"] = tags
        if zone_tag is not None:
            self._values["zone_tag"] = zone_tag
        if zone_type is not None:
            self._values["zone_type"] = zone_type

    @builtins.property
    def zone_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneName: Zone name
        '''
        result = self._values.get("zone_name")
        assert result is not None, "Required property 'zone_name' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def ignored_stack_tag_keys(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]]:
        '''
        :Property: ignoredStackTagKeys: Stack tag keys to ignore
        '''
        result = self._values.get("ignored_stack_tag_keys")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]], result)

    @builtins.property
    def proxy_pattern(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        proxyPattern: ZONE: completely hijack the entire zone.
        RECORD: Incomplete hijacking, recursive resolution agent.
        Default to ZONE.
        '''
        result = self._values.get("proxy_pattern")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def remark(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: remark: 50 characters at most. It can only contain numbers, Chinese, English and special characters: "_-,.，。".
        '''
        result = self._values.get("remark")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: resourceGroupId: Resource group id.
        '''
        result = self._values.get("resource_group_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[RosZone.TagsProperty]]:
        '''
        :Property: tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[RosZone.TagsProperty]], result)

    @builtins.property
    def zone_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneTag: Zone label. It will be ignored when ZoneType is AUTH_ZONE.
        '''
        result = self._values.get("zone_tag")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def zone_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneType: Zone type. For instance: AUTH_ZONE, CLOUD_PRODUCT_ZONE.
        '''
        result = self._values.get("zone_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosZoneRecord(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.RosZoneRecord",
):
    '''A ROS template type:  ``ALIYUN::PVTZ::ZoneRecord``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosZoneRecordProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::ZoneRecord``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosZoneRecordProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            def stub(props: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRecord")
    def attr_record(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Record: Record data.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRecord"))

    @builtins.property
    @jsii.member(jsii_name="attrRecordId")
    def attr_record_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: RecordId: Parsing record Id
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRecordId"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneId: Zone ID.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="rr")
    def rr(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :: " instead of empty
        :Property: rr: Host record, if you want to resolve
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "rr"))

    @rr.setter
    def rr(self, value: typing.Union[builtins.str, ros_cdk_core.IResolvable]) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rr", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: status: Allowed values: [ENABLE, DISABLE]
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "status"))

    @status.setter
    def status(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: type: Analyze record type, currently only supports A, AAAA, CNAME, TXT, MX, PTR, SRV
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Union[builtins.str, ros_cdk_core.IResolvable]) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: value: Record value
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneId: Zone Id
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: priority: MX record priority, value range [1,99]. Default to 10.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "priority"))

    @priority.setter
    def priority(
        self,
        value: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: ttl: Survival time, default is 60
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(
        self,
        value: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.RosZoneRecordProps",
    jsii_struct_bases=[],
    name_mapping={
        "rr": "rr",
        "status": "status",
        "type": "type",
        "value": "value",
        "zone_id": "zoneId",
        "priority": "priority",
        "ttl": "ttl",
    },
)
class RosZoneRecordProps:
    def __init__(
        self,
        *,
        rr: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        status: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        priority: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        ttl: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::ZoneRecord``.

        :param rr: 
        :param status: 
        :param type: 
        :param value: 
        :param zone_id: 
        :param priority: 
        :param ttl: 
        '''
        if __debug__:
            def stub(
                *,
                rr: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                status: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                priority: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                ttl: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument rr", value=rr, expected_type=type_hints["rr"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[str, typing.Any] = {
            "rr": rr,
            "status": status,
            "type": type,
            "value": value,
            "zone_id": zone_id,
        }
        if priority is not None:
            self._values["priority"] = priority
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def rr(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :: " instead of empty
        :Property: rr: Host record, if you want to resolve
        '''
        result = self._values.get("rr")
        assert result is not None, "Required property 'rr' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def status(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: status: Allowed values: [ENABLE, DISABLE]
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: type: Analyze record type, currently only supports A, AAAA, CNAME, TXT, MX, PTR, SRV
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def value(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: value: Record value
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneId: Zone Id
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def priority(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: priority: MX record priority, value range [1,99]. Default to 10.
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: ttl: Survival time, default is 60
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosZoneRecordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosZoneVpcBinder(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.RosZoneVpcBinder",
):
    '''A ROS template type:  ``ALIYUN::PVTZ::ZoneVpcBinder``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosZoneVpcBinderProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::ZoneVpcBinder``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosZoneVpcBinderProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            def stub(props: typing.Mapping[builtins.str, typing.Any]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcs")
    def attr_vpcs(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Vpcs: Vpc list
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrVpcs"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ZoneId: Zone Id
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="vpcs")
    def vpcs(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosZoneVpcBinder.VpcsProperty"]]]:
        '''
        :Property: vpcs:
        '''
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosZoneVpcBinder.VpcsProperty"]]], jsii.get(self, "vpcs"))

    @vpcs.setter
    def vpcs(
        self,
        value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosZoneVpcBinder.VpcsProperty"]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosZoneVpcBinder.VpcsProperty]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcs", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneId: Zone Id
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(
        self,
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-pvtz.RosZoneVpcBinder.VpcsProperty",
        jsii_struct_bases=[],
        name_mapping={"region_id": "regionId", "vpc_id": "vpcId"},
    )
    class VpcsProperty:
        def __init__(
            self,
            *,
            region_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        ) -> None:
            '''
            :param region_id: 
            :param vpc_id: 
            '''
            if __debug__:
                def stub(
                    *,
                    region_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                    vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument region_id", value=region_id, expected_type=type_hints["region_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[str, typing.Any] = {
                "region_id": region_id,
                "vpc_id": vpc_id,
            }

        @builtins.property
        def region_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: regionId: Vpcs attribute, region Id
            '''
            result = self._values.get("region_id")
            assert result is not None, "Required property 'region_id' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        @builtins.property
        def vpc_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: vpcId: Vpcs attribute, vpc Id
            '''
            result = self._values.get("vpc_id")
            assert result is not None, "Required property 'vpc_id' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.RosZoneVpcBinderProps",
    jsii_struct_bases=[],
    name_mapping={"vpcs": "vpcs", "zone_id": "zoneId"},
)
class RosZoneVpcBinderProps:
    def __init__(
        self,
        *,
        vpcs: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosZoneVpcBinder.VpcsProperty, typing.Dict[str, typing.Any]]]]],
        zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::ZoneVpcBinder``.

        :param vpcs: 
        :param zone_id: 
        '''
        if __debug__:
            def stub(
                *,
                vpcs: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosZoneVpcBinder.VpcsProperty, typing.Dict[str, typing.Any]]]]],
                zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpcs": vpcs,
            "zone_id": zone_id,
        }

    @builtins.property
    def vpcs(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosZoneVpcBinder.VpcsProperty]]]:
        '''
        :Property: vpcs:
        '''
        result = self._values.get("vpcs")
        assert result is not None, "Required property 'vpcs' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosZoneVpcBinder.VpcsProperty]]], result)

    @builtins.property
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: zoneId: Zone Id
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosZoneVpcBinderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserVpcAuthorization(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.UserVpcAuthorization",
):
    '''A ROS resource type:  ``ALIYUN::PVTZ::UserVpcAuthorization``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["UserVpcAuthorizationProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::UserVpcAuthorization``.

        Param scope - scope in which this resource is defined
        Param id    - scoped id of the resource
        Param props - resource properties

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[UserVpcAuthorizationProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrAuthorizedUserId")
    def attr_authorized_user_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute AuthorizedUserId: The account ID of the user who authorizes the resource.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAuthorizedUserId"))

    @builtins.property
    @jsii.member(jsii_name="attrAuthType")
    def attr_auth_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute AuthType: Authorization type.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAuthType"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.UserVpcAuthorizationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_user_id": "authorizedUserId",
        "auth_channel": "authChannel",
        "auth_code": "authCode",
        "auth_type": "authType",
        "ignore_deletion_forbidden": "ignoreDeletionForbidden",
    },
)
class UserVpcAuthorizationProps:
    def __init__(
        self,
        *,
        authorized_user_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        auth_channel: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auth_code: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ignore_deletion_forbidden: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::UserVpcAuthorization``.

        :param authorized_user_id: Property authorizedUserId: The account ID of the user who authorizes the resource.
        :param auth_channel: Property authChannel: Authorization channel. Valid values: AUTH_CODE: Verification code authorization, to verify whether the verification code passed in by AuthCode is correct. RESOURCE_DIRECTORY: Resource directory authorization, verify whether the AuthorizedUserId and the current account have resource directory credit.When it is empty, it is the same as AUTH_CODE, that is, verification code authorization.
        :param auth_code: Property authCode: Verification code, if AuthChannel takes "AUTH_CODE" or is empty, it is mandatory.
        :param auth_type: Property authType: Authorization type.
        :param ignore_deletion_forbidden: Property ignoreDeletionForbidden: Whether to ignore following deletion forbidden errors when deleting:- UserAuth.DeleteForbidden.ZoneVpcExists.
        '''
        if __debug__:
            def stub(
                *,
                authorized_user_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                auth_channel: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auth_code: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ignore_deletion_forbidden: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument authorized_user_id", value=authorized_user_id, expected_type=type_hints["authorized_user_id"])
            check_type(argname="argument auth_channel", value=auth_channel, expected_type=type_hints["auth_channel"])
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument ignore_deletion_forbidden", value=ignore_deletion_forbidden, expected_type=type_hints["ignore_deletion_forbidden"])
        self._values: typing.Dict[str, typing.Any] = {
            "authorized_user_id": authorized_user_id,
        }
        if auth_channel is not None:
            self._values["auth_channel"] = auth_channel
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if ignore_deletion_forbidden is not None:
            self._values["ignore_deletion_forbidden"] = ignore_deletion_forbidden

    @builtins.property
    def authorized_user_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property authorizedUserId: The account ID of the user who authorizes the resource.'''
        result = self._values.get("authorized_user_id")
        assert result is not None, "Required property 'authorized_user_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def auth_channel(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property authChannel: Authorization channel.

        Valid values:
        AUTH_CODE: Verification code authorization, to verify whether the verification code passed in by AuthCode is correct.
        RESOURCE_DIRECTORY: Resource directory authorization, verify whether the AuthorizedUserId and the current account have resource directory credit.When it is empty, it is the same as AUTH_CODE, that is, verification code authorization.
        '''
        result = self._values.get("auth_channel")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auth_code(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property authCode: Verification code, if AuthChannel takes "AUTH_CODE" or is empty, it is mandatory.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property authType: Authorization type.'''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ignore_deletion_forbidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''Property ignoreDeletionForbidden: Whether to ignore following deletion forbidden errors when deleting:- UserAuth.DeleteForbidden.ZoneVpcExists.'''
        result = self._values.get("ignore_deletion_forbidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserVpcAuthorizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Zone(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.Zone",
):
    '''A ROS resource type:  ``ALIYUN::PVTZ::Zone``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["ZoneProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::Zone``.

        Param scope - scope in which this resource is defined
        Param id    - scoped id of the resource
        Param props - resource properties

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[ZoneProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneId: Zone ID.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneName")
    def attr_zone_name(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneName: Zone name.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneName"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneTag")
    def attr_zone_tag(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneTag: Zone label.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneTag"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneType")
    def attr_zone_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneType: Zone type.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneType"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.ZoneProps",
    jsii_struct_bases=[],
    name_mapping={
        "zone_name": "zoneName",
        "ignored_stack_tag_keys": "ignoredStackTagKeys",
        "proxy_pattern": "proxyPattern",
        "remark": "remark",
        "resource_group_id": "resourceGroupId",
        "tags": "tags",
        "zone_tag": "zoneTag",
        "zone_type": "zoneType",
    },
)
class ZoneProps:
    def __init__(
        self,
        *,
        zone_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        ignored_stack_tag_keys: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]] = None,
        proxy_pattern: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        remark: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[RosZone.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
        zone_tag: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        zone_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::Zone``.

        :param zone_name: Property zoneName: Zone name.
        :param ignored_stack_tag_keys: Property ignoredStackTagKeys: Stack tag keys to ignore.
        :param proxy_pattern: Property proxyPattern: ZONE: completely hijack the entire zone. RECORD: Incomplete hijacking, recursive resolution agent. Default to ZONE.
        :param remark: Property remark: 50 characters at most. It can only contain numbers, Chinese, English and special characters: "_-,.，。".
        :param resource_group_id: Property resourceGroupId: Resource group id.
        :param tags: Property tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        :param zone_tag: Property zoneTag: Zone label. It will be ignored when ZoneType is AUTH_ZONE.
        :param zone_type: Property zoneType: Zone type. For instance: AUTH_ZONE, CLOUD_PRODUCT_ZONE.
        '''
        if __debug__:
            def stub(
                *,
                zone_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                ignored_stack_tag_keys: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]] = None,
                proxy_pattern: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                remark: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union[RosZone.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
                zone_tag: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                zone_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
            check_type(argname="argument ignored_stack_tag_keys", value=ignored_stack_tag_keys, expected_type=type_hints["ignored_stack_tag_keys"])
            check_type(argname="argument proxy_pattern", value=proxy_pattern, expected_type=type_hints["proxy_pattern"])
            check_type(argname="argument remark", value=remark, expected_type=type_hints["remark"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone_tag", value=zone_tag, expected_type=type_hints["zone_tag"])
            check_type(argname="argument zone_type", value=zone_type, expected_type=type_hints["zone_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "zone_name": zone_name,
        }
        if ignored_stack_tag_keys is not None:
            self._values["ignored_stack_tag_keys"] = ignored_stack_tag_keys
        if proxy_pattern is not None:
            self._values["proxy_pattern"] = proxy_pattern
        if remark is not None:
            self._values["remark"] = remark
        if resource_group_id is not None:
            self._values["resource_group_id"] = resource_group_id
        if tags is not None:
            self._values["tags"] = tags
        if zone_tag is not None:
            self._values["zone_tag"] = zone_tag
        if zone_type is not None:
            self._values["zone_type"] = zone_type

    @builtins.property
    def zone_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property zoneName: Zone name.'''
        result = self._values.get("zone_name")
        assert result is not None, "Required property 'zone_name' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def ignored_stack_tag_keys(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]]:
        '''Property ignoredStackTagKeys: Stack tag keys to ignore.'''
        result = self._values.get("ignored_stack_tag_keys")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[builtins.str, ros_cdk_core.IResolvable]]]], result)

    @builtins.property
    def proxy_pattern(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property proxyPattern: ZONE: completely hijack the entire zone.

        RECORD: Incomplete hijacking, recursive resolution agent.
        Default to ZONE.
        '''
        result = self._values.get("proxy_pattern")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def remark(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property remark: 50 characters at most.

        It can only contain numbers, Chinese, English and special characters: "_-,.，。".
        '''
        result = self._values.get("remark")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property resourceGroupId: Resource group id.'''
        result = self._values.get("resource_group_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[RosZone.TagsProperty]]:
        '''Property tags: Tags to attach to instance.

        Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[RosZone.TagsProperty]], result)

    @builtins.property
    def zone_tag(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property zoneTag: Zone label.

        It will be ignored when ZoneType is AUTH_ZONE.
        '''
        result = self._values.get("zone_tag")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def zone_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property zoneType: Zone type.

        For instance: AUTH_ZONE, CLOUD_PRODUCT_ZONE.
        '''
        result = self._values.get("zone_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneRecord(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.ZoneRecord",
):
    '''A ROS resource type:  ``ALIYUN::PVTZ::ZoneRecord``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["ZoneRecordProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::ZoneRecord``.

        Param scope - scope in which this resource is defined
        Param id    - scoped id of the resource
        Param props - resource properties

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[ZoneRecordProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrRecord")
    def attr_record(self) -> ros_cdk_core.IResolvable:
        '''Attribute Record: Record data.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRecord"))

    @builtins.property
    @jsii.member(jsii_name="attrRecordId")
    def attr_record_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute RecordId: Parsing record Id.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRecordId"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneId: Zone ID.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.ZoneRecordProps",
    jsii_struct_bases=[],
    name_mapping={
        "rr": "rr",
        "status": "status",
        "type": "type",
        "value": "value",
        "zone_id": "zoneId",
        "priority": "priority",
        "ttl": "ttl",
    },
)
class ZoneRecordProps:
    def __init__(
        self,
        *,
        rr: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        status: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        priority: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        ttl: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::ZoneRecord``.

        :param rr: Property rr: Host record, if you want to resolve @.exmaple.com, the host record should fill in "@" instead of empty.
        :param status: Property status: Allowed values: [ENABLE, DISABLE].
        :param type: Property type: Analyze record type, currently only supports A, AAAA, CNAME, TXT, MX, PTR, SRV.
        :param value: Property value: Record value.
        :param zone_id: Property zoneId: Zone Id.
        :param priority: Property priority: MX record priority, value range [1,99]. Default to 10.
        :param ttl: Property ttl: Survival time, default is 60.
        '''
        if __debug__:
            def stub(
                *,
                rr: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                status: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                priority: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                ttl: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument rr", value=rr, expected_type=type_hints["rr"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[str, typing.Any] = {
            "rr": rr,
            "status": status,
            "type": type,
            "value": value,
            "zone_id": zone_id,
        }
        if priority is not None:
            self._values["priority"] = priority
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def rr(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property rr: Host record, if you want to resolve @.exmaple.com, the host record should fill in "@" instead of empty.'''
        result = self._values.get("rr")
        assert result is not None, "Required property 'rr' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def status(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property status: Allowed values: [ENABLE, DISABLE].'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property type: Analyze record type, currently only supports A, AAAA, CNAME, TXT, MX, PTR, SRV.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def value(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property value: Record value.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property zoneId: Zone Id.'''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def priority(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property priority: MX record priority, value range [1,99].

        Default to 10.
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property ttl: Survival time, default is 60.'''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneRecordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneVpcBinder(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-pvtz.ZoneVpcBinder",
):
    '''A ROS resource type:  ``ALIYUN::PVTZ::ZoneVpcBinder``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["ZoneVpcBinderProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::PVTZ::ZoneVpcBinder``.

        Param scope - scope in which this resource is defined
        Param id    - scoped id of the resource
        Param props - resource properties

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[ZoneVpcBinderProps, typing.Dict[str, typing.Any]],
                enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrVpcs")
    def attr_vpcs(self) -> ros_cdk_core.IResolvable:
        '''Attribute Vpcs: Vpc list.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrVpcs"))

    @builtins.property
    @jsii.member(jsii_name="attrZoneId")
    def attr_zone_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute ZoneId: Zone Id.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrZoneId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-pvtz.ZoneVpcBinderProps",
    jsii_struct_bases=[],
    name_mapping={"vpcs": "vpcs", "zone_id": "zoneId"},
)
class ZoneVpcBinderProps:
    def __init__(
        self,
        *,
        vpcs: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosZoneVpcBinder.VpcsProperty, typing.Dict[str, typing.Any]]]]],
        zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::PVTZ::ZoneVpcBinder``.

        :param vpcs: Property vpcs:.
        :param zone_id: Property zoneId: Zone Id.
        '''
        if __debug__:
            def stub(
                *,
                vpcs: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosZoneVpcBinder.VpcsProperty, typing.Dict[str, typing.Any]]]]],
                zone_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpcs": vpcs,
            "zone_id": zone_id,
        }

    @builtins.property
    def vpcs(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosZoneVpcBinder.VpcsProperty]]]:
        '''Property vpcs:.'''
        result = self._values.get("vpcs")
        assert result is not None, "Required property 'vpcs' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosZoneVpcBinder.VpcsProperty]]], result)

    @builtins.property
    def zone_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property zoneId: Zone Id.'''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneVpcBinderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RosUserVpcAuthorization",
    "RosUserVpcAuthorizationProps",
    "RosZone",
    "RosZoneProps",
    "RosZoneRecord",
    "RosZoneRecordProps",
    "RosZoneVpcBinder",
    "RosZoneVpcBinderProps",
    "UserVpcAuthorization",
    "UserVpcAuthorizationProps",
    "Zone",
    "ZoneProps",
    "ZoneRecord",
    "ZoneRecordProps",
    "ZoneVpcBinder",
    "ZoneVpcBinderProps",
]

publication.publish()
