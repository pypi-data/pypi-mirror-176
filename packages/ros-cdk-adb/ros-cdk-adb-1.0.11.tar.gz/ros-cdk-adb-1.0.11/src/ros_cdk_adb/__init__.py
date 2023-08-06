'''
## Aliyun ROS ADB Construct Library

This module is part of the AliCloud ROS Cloud Development Kit (ROS CDK) project.

```python
import * as ADB from '@alicloud/ros-cdk-adb';
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


class Account(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-adb.Account",
):
    '''A ROS resource type:  ``ALIYUN::ADB::Account``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["AccountProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::ADB::Account``.

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
                props: typing.Union[AccountProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAccountName")
    def attr_account_name(self) -> ros_cdk_core.IResolvable:
        '''Attribute AccountName: The name of the account.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccountName"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountType")
    def attr_account_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute AccountType: The type of the account.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccountType"))

    @builtins.property
    @jsii.member(jsii_name="attrDbClusterId")
    def attr_db_cluster_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute DBClusterId: The ID of the cluster.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDbClusterId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-adb.AccountProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "account_password": "accountPassword",
        "db_cluster_id": "dbClusterId",
        "account_description": "accountDescription",
        "account_type": "accountType",
    },
)
class AccountProps:
    def __init__(
        self,
        *,
        account_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        account_password: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        db_cluster_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        account_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        account_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::ADB::Account``.

        :param account_name: Property accountName: The name of the account.
        :param account_password: Property accountPassword: The password of the account. The password must contain uppercase letters, lowercase letters, digits, and special characters. Special characters include ! @ # $ % ^ & * () _ + - and = The password must be 8 to 32 characters in length.
        :param db_cluster_id: Property dbClusterId: The ID of the cluster.
        :param account_description: Property accountDescription: The description of the account. The description cannot start with http://or https://. The description can be up to 256 characters in length.
        :param account_type: Property accountType: Normal: standard account Super: privileged account.
        '''
        if __debug__:
            def stub(
                *,
                account_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                account_password: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                db_cluster_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                account_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                account_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument account_password", value=account_password, expected_type=type_hints["account_password"])
            check_type(argname="argument db_cluster_id", value=db_cluster_id, expected_type=type_hints["db_cluster_id"])
            check_type(argname="argument account_description", value=account_description, expected_type=type_hints["account_description"])
            check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "account_name": account_name,
            "account_password": account_password,
            "db_cluster_id": db_cluster_id,
        }
        if account_description is not None:
            self._values["account_description"] = account_description
        if account_type is not None:
            self._values["account_type"] = account_type

    @builtins.property
    def account_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property accountName: The name of the account.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def account_password(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property accountPassword: The password of the account.

        The password must contain uppercase letters, lowercase letters, digits, and special
        characters.
        Special characters include ! @ # $ % ^ & * ()  _ + - and =
        The password must be 8 to 32 characters in length.
        '''
        result = self._values.get("account_password")
        assert result is not None, "Required property 'account_password' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def db_cluster_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property dbClusterId: The ID of the cluster.'''
        result = self._values.get("db_cluster_id")
        assert result is not None, "Required property 'db_cluster_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def account_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property accountDescription: The description of the account.

        The description cannot start with http://or https://.
        The description can be up to 256 characters in length.
        '''
        result = self._values.get("account_description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def account_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property accountType: Normal: standard account Super: privileged account.'''
        result = self._values.get("account_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DBCluster(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-adb.DBCluster",
):
    '''A ROS resource type:  ``ALIYUN::ADB::DBCluster``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["DBClusterProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::ADB::DBCluster``.

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
                props: typing.Union[DBClusterProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrConnectionString")
    def attr_connection_string(self) -> ros_cdk_core.IResolvable:
        '''Attribute ConnectionString: Vpc connection string.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="attrDbClusterId")
    def attr_db_cluster_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute DBClusterId: The ID of the cluster.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDbClusterId"))

    @builtins.property
    @jsii.member(jsii_name="attrOrderId")
    def attr_order_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute OrderId: The ID of the order.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrOrderId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-adb.DBClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_cluster_category": "dbClusterCategory",
        "db_cluster_version": "dbClusterVersion",
        "mode": "mode",
        "pay_type": "payType",
        "vpc_id": "vpcId",
        "v_switch_id": "vSwitchId",
        "compute_resource": "computeResource",
        "db_cluster_class": "dbClusterClass",
        "db_cluster_description": "dbClusterDescription",
        "db_node_group_count": "dbNodeGroupCount",
        "db_node_storage": "dbNodeStorage",
        "elastic_io_resource": "elasticIoResource",
        "executor_count": "executorCount",
        "period": "period",
        "period_type": "periodType",
        "resource_group_id": "resourceGroupId",
        "tags": "tags",
        "zone_id": "zoneId",
    },
)
class DBClusterProps:
    def __init__(
        self,
        *,
        db_cluster_category: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        db_cluster_version: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        mode: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        pay_type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        v_switch_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        compute_resource: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_cluster_class: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_cluster_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_node_group_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        db_node_storage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        elastic_io_resource: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        executor_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        period: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        period_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["RosDBCluster.TagsProperty", typing.Dict[str, typing.Any]]]] = None,
        zone_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::ADB::DBCluster``.

        :param db_cluster_category: Property dbClusterCategory: The edition of the cluster. Valid values when the cluster is in reserved mode: Basic Cluster When the cluster is in elastic mode, set the value to MixedStorage.
        :param db_cluster_version: Property dbClusterVersion: The version of the cluster. Set the value to 3.0.
        :param mode: Property mode: The mode of the cluster. Valid values: Reserver: the reserved mode Flexible: the elastic mode
        :param pay_type: Property payType: The billing method of the cluster. Valid values: Postpaid: pay-as-you-go Prepaid: subscription
        :param vpc_id: Property vpcId: The ID of the VPC.
        :param v_switch_id: Property vSwitchId: The ID of the vSwitch.
        :param compute_resource: Property computeResource: The computing resource of the cluster. This parameter is required in elastic mode.
        :param db_cluster_class: Property dbClusterClass: The specification of the cluster. This parameter is required in reserved mode. Valid values: Basic Edition: T8, T16, T32, and T52 Cluster Edition: C8 and C32
        :param db_cluster_description: Property dbClusterDescription: The description of the cluster.
        :param db_node_group_count: Property dbNodeGroupCount: The number of node groups. This parameter is required in reserved mode. Valid values: T8, T16, T32, and T52: 1 C8 and C32: 1 to 128
        :param db_node_storage: Property dbNodeStorage: The storage space of the node. This parameter is required in reserved mode. Unit: GB. Valid values: T8: 100 to 500 T16 and T32: 100 to 2000 T52: 100 to 4000 C8: 100 to 1000 C32: 100 to 8000 Note The storage space less than 1,000 GB increases in increments of 100 GB. The storage space greater than 1,000 GB increases in increments of 1,000 GB.
        :param elastic_io_resource: Property elasticIoResource: Elastic IO Unit Note the flexible mode cluster will use this parameter.
        :param executor_count: Property executorCount: ExecutorCount.
        :param period: Property period: Valid values when the Period parameter is set to Month: 1, 2, 3, 4, 5, 6, 7, 8, and 9. Valid values when the Period parameter is set to Year: 1, 2, and 3.
        :param period_type: Property periodType: The subscription period for the cluster. This parameter is required if the PayType parameter is set to Prepaid. Valid values: Year: subscription on a yearly basis Month: subscription on a monthly basis
        :param resource_group_id: Property resourceGroupId: The ID of the resource group.
        :param tags: Property tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        :param zone_id: Property zoneId: The zone ID of the cluster. You can call the DescribeRegions operation to query the most recent zone list.
        '''
        if __debug__:
            def stub(
                *,
                db_cluster_category: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                db_cluster_version: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                mode: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                pay_type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                v_switch_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                compute_resource: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_cluster_class: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_cluster_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_node_group_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                db_node_storage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                elastic_io_resource: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                executor_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                period: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                period_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union[RosDBCluster.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
                zone_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument db_cluster_category", value=db_cluster_category, expected_type=type_hints["db_cluster_category"])
            check_type(argname="argument db_cluster_version", value=db_cluster_version, expected_type=type_hints["db_cluster_version"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument pay_type", value=pay_type, expected_type=type_hints["pay_type"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument v_switch_id", value=v_switch_id, expected_type=type_hints["v_switch_id"])
            check_type(argname="argument compute_resource", value=compute_resource, expected_type=type_hints["compute_resource"])
            check_type(argname="argument db_cluster_class", value=db_cluster_class, expected_type=type_hints["db_cluster_class"])
            check_type(argname="argument db_cluster_description", value=db_cluster_description, expected_type=type_hints["db_cluster_description"])
            check_type(argname="argument db_node_group_count", value=db_node_group_count, expected_type=type_hints["db_node_group_count"])
            check_type(argname="argument db_node_storage", value=db_node_storage, expected_type=type_hints["db_node_storage"])
            check_type(argname="argument elastic_io_resource", value=elastic_io_resource, expected_type=type_hints["elastic_io_resource"])
            check_type(argname="argument executor_count", value=executor_count, expected_type=type_hints["executor_count"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "db_cluster_category": db_cluster_category,
            "db_cluster_version": db_cluster_version,
            "mode": mode,
            "pay_type": pay_type,
            "vpc_id": vpc_id,
            "v_switch_id": v_switch_id,
        }
        if compute_resource is not None:
            self._values["compute_resource"] = compute_resource
        if db_cluster_class is not None:
            self._values["db_cluster_class"] = db_cluster_class
        if db_cluster_description is not None:
            self._values["db_cluster_description"] = db_cluster_description
        if db_node_group_count is not None:
            self._values["db_node_group_count"] = db_node_group_count
        if db_node_storage is not None:
            self._values["db_node_storage"] = db_node_storage
        if elastic_io_resource is not None:
            self._values["elastic_io_resource"] = elastic_io_resource
        if executor_count is not None:
            self._values["executor_count"] = executor_count
        if period is not None:
            self._values["period"] = period
        if period_type is not None:
            self._values["period_type"] = period_type
        if resource_group_id is not None:
            self._values["resource_group_id"] = resource_group_id
        if tags is not None:
            self._values["tags"] = tags
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def db_cluster_category(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property dbClusterCategory: The edition of the cluster.

        Valid values when the cluster is in reserved mode:
        Basic
        Cluster
        When the cluster is in elastic mode, set the value to MixedStorage.
        '''
        result = self._values.get("db_cluster_category")
        assert result is not None, "Required property 'db_cluster_category' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def db_cluster_version(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property dbClusterVersion: The version of the cluster.

        Set the value to 3.0.
        '''
        result = self._values.get("db_cluster_version")
        assert result is not None, "Required property 'db_cluster_version' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def mode(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property mode: The mode of the cluster.

        Valid values:
        Reserver: the reserved mode
        Flexible: the elastic mode
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def pay_type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property payType: The billing method of the cluster.

        Valid values:
        Postpaid: pay-as-you-go
        Prepaid: subscription
        '''
        result = self._values.get("pay_type")
        assert result is not None, "Required property 'pay_type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def vpc_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property vpcId: The ID of the VPC.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def v_switch_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property vSwitchId: The ID of the vSwitch.'''
        result = self._values.get("v_switch_id")
        assert result is not None, "Required property 'v_switch_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def compute_resource(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property computeResource: The computing resource of the cluster.

        This parameter is required in elastic mode.
        '''
        result = self._values.get("compute_resource")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_cluster_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property dbClusterClass: The specification of the cluster.

        This parameter is required in reserved mode. Valid values:
        Basic Edition: T8, T16, T32, and T52
        Cluster Edition: C8 and C32
        '''
        result = self._values.get("db_cluster_class")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_cluster_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property dbClusterDescription: The description of the cluster.'''
        result = self._values.get("db_cluster_description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_node_group_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property dbNodeGroupCount: The number of node groups.

        This parameter is required in reserved mode. Valid values:
        T8, T16, T32, and T52: 1
        C8 and C32: 1 to 128
        '''
        result = self._values.get("db_node_group_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_node_storage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property dbNodeStorage: The storage space of the node.

        This parameter is required in reserved mode. Unit: GB. Valid values:
        T8: 100 to 500
        T16 and T32: 100 to 2000
        T52: 100 to 4000
        C8: 100 to 1000
        C32: 100 to 8000
        Note The storage space less than 1,000 GB increases in increments of 100 GB. The storage space greater than 1,000 GB increases in increments of 1,000 GB.
        '''
        result = self._values.get("db_node_storage")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def elastic_io_resource(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property elasticIoResource: Elastic IO Unit Note the flexible mode cluster will use this parameter.'''
        result = self._values.get("elastic_io_resource")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def executor_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property executorCount: ExecutorCount.'''
        result = self._values.get("executor_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def period(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property period: Valid values when the Period parameter is set to Month: 1, 2, 3, 4, 5, 6, 7, 8, and 9.

        Valid values when the Period parameter is set to Year: 1, 2, and 3.
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def period_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property periodType: The subscription period for the cluster.

        This parameter is required if the PayType parameter is set to Prepaid. Valid values:
        Year: subscription on a yearly basis
        Month: subscription on a monthly basis
        '''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property resourceGroupId: The ID of the resource group.'''
        result = self._values.get("resource_group_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["RosDBCluster.TagsProperty"]]:
        '''Property tags: Tags to attach to instance.

        Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["RosDBCluster.TagsProperty"]], result)

    @builtins.property
    def zone_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property zoneId: The zone ID of the cluster.

        You can call the DescribeRegions operation to query the most recent zone list.
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DBClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosAccount(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-adb.RosAccount",
):
    '''A ROS template type:  ``ALIYUN::ADB::Account``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosAccountProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::ADB::Account``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosAccountProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAccountName")
    def attr_account_name(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AccountName: The name of the account.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccountName"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountType")
    def attr_account_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AccountType: The type of the account.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccountType"))

    @builtins.property
    @jsii.member(jsii_name="attrDbClusterId")
    def attr_db_cluster_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: DBClusterId: The ID of the cluster.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDbClusterId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: accountName: The name of the account.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(
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
        jsii.set(self, "accountName", value)

    @builtins.property
    @jsii.member(jsii_name="accountPassword")
    def account_password(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        ::



        $ % ^ & * ()  _ + - and =

        The password must be 8 to 32 characters in length.
        :Property:

        accountPassword: The password of the account.
        The password must contain uppercase letters, lowercase letters, digits, and special
        characters.
        Special characters include !
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "accountPassword"))

    @account_password.setter
    def account_password(
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
        jsii.set(self, "accountPassword", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterId")
    def db_cluster_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: dbClusterId: The ID of the cluster.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "dbClusterId"))

    @db_cluster_id.setter
    def db_cluster_id(
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
        jsii.set(self, "dbClusterId", value)

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
    @jsii.member(jsii_name="accountDescription")
    def account_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        accountDescription: The description of the account.
        The description cannot start with http://or https://.
        The description can be up to 256 characters in length.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "accountDescription"))

    @account_description.setter
    def account_description(
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
        jsii.set(self, "accountDescription", value)

    @builtins.property
    @jsii.member(jsii_name="accountType")
    def account_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        accountType: Normal: standard account
        Super: privileged account
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "accountType"))

    @account_type.setter
    def account_type(
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
        jsii.set(self, "accountType", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-adb.RosAccountProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "account_password": "accountPassword",
        "db_cluster_id": "dbClusterId",
        "account_description": "accountDescription",
        "account_type": "accountType",
    },
)
class RosAccountProps:
    def __init__(
        self,
        *,
        account_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        account_password: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        db_cluster_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        account_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        account_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::ADB::Account``.

        :param account_name: 
        :param account_password: 
        :param db_cluster_id: 
        :param account_description: 
        :param account_type: 
        '''
        if __debug__:
            def stub(
                *,
                account_name: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                account_password: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                db_cluster_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                account_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                account_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument account_password", value=account_password, expected_type=type_hints["account_password"])
            check_type(argname="argument db_cluster_id", value=db_cluster_id, expected_type=type_hints["db_cluster_id"])
            check_type(argname="argument account_description", value=account_description, expected_type=type_hints["account_description"])
            check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "account_name": account_name,
            "account_password": account_password,
            "db_cluster_id": db_cluster_id,
        }
        if account_description is not None:
            self._values["account_description"] = account_description
        if account_type is not None:
            self._values["account_type"] = account_type

    @builtins.property
    def account_name(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: accountName: The name of the account.
        '''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def account_password(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        ::



        $ % ^ & * ()  _ + - and =

        The password must be 8 to 32 characters in length.
        :Property:

        accountPassword: The password of the account.
        The password must contain uppercase letters, lowercase letters, digits, and special
        characters.
        Special characters include !
        '''
        result = self._values.get("account_password")
        assert result is not None, "Required property 'account_password' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def db_cluster_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: dbClusterId: The ID of the cluster.
        '''
        result = self._values.get("db_cluster_id")
        assert result is not None, "Required property 'db_cluster_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def account_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        accountDescription: The description of the account.
        The description cannot start with http://or https://.
        The description can be up to 256 characters in length.
        '''
        result = self._values.get("account_description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def account_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        accountType: Normal: standard account
        Super: privileged account
        '''
        result = self._values.get("account_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosDBCluster(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-adb.RosDBCluster",
):
    '''A ROS template type:  ``ALIYUN::ADB::DBCluster``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosDBClusterProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::ADB::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosDBClusterProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrConnectionString")
    def attr_connection_string(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ConnectionString: Vpc connection string.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="attrDbClusterId")
    def attr_db_cluster_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: DBClusterId: The ID of the cluster.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDbClusterId"))

    @builtins.property
    @jsii.member(jsii_name="attrOrderId")
    def attr_order_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: OrderId: The ID of the order.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrOrderId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="dbClusterCategory")
    def db_cluster_category(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        dbClusterCategory: The edition of the cluster.
        Valid values when the cluster is in reserved mode:
        Basic
        Cluster
        When the cluster is in elastic mode, set the value to MixedStorage.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "dbClusterCategory"))

    @db_cluster_category.setter
    def db_cluster_category(
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
        jsii.set(self, "dbClusterCategory", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterVersion")
    def db_cluster_version(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: dbClusterVersion: The version of the cluster. Set the value to 3.0.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "dbClusterVersion"))

    @db_cluster_version.setter
    def db_cluster_version(
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
        jsii.set(self, "dbClusterVersion", value)

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
    @jsii.member(jsii_name="mode")
    def mode(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        mode: The mode of the cluster. Valid values:
        Reserver: the reserved mode
        Flexible: the elastic mode
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: typing.Union[builtins.str, ros_cdk_core.IResolvable]) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="payType")
    def pay_type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        payType: The billing method of the cluster. Valid values:
        Postpaid: pay-as-you-go
        Prepaid: subscription
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "payType"))

    @pay_type.setter
    def pay_type(
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
        jsii.set(self, "payType", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: vpcId: The ID of the VPC.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(
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
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="vSwitchId")
    def v_switch_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: vSwitchId: The ID of the vSwitch.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "vSwitchId"))

    @v_switch_id.setter
    def v_switch_id(
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
        jsii.set(self, "vSwitchId", value)

    @builtins.property
    @jsii.member(jsii_name="computeResource")
    def compute_resource(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: computeResource: The computing resource of the cluster. This parameter is required in elastic mode.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "computeResource"))

    @compute_resource.setter
    def compute_resource(
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
        jsii.set(self, "computeResource", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterClass")
    def db_cluster_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbClusterClass: The specification of the cluster. This parameter is required in reserved mode. Valid values:
        Basic Edition: T8, T16, T32, and T52
        Cluster Edition: C8 and C32
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "dbClusterClass"))

    @db_cluster_class.setter
    def db_cluster_class(
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
        jsii.set(self, "dbClusterClass", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterDescription")
    def db_cluster_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: dbClusterDescription: The description of the cluster.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "dbClusterDescription"))

    @db_cluster_description.setter
    def db_cluster_description(
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
        jsii.set(self, "dbClusterDescription", value)

    @builtins.property
    @jsii.member(jsii_name="dbNodeGroupCount")
    def db_node_group_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbNodeGroupCount: The number of node groups. This parameter is required in reserved mode. Valid values:
        T8, T16, T32, and T52: 1
        C8 and C32: 1 to 128
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "dbNodeGroupCount"))

    @db_node_group_count.setter
    def db_node_group_count(
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
        jsii.set(self, "dbNodeGroupCount", value)

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorage")
    def db_node_storage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbNodeStorage: The storage space of the node. This parameter is required in reserved mode. Unit: GB. Valid values:
        T8: 100 to 500
        T16 and T32: 100 to 2000
        T52: 100 to 4000
        C8: 100 to 1000
        C32: 100 to 8000
        Note The storage space less than 1,000 GB increases in increments of 100 GB. The storage space greater than 1,000 GB increases in increments of 1,000 GB.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "dbNodeStorage"))

    @db_node_storage.setter
    def db_node_storage(
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
        jsii.set(self, "dbNodeStorage", value)

    @builtins.property
    @jsii.member(jsii_name="elasticIoResource")
    def elastic_io_resource(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        elasticIoResource: Elastic IO Unit
        Note the flexible mode cluster will use this parameter.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "elasticIoResource"))

    @elastic_io_resource.setter
    def elastic_io_resource(
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
        jsii.set(self, "elasticIoResource", value)

    @builtins.property
    @jsii.member(jsii_name="executorCount")
    def executor_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: executorCount: ExecutorCount
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "executorCount"))

    @executor_count.setter
    def executor_count(
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
        jsii.set(self, "executorCount", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        period: Valid values when the Period parameter is set to Month: 1, 2, 3, 4, 5, 6, 7, 8, and 9.
        Valid values when the Period parameter is set to Year: 1, 2, and 3.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "period"))

    @period.setter
    def period(
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
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        periodType: The subscription period for the cluster. This parameter is required if the PayType parameter is set to Prepaid. Valid values:
        Year: subscription on a yearly basis
        Month: subscription on a monthly basis
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(
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
        jsii.set(self, "periodType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: resourceGroupId: The ID of the resource group.
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
    def tags(self) -> typing.Optional[typing.List["RosDBCluster.TagsProperty"]]:
        '''
        :Property: tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        return typing.cast(typing.Optional[typing.List["RosDBCluster.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["RosDBCluster.TagsProperty"]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.List[RosDBCluster.TagsProperty]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneId: The zone ID of the cluster. You can call the DescribeRegions operation to query the most recent zone list.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(
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
        jsii.set(self, "zoneId", value)

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-adb.RosDBCluster.TagsProperty",
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
    jsii_type="@alicloud/ros-cdk-adb.RosDBClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_cluster_category": "dbClusterCategory",
        "db_cluster_version": "dbClusterVersion",
        "mode": "mode",
        "pay_type": "payType",
        "vpc_id": "vpcId",
        "v_switch_id": "vSwitchId",
        "compute_resource": "computeResource",
        "db_cluster_class": "dbClusterClass",
        "db_cluster_description": "dbClusterDescription",
        "db_node_group_count": "dbNodeGroupCount",
        "db_node_storage": "dbNodeStorage",
        "elastic_io_resource": "elasticIoResource",
        "executor_count": "executorCount",
        "period": "period",
        "period_type": "periodType",
        "resource_group_id": "resourceGroupId",
        "tags": "tags",
        "zone_id": "zoneId",
    },
)
class RosDBClusterProps:
    def __init__(
        self,
        *,
        db_cluster_category: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        db_cluster_version: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        mode: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        pay_type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        v_switch_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        compute_resource: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_cluster_class: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_cluster_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        db_node_group_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        db_node_storage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        elastic_io_resource: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        executor_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        period: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        period_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[RosDBCluster.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
        zone_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::ADB::DBCluster``.

        :param db_cluster_category: 
        :param db_cluster_version: 
        :param mode: 
        :param pay_type: 
        :param vpc_id: 
        :param v_switch_id: 
        :param compute_resource: 
        :param db_cluster_class: 
        :param db_cluster_description: 
        :param db_node_group_count: 
        :param db_node_storage: 
        :param elastic_io_resource: 
        :param executor_count: 
        :param period: 
        :param period_type: 
        :param resource_group_id: 
        :param tags: 
        :param zone_id: 
        '''
        if __debug__:
            def stub(
                *,
                db_cluster_category: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                db_cluster_version: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                mode: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                pay_type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                vpc_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                v_switch_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                compute_resource: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_cluster_class: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_cluster_description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                db_node_group_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                db_node_storage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                elastic_io_resource: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                executor_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                period: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                period_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                resource_group_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union[RosDBCluster.TagsProperty, typing.Dict[str, typing.Any]]]] = None,
                zone_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument db_cluster_category", value=db_cluster_category, expected_type=type_hints["db_cluster_category"])
            check_type(argname="argument db_cluster_version", value=db_cluster_version, expected_type=type_hints["db_cluster_version"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument pay_type", value=pay_type, expected_type=type_hints["pay_type"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument v_switch_id", value=v_switch_id, expected_type=type_hints["v_switch_id"])
            check_type(argname="argument compute_resource", value=compute_resource, expected_type=type_hints["compute_resource"])
            check_type(argname="argument db_cluster_class", value=db_cluster_class, expected_type=type_hints["db_cluster_class"])
            check_type(argname="argument db_cluster_description", value=db_cluster_description, expected_type=type_hints["db_cluster_description"])
            check_type(argname="argument db_node_group_count", value=db_node_group_count, expected_type=type_hints["db_node_group_count"])
            check_type(argname="argument db_node_storage", value=db_node_storage, expected_type=type_hints["db_node_storage"])
            check_type(argname="argument elastic_io_resource", value=elastic_io_resource, expected_type=type_hints["elastic_io_resource"])
            check_type(argname="argument executor_count", value=executor_count, expected_type=type_hints["executor_count"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "db_cluster_category": db_cluster_category,
            "db_cluster_version": db_cluster_version,
            "mode": mode,
            "pay_type": pay_type,
            "vpc_id": vpc_id,
            "v_switch_id": v_switch_id,
        }
        if compute_resource is not None:
            self._values["compute_resource"] = compute_resource
        if db_cluster_class is not None:
            self._values["db_cluster_class"] = db_cluster_class
        if db_cluster_description is not None:
            self._values["db_cluster_description"] = db_cluster_description
        if db_node_group_count is not None:
            self._values["db_node_group_count"] = db_node_group_count
        if db_node_storage is not None:
            self._values["db_node_storage"] = db_node_storage
        if elastic_io_resource is not None:
            self._values["elastic_io_resource"] = elastic_io_resource
        if executor_count is not None:
            self._values["executor_count"] = executor_count
        if period is not None:
            self._values["period"] = period
        if period_type is not None:
            self._values["period_type"] = period_type
        if resource_group_id is not None:
            self._values["resource_group_id"] = resource_group_id
        if tags is not None:
            self._values["tags"] = tags
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def db_cluster_category(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        dbClusterCategory: The edition of the cluster.
        Valid values when the cluster is in reserved mode:
        Basic
        Cluster
        When the cluster is in elastic mode, set the value to MixedStorage.
        '''
        result = self._values.get("db_cluster_category")
        assert result is not None, "Required property 'db_cluster_category' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def db_cluster_version(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: dbClusterVersion: The version of the cluster. Set the value to 3.0.
        '''
        result = self._values.get("db_cluster_version")
        assert result is not None, "Required property 'db_cluster_version' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def mode(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        mode: The mode of the cluster. Valid values:
        Reserver: the reserved mode
        Flexible: the elastic mode
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def pay_type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        payType: The billing method of the cluster. Valid values:
        Postpaid: pay-as-you-go
        Prepaid: subscription
        '''
        result = self._values.get("pay_type")
        assert result is not None, "Required property 'pay_type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def vpc_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: vpcId: The ID of the VPC.
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def v_switch_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: vSwitchId: The ID of the vSwitch.
        '''
        result = self._values.get("v_switch_id")
        assert result is not None, "Required property 'v_switch_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def compute_resource(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: computeResource: The computing resource of the cluster. This parameter is required in elastic mode.
        '''
        result = self._values.get("compute_resource")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_cluster_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbClusterClass: The specification of the cluster. This parameter is required in reserved mode. Valid values:
        Basic Edition: T8, T16, T32, and T52
        Cluster Edition: C8 and C32
        '''
        result = self._values.get("db_cluster_class")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_cluster_description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: dbClusterDescription: The description of the cluster.
        '''
        result = self._values.get("db_cluster_description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_node_group_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbNodeGroupCount: The number of node groups. This parameter is required in reserved mode. Valid values:
        T8, T16, T32, and T52: 1
        C8 and C32: 1 to 128
        '''
        result = self._values.get("db_node_group_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def db_node_storage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        dbNodeStorage: The storage space of the node. This parameter is required in reserved mode. Unit: GB. Valid values:
        T8: 100 to 500
        T16 and T32: 100 to 2000
        T52: 100 to 4000
        C8: 100 to 1000
        C32: 100 to 8000
        Note The storage space less than 1,000 GB increases in increments of 100 GB. The storage space greater than 1,000 GB increases in increments of 1,000 GB.
        '''
        result = self._values.get("db_node_storage")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def elastic_io_resource(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        elasticIoResource: Elastic IO Unit
        Note the flexible mode cluster will use this parameter.
        '''
        result = self._values.get("elastic_io_resource")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def executor_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: executorCount: ExecutorCount
        '''
        result = self._values.get("executor_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def period(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        period: Valid values when the Period parameter is set to Month: 1, 2, 3, 4, 5, 6, 7, 8, and 9.
        Valid values when the Period parameter is set to Year: 1, 2, and 3.
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def period_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        periodType: The subscription period for the cluster. This parameter is required if the PayType parameter is set to Prepaid. Valid values:
        Year: subscription on a yearly basis
        Month: subscription on a monthly basis
        '''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def resource_group_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: resourceGroupId: The ID of the resource group.
        '''
        result = self._values.get("resource_group_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[RosDBCluster.TagsProperty]]:
        '''
        :Property: tags: Tags to attach to instance. Max support 20 tags to add during create instance. Each tag with two properties Key and Value, and Key is required.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[RosDBCluster.TagsProperty]], result)

    @builtins.property
    def zone_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: zoneId: The zone ID of the cluster. You can call the DescribeRegions operation to query the most recent zone list.
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosDBClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Account",
    "AccountProps",
    "DBCluster",
    "DBClusterProps",
    "RosAccount",
    "RosAccountProps",
    "RosDBCluster",
    "RosDBClusterProps",
]

publication.publish()
