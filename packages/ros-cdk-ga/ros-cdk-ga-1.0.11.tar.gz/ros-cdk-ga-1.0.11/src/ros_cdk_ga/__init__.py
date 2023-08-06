'''
## Aliyun ROS GA Construct Library

This module is part of the AliCloud ROS Cloud Development Kit (ROS CDK) project.

```python
import * as GA from '@alicloud/ros-cdk-ga';
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


class Accelerator(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.Accelerator",
):
    '''A ROS resource type:  ``ALIYUN::GA::Accelerator``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["AcceleratorProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::Accelerator``.

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
                props: typing.Union[AcceleratorProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAcceleratorId")
    def attr_accelerator_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute AcceleratorId: The ID of the GA instance to query.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorId"))

    @builtins.property
    @jsii.member(jsii_name="attrAcceleratorName")
    def attr_accelerator_name(self) -> ros_cdk_core.IResolvable:
        '''Attribute AcceleratorName: The Name of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorName"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoPay")
    def attr_auto_pay(self) -> ros_cdk_core.IResolvable:
        '''Attribute AutoPay: The AutoPay of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoPay"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoUseCoupon")
    def attr_auto_use_coupon(self) -> ros_cdk_core.IResolvable:
        '''Attribute AutoUseCoupon: The AutoUseCoupon of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoUseCoupon"))

    @builtins.property
    @jsii.member(jsii_name="attrDuration")
    def attr_duration(self) -> ros_cdk_core.IResolvable:
        '''Attribute Duration: The Duration of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDuration"))

    @builtins.property
    @jsii.member(jsii_name="attrOrderId")
    def attr_order_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute OrderId: The OrderId of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrOrderId"))

    @builtins.property
    @jsii.member(jsii_name="attrPaymentType")
    def attr_payment_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute PaymentType: The Payment Typethe GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPaymentType"))

    @builtins.property
    @jsii.member(jsii_name="attrPricingCycle")
    def attr_pricing_cycle(self) -> ros_cdk_core.IResolvable:
        '''Attribute PricingCycle: The PricingCycle of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPricingCycle"))

    @builtins.property
    @jsii.member(jsii_name="attrSpec")
    def attr_spec(self) -> ros_cdk_core.IResolvable:
        '''Attribute Spec: The instance type of the GA instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrSpec"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.AcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "pricing_cycle": "pricingCycle",
        "spec": "spec",
        "accelerator_name": "acceleratorName",
        "auto_pay": "autoPay",
        "auto_use_coupon": "autoUseCoupon",
    },
)
class AcceleratorProps:
    def __init__(
        self,
        *,
        duration: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        pricing_cycle: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        spec: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        accelerator_name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auto_pay: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::Accelerator``.

        :param duration: Property duration: The Duration of the GA instance.
        :param pricing_cycle: Property pricingCycle: The PricingCycle of the GA instance.
        :param spec: Property spec: The instance type of the GA instance.
        :param accelerator_name: Property acceleratorName: The Name of the GA instance.
        :param auto_pay: Property autoPay: The AutoPay of the GA instance.
        :param auto_use_coupon: Property autoUseCoupon: The AutoUseCoupon of the GA instance.
        '''
        if __debug__:
            def stub(
                *,
                duration: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                pricing_cycle: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                spec: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                accelerator_name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auto_pay: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument pricing_cycle", value=pricing_cycle, expected_type=type_hints["pricing_cycle"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument accelerator_name", value=accelerator_name, expected_type=type_hints["accelerator_name"])
            check_type(argname="argument auto_pay", value=auto_pay, expected_type=type_hints["auto_pay"])
            check_type(argname="argument auto_use_coupon", value=auto_use_coupon, expected_type=type_hints["auto_use_coupon"])
        self._values: typing.Dict[str, typing.Any] = {
            "duration": duration,
            "pricing_cycle": pricing_cycle,
            "spec": spec,
        }
        if accelerator_name is not None:
            self._values["accelerator_name"] = accelerator_name
        if auto_pay is not None:
            self._values["auto_pay"] = auto_pay
        if auto_use_coupon is not None:
            self._values["auto_use_coupon"] = auto_use_coupon

    @builtins.property
    def duration(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property duration: The Duration of the GA instance.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def pricing_cycle(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property pricingCycle: The PricingCycle of the GA instance.'''
        result = self._values.get("pricing_cycle")
        assert result is not None, "Required property 'pricing_cycle' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def spec(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property spec: The instance type of the GA instance.'''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def accelerator_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property acceleratorName: The Name of the GA instance.'''
        result = self._values.get("accelerator_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property autoPay: The AutoPay of the GA instance.'''
        result = self._values.get("auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property autoUseCoupon: The AutoUseCoupon of the GA instance.'''
        result = self._values.get("auto_use_coupon")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BandwidthPackage(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.BandwidthPackage",
):
    '''A ROS resource type:  ``ALIYUN::GA::BandwidthPackage``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["BandwidthPackageProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::BandwidthPackage``.

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
                props: typing.Union[BandwidthPackageProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAutoPay")
    def attr_auto_pay(self) -> ros_cdk_core.IResolvable:
        '''Attribute AutoPay: The AutoPay of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoPay"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoUseCoupon")
    def attr_auto_use_coupon(self) -> ros_cdk_core.IResolvable:
        '''Attribute AutoUseCoupon: The AutoUseCoupon  of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoUseCoupon"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidth")
    def attr_bandwidth(self) -> ros_cdk_core.IResolvable:
        '''Attribute Bandwidth: The bandwidth provided by the bandwidth plan.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageId")
    def attr_bandwidth_package_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute BandwidthPackageId: The Resource ID of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageId"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageName")
    def attr_bandwidth_package_name(self) -> ros_cdk_core.IResolvable:
        '''Attribute BandwidthPackageName: The Resource name of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageName"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthType")
    def attr_bandwidth_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute BandwidthType: the bandwidth BandwidthType of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthType"))

    @builtins.property
    @jsii.member(jsii_name="attrBillingType")
    def attr_billing_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute BillingType: The BillingType of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBillingType"))

    @builtins.property
    @jsii.member(jsii_name="attrCbnGeographicRegionIdA")
    def attr_cbn_geographic_region_id_a(self) -> ros_cdk_core.IResolvable:
        '''Attribute CbnGeographicRegionIdA: The CbnGeographicRegionIdA  of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrCbnGeographicRegionIdA"))

    @builtins.property
    @jsii.member(jsii_name="attrCbnGeographicRegionIdB")
    def attr_cbn_geographic_region_id_b(self) -> ros_cdk_core.IResolvable:
        '''Attribute CbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrCbnGeographicRegionIdB"))

    @builtins.property
    @jsii.member(jsii_name="attrChargeType")
    def attr_charge_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute ChargeType: The ChargeType of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrChargeType"))

    @builtins.property
    @jsii.member(jsii_name="attrPaymentType")
    def attr_payment_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute PaymentType: The Payment Type of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPaymentType"))

    @builtins.property
    @jsii.member(jsii_name="attrRatio")
    def attr_ratio(self) -> ros_cdk_core.IResolvable:
        '''Attribute Ratio: The Ratio of the bandwidth.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRatio"))

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> ros_cdk_core.IResolvable:
        '''Attribute Type: The type of the bandwidth plan.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrType"))


class BandwidthPackageAcceleratorAddition(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.BandwidthPackageAcceleratorAddition",
):
    '''A ROS resource type:  ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["BandwidthPackageAcceleratorAdditionProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.

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
                props: typing.Union[BandwidthPackageAcceleratorAdditionProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAcceleratorId")
    def attr_accelerator_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute AcceleratorId: The ID of the Global Accelerator instance.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorId"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageId")
    def attr_bandwidth_package_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute BandwidthPackageId: The ID of the bandwidth package which is associated.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.BandwidthPackageAcceleratorAdditionProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "bandwidth_package_id": "bandwidthPackageId",
    },
)
class BandwidthPackageAcceleratorAdditionProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        bandwidth_package_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.

        :param accelerator_id: Property acceleratorId: The ID of the Global Accelerator instance with which you want to associate the bandwidth plan.
        :param bandwidth_package_id: Property bandwidthPackageId: The ID of the bandwidth package to associate.
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                bandwidth_package_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument bandwidth_package_id", value=bandwidth_package_id, expected_type=type_hints["bandwidth_package_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "bandwidth_package_id": bandwidth_package_id,
        }

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property acceleratorId: The ID of the Global Accelerator instance with which you want to associate the bandwidth plan.'''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def bandwidth_package_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property bandwidthPackageId: The ID of the bandwidth package to associate.'''
        result = self._values.get("bandwidth_package_id")
        assert result is not None, "Required property 'bandwidth_package_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BandwidthPackageAcceleratorAdditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.BandwidthPackageProps",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "type": "type",
        "auto_pay": "autoPay",
        "auto_use_coupon": "autoUseCoupon",
        "bandwidth_type": "bandwidthType",
        "billing_type": "billingType",
        "cbn_geographic_region_id_a": "cbnGeographicRegionIdA",
        "cbn_geographic_region_id_b": "cbnGeographicRegionIdB",
        "charge_type": "chargeType",
        "duration": "duration",
        "pricing_cycle": "pricingCycle",
        "ratio": "ratio",
    },
)
class BandwidthPackageProps:
    def __init__(
        self,
        *,
        bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
        type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        auto_pay: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        bandwidth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        billing_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        cbn_geographic_region_id_a: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        cbn_geographic_region_id_b: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        charge_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        duration: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        pricing_cycle: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ratio: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::BandwidthPackage``.

        :param bandwidth: Property bandwidth: The bandwidth provided by the bandwidth plan.
        :param type: Property type: The type of the bandwidth plan.
        :param auto_pay: Property autoPay: Specifies whether to enable automatic payment.
        :param auto_use_coupon: Property autoUseCoupon: The AutoUseCoupon of the bandwidth.
        :param bandwidth_type: Property bandwidthType: the bandwidth BandwidthType of the bandwidth.
        :param billing_type: Property billingType: The BillingType of the bandwidth.
        :param cbn_geographic_region_id_a: Property cbnGeographicRegionIdA: The CbnGeographicRegionIdA of the bandwidth.
        :param cbn_geographic_region_id_b: Property cbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth.
        :param charge_type: Property chargeType: The ChargeType of the bandwidth.
        :param duration: Property duration:.
        :param pricing_cycle: Property pricingCycle:.
        :param ratio: Property ratio: The Ratio of the bandwidth.
        '''
        if __debug__:
            def stub(
                *,
                bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                auto_pay: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                bandwidth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                billing_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                cbn_geographic_region_id_a: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                cbn_geographic_region_id_b: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                charge_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                duration: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                pricing_cycle: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ratio: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument auto_pay", value=auto_pay, expected_type=type_hints["auto_pay"])
            check_type(argname="argument auto_use_coupon", value=auto_use_coupon, expected_type=type_hints["auto_use_coupon"])
            check_type(argname="argument bandwidth_type", value=bandwidth_type, expected_type=type_hints["bandwidth_type"])
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument cbn_geographic_region_id_a", value=cbn_geographic_region_id_a, expected_type=type_hints["cbn_geographic_region_id_a"])
            check_type(argname="argument cbn_geographic_region_id_b", value=cbn_geographic_region_id_b, expected_type=type_hints["cbn_geographic_region_id_b"])
            check_type(argname="argument charge_type", value=charge_type, expected_type=type_hints["charge_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument pricing_cycle", value=pricing_cycle, expected_type=type_hints["pricing_cycle"])
            check_type(argname="argument ratio", value=ratio, expected_type=type_hints["ratio"])
        self._values: typing.Dict[str, typing.Any] = {
            "bandwidth": bandwidth,
            "type": type,
        }
        if auto_pay is not None:
            self._values["auto_pay"] = auto_pay
        if auto_use_coupon is not None:
            self._values["auto_use_coupon"] = auto_use_coupon
        if bandwidth_type is not None:
            self._values["bandwidth_type"] = bandwidth_type
        if billing_type is not None:
            self._values["billing_type"] = billing_type
        if cbn_geographic_region_id_a is not None:
            self._values["cbn_geographic_region_id_a"] = cbn_geographic_region_id_a
        if cbn_geographic_region_id_b is not None:
            self._values["cbn_geographic_region_id_b"] = cbn_geographic_region_id_b
        if charge_type is not None:
            self._values["charge_type"] = charge_type
        if duration is not None:
            self._values["duration"] = duration
        if pricing_cycle is not None:
            self._values["pricing_cycle"] = pricing_cycle
        if ratio is not None:
            self._values["ratio"] = ratio

    @builtins.property
    def bandwidth(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
        '''Property bandwidth: The bandwidth provided by the bandwidth plan.'''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

    @builtins.property
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property type: The type of the bandwidth plan.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''Property autoPay: Specifies whether to enable automatic payment.'''
        result = self._values.get("auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property autoUseCoupon: The AutoUseCoupon  of the bandwidth.'''
        result = self._values.get("auto_use_coupon")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def bandwidth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property bandwidthType: the bandwidth BandwidthType of the bandwidth.'''
        result = self._values.get("bandwidth_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def billing_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property billingType: The BillingType of the bandwidth.'''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def cbn_geographic_region_id_a(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property cbnGeographicRegionIdA: The CbnGeographicRegionIdA  of the bandwidth.'''
        result = self._values.get("cbn_geographic_region_id_a")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def cbn_geographic_region_id_b(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property cbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth.'''
        result = self._values.get("cbn_geographic_region_id_b")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def charge_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property chargeType: The ChargeType of the bandwidth.'''
        result = self._values.get("charge_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def duration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property duration:.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def pricing_cycle(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property pricingCycle:.'''
        result = self._values.get("pricing_cycle")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ratio(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property ratio: The Ratio of the bandwidth.'''
        result = self._values.get("ratio")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BandwidthPackageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EndpointGroup(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.EndpointGroup",
):
    '''A ROS resource type:  ``ALIYUN::GA::EndpointGroup``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["EndpointGroupProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::EndpointGroup``.

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
                props: typing.Union[EndpointGroupProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrEndpointGroupId")
    def attr_endpoint_group_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute EndpointGroupId: The ID of the endpoint group.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrEndpointGroupId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.EndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "endpoint_configurations": "endpointConfigurations",
        "endpoint_group_region": "endpointGroupRegion",
        "listener_id": "listenerId",
        "description": "description",
        "endpoint_group_type": "endpointGroupType",
        "endpoint_request_protocol": "endpointRequestProtocol",
        "health_check_enabled": "healthCheckEnabled",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "name": "name",
        "threshold_count": "thresholdCount",
        "traffic_percentage": "trafficPercentage",
    },
)
class EndpointGroupProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        endpoint_configurations: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union["RosEndpointGroup.EndpointConfigurationsProperty", typing.Dict[str, typing.Any]]]]],
        endpoint_group_region: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        listener_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        endpoint_group_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        endpoint_request_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        health_check_interval_seconds: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        health_check_path: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        health_check_port: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        health_check_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        threshold_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        traffic_percentage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::EndpointGroup``.

        :param accelerator_id: Property acceleratorId: The ID of the Global Accelerator instance with which the endpoint group will be associated.
        :param endpoint_configurations: Property endpointConfigurations:.
        :param endpoint_group_region: Property endpointGroupRegion: The region ID of the endpoint group.
        :param listener_id: Property listenerId: The ID of the listener to be associated with the endpoint group.
        :param description: Property description: The description of the endpoint group.
        :param endpoint_group_type: Property endpointGroupType: The type of the endpoint group. Valid values: default: The endpoint group is a default endpoint group. This is the default value. virtual: The endpoint group is a virtual endpoint group. Note Only HTTP and HTTPS listeners support virtual endpoint groups.
        :param endpoint_request_protocol: Property endpointRequestProtocol: The protocol used by the backend service. Valid values: http: This is the default value. https Note: You can set this parameter only when the listener that is associated with the endpoint group uses HTTP or HTTPS. For an HTTP listener, the backend service protocol must be HTTP.
        :param health_check_enabled: Property healthCheckEnabled: Specifies whether to enable the health check feature.
        :param health_check_interval_seconds: Property healthCheckIntervalSeconds: The interval between two consecutive health checks. Unit: seconds.
        :param health_check_path: Property healthCheckPath: The path set as the destination on the targets for health checks.
        :param health_check_port: Property healthCheckPort: The port that is used to connect with the targets for health checks.
        :param health_check_protocol: Property healthCheckProtocol: The protocol that is used to connect with the targets for health checks. tcp: TCP protocol http: HTTP protocol https: HTTPS protocol
        :param name: Property name: The name of the endpoint group.
        :param threshold_count: Property thresholdCount: The number of consecutive health check failures that must occur before a healthy endpoint is considered unhealthy, or the number of consecutive health check successes that must occur before an unhealthy endpoint is considered healthy. Valid values: 2 to 10. Default value: 3.
        :param traffic_percentage: Property trafficPercentage: The weight of the endpoint group when the corresponding listener is associated with multiple endpoint groups.
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                endpoint_configurations: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosEndpointGroup.EndpointConfigurationsProperty, typing.Dict[str, typing.Any]]]]],
                endpoint_group_region: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                listener_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                endpoint_group_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                endpoint_request_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                health_check_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                health_check_interval_seconds: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                health_check_path: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                health_check_port: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                health_check_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                threshold_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                traffic_percentage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument endpoint_configurations", value=endpoint_configurations, expected_type=type_hints["endpoint_configurations"])
            check_type(argname="argument endpoint_group_region", value=endpoint_group_region, expected_type=type_hints["endpoint_group_region"])
            check_type(argname="argument listener_id", value=listener_id, expected_type=type_hints["listener_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint_group_type", value=endpoint_group_type, expected_type=type_hints["endpoint_group_type"])
            check_type(argname="argument endpoint_request_protocol", value=endpoint_request_protocol, expected_type=type_hints["endpoint_request_protocol"])
            check_type(argname="argument health_check_enabled", value=health_check_enabled, expected_type=type_hints["health_check_enabled"])
            check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument threshold_count", value=threshold_count, expected_type=type_hints["threshold_count"])
            check_type(argname="argument traffic_percentage", value=traffic_percentage, expected_type=type_hints["traffic_percentage"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "endpoint_configurations": endpoint_configurations,
            "endpoint_group_region": endpoint_group_region,
            "listener_id": listener_id,
        }
        if description is not None:
            self._values["description"] = description
        if endpoint_group_type is not None:
            self._values["endpoint_group_type"] = endpoint_group_type
        if endpoint_request_protocol is not None:
            self._values["endpoint_request_protocol"] = endpoint_request_protocol
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if name is not None:
            self._values["name"] = name
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if traffic_percentage is not None:
            self._values["traffic_percentage"] = traffic_percentage

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property acceleratorId: The ID of the Global Accelerator instance with which the endpoint group will be associated.'''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def endpoint_configurations(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosEndpointGroup.EndpointConfigurationsProperty"]]]:
        '''Property endpointConfigurations:.'''
        result = self._values.get("endpoint_configurations")
        assert result is not None, "Required property 'endpoint_configurations' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosEndpointGroup.EndpointConfigurationsProperty"]]], result)

    @builtins.property
    def endpoint_group_region(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property endpointGroupRegion: The region ID of the endpoint group.'''
        result = self._values.get("endpoint_group_region")
        assert result is not None, "Required property 'endpoint_group_region' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def listener_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property listenerId: The ID of the listener to be associated with the endpoint group.'''
        result = self._values.get("listener_id")
        assert result is not None, "Required property 'listener_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property description: The description of the endpoint group.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def endpoint_group_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property endpointGroupType: The type of the endpoint group.

        Valid values:
        default: The endpoint group is a default endpoint group. This is the default value.
        virtual: The endpoint group is a virtual endpoint group.
        Note Only HTTP and HTTPS listeners support virtual endpoint groups.
        '''
        result = self._values.get("endpoint_group_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def endpoint_request_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property endpointRequestProtocol: The protocol used by the backend service.

        Valid values:
        http: This is the default value.
        https
        Note: You can set this parameter only when the listener that is associated with the endpoint group uses HTTP or HTTPS.
        For an HTTP listener, the backend service protocol must be HTTP.
        '''
        result = self._values.get("endpoint_request_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''Property healthCheckEnabled: Specifies whether to enable the health check feature.'''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_interval_seconds(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property healthCheckIntervalSeconds: The interval between two consecutive health checks.

        Unit: seconds.
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property healthCheckPath: The path set as the destination on the targets for health checks.'''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_port(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property healthCheckPort: The port that is used to connect with the targets for health checks.'''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property healthCheckProtocol: The protocol that is used to connect with the targets for health checks.

        tcp: TCP protocol
        http: HTTP protocol
        https: HTTPS protocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property name: The name of the endpoint group.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def threshold_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property thresholdCount: The number of consecutive health check failures that must occur before a healthy endpoint is considered unhealthy, or the number of consecutive health check successes that must occur before an unhealthy endpoint is considered healthy.

        Valid values: 2 to 10. Default value: 3.
        '''
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def traffic_percentage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''Property trafficPercentage: The weight of the endpoint group when the corresponding listener is associated with multiple endpoint groups.'''
        result = self._values.get("traffic_percentage")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpSets(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.IpSets",
):
    '''A ROS resource type:  ``ALIYUN::GA::IpSets``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["IpSetsProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::IpSets``.

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
                props: typing.Union[IpSetsProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAccelerateRegionIds")
    def attr_accelerate_region_ids(self) -> ros_cdk_core.IResolvable:
        '''Attribute AccelerateRegionIds: The ID list of the accelerate region.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccelerateRegionIds"))

    @builtins.property
    @jsii.member(jsii_name="attrIpSetIds")
    def attr_ip_set_ids(self) -> ros_cdk_core.IResolvable:
        '''Attribute IpSetIds: The ID list of the ip set.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrIpSetIds"))

    @builtins.property
    @jsii.member(jsii_name="attrIpVersions")
    def attr_ip_versions(self) -> ros_cdk_core.IResolvable:
        '''Attribute IpVersions: The IP version list of the accelerate region.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrIpVersions"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.IpSetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerate_region": "accelerateRegion",
        "accelerator_id": "acceleratorId",
    },
)
class IpSetsProps:
    def __init__(
        self,
        *,
        accelerate_region: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union["RosIpSets.AccelerateRegionProperty", typing.Dict[str, typing.Any]]]]],
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::IpSets``.

        :param accelerate_region: Property accelerateRegion:.
        :param accelerator_id: Property acceleratorId: The ID of the GA instance.
        '''
        if __debug__:
            def stub(
                *,
                accelerate_region: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosIpSets.AccelerateRegionProperty, typing.Dict[str, typing.Any]]]]],
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerate_region", value=accelerate_region, expected_type=type_hints["accelerate_region"])
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerate_region": accelerate_region,
            "accelerator_id": accelerator_id,
        }

    @builtins.property
    def accelerate_region(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosIpSets.AccelerateRegionProperty"]]]:
        '''Property accelerateRegion:.'''
        result = self._values.get("accelerate_region")
        assert result is not None, "Required property 'accelerate_region' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosIpSets.AccelerateRegionProperty"]]], result)

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property acceleratorId: The ID of the GA instance.'''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpSetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Listener(
    ros_cdk_core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.Listener",
):
    '''A ROS resource type:  ``ALIYUN::GA::Listener``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["ListenerProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``ALIYUN::GA::Listener``.

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
                props: typing.Union[ListenerProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrListenerId")
    def attr_listener_id(self) -> ros_cdk_core.IResolvable:
        '''Attribute ListenerId: The ID of the listener.'''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrListenerId"))


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.ListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "port_ranges": "portRanges",
        "protocol": "protocol",
        "certificates": "certificates",
        "client_affinity": "clientAffinity",
        "description": "description",
        "name": "name",
        "proxy_protocol": "proxyProtocol",
        "security_policy_id": "securityPolicyId",
        "x_forwarded_for_config": "xForwardedForConfig",
    },
)
class ListenerProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        port_ranges: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union["RosListener.PortRangesProperty", typing.Dict[str, typing.Any]]]]],
        protocol: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        certificates: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union["RosListener.CertificatesProperty", typing.Dict[str, typing.Any]]]]]] = None,
        client_affinity: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        security_policy_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        x_forwarded_for_config: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Union["RosListener.XForwardedForConfigProperty", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::Listener``.

        :param accelerator_id: Property acceleratorId: The ID of the Global Accelerator instance to which the listener will be added.
        :param port_ranges: Property portRanges:.
        :param protocol: Property protocol: The network transmission protocol of the listener. Valid values: tcp: TCP protocol udp: UDP protocol http: HTTP protocolhttps: HTTPS protocol.
        :param certificates: Property certificates:.
        :param client_affinity: Property clientAffinity: Specifies whether to enable client affinity for the listener. If you do not specify the default value in the parameter, client affinity is disabled. When client affinity is disabled, the connections from a specific source (client) IP address are not always routed to the same endpoint. If you set the value to SOURCE_IP, client affinity is enabled. When client affinity is enabled, the connections from a specific source (client) IP address are always routed to the same endpoint.
        :param description: Property description: The description of the listener.
        :param name: Property name: The name of the listener. The name must be 2 to 128 characters in length and can contain letters, digits, underscores (_), and hyphens (-). It must start with a letter or Chinese character.
        :param proxy_protocol: Property proxyProtocol: Specifies whether to preserve client IP addresses. Valid values: true: preserves client IP addresses. After this feature is enabled, backend servers can retrieve client IP addresses. false (default): does not preserve client IP addresses.
        :param security_policy_id: Property securityPolicyId: The ID of the security policy. Valid values: tls_cipher_policy_1_0 tls_cipher_policy_1_1 tls_cipher_policy_1_2 tls_cipher_policy_1_2_strict tls_cipher_policy_1_2_strict_with_1_3 Note Only HTTPS listeners support this parameter.
        :param x_forwarded_for_config: Property xForwardedForConfig: The configuration of the XForward field.
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                port_ranges: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.PortRangesProperty, typing.Dict[str, typing.Any]]]]],
                protocol: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                certificates: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.CertificatesProperty, typing.Dict[str, typing.Any]]]]]] = None,
                client_affinity: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                security_policy_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                x_forwarded_for_config: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.XForwardedForConfigProperty, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument port_ranges", value=port_ranges, expected_type=type_hints["port_ranges"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument client_affinity", value=client_affinity, expected_type=type_hints["client_affinity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument proxy_protocol", value=proxy_protocol, expected_type=type_hints["proxy_protocol"])
            check_type(argname="argument security_policy_id", value=security_policy_id, expected_type=type_hints["security_policy_id"])
            check_type(argname="argument x_forwarded_for_config", value=x_forwarded_for_config, expected_type=type_hints["x_forwarded_for_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "port_ranges": port_ranges,
            "protocol": protocol,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if proxy_protocol is not None:
            self._values["proxy_protocol"] = proxy_protocol
        if security_policy_id is not None:
            self._values["security_policy_id"] = security_policy_id
        if x_forwarded_for_config is not None:
            self._values["x_forwarded_for_config"] = x_forwarded_for_config

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property acceleratorId: The ID of the Global Accelerator instance to which the listener will be added.'''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def port_ranges(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.PortRangesProperty"]]]:
        '''Property portRanges:.'''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.PortRangesProperty"]]], result)

    @builtins.property
    def protocol(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''Property protocol: The network transmission protocol of the listener.

        Valid values:
        tcp: TCP protocol
        udp: UDP protocol
        http: HTTP protocolhttps: HTTPS protocol.
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.CertificatesProperty"]]]]:
        '''Property certificates:.'''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.CertificatesProperty"]]]], result)

    @builtins.property
    def client_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property clientAffinity: Specifies whether to enable client affinity for the listener.

        If you do not specify the default value in the parameter, client affinity is disabled.
        When client affinity is disabled, the connections from a specific source (client)
        IP address are not always routed to the same endpoint.
        If you set the value to SOURCE_IP, client affinity is enabled. When client affinity is enabled, the connections from
        a specific source (client) IP address are always routed to the same endpoint.
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property description: The description of the listener.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property name: The name of the listener.

        The name must be 2 to 128 characters in length and can contain letters, digits, underscores
        (_), and hyphens (-). It must start with a letter or Chinese character.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def proxy_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''Property proxyProtocol: Specifies whether to preserve client IP addresses.

        Valid values:
        true: preserves client IP addresses. After this feature is enabled, backend servers can retrieve client IP addresses.
        false (default): does not preserve client IP addresses.
        '''
        result = self._values.get("proxy_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def security_policy_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''Property securityPolicyId: The ID of the security policy.

        Valid values:
        tls_cipher_policy_1_0
        tls_cipher_policy_1_1
        tls_cipher_policy_1_2
        tls_cipher_policy_1_2_strict
        tls_cipher_policy_1_2_strict_with_1_3
        Note Only HTTPS listeners support this parameter.
        '''
        result = self._values.get("security_policy_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def x_forwarded_for_config(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, "RosListener.XForwardedForConfigProperty"]]:
        '''Property xForwardedForConfig: The configuration of the XForward field.'''
        result = self._values.get("x_forwarded_for_config")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, "RosListener.XForwardedForConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosAccelerator(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosAccelerator",
):
    '''A ROS template type:  ``ALIYUN::GA::Accelerator``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosAcceleratorProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::Accelerator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosAcceleratorProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAcceleratorId")
    def attr_accelerator_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AcceleratorId: The ID of the GA instance to query.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorId"))

    @builtins.property
    @jsii.member(jsii_name="attrAcceleratorName")
    def attr_accelerator_name(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AcceleratorName: The Name of the GA instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorName"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoPay")
    def attr_auto_pay(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AutoPay: The AutoPay of the GA instance.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoPay"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoUseCoupon")
    def attr_auto_use_coupon(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AutoUseCoupon: The AutoUseCoupon of the GA instance.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoUseCoupon"))

    @builtins.property
    @jsii.member(jsii_name="attrDuration")
    def attr_duration(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Duration: The Duration of the GA instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrDuration"))

    @builtins.property
    @jsii.member(jsii_name="attrOrderId")
    def attr_order_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: OrderId: The OrderId of the GA instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrOrderId"))

    @builtins.property
    @jsii.member(jsii_name="attrPaymentType")
    def attr_payment_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: PaymentType: The Payment Typethe GA instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPaymentType"))

    @builtins.property
    @jsii.member(jsii_name="attrPricingCycle")
    def attr_pricing_cycle(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: PricingCycle: The PricingCycle of the GA instance.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPricingCycle"))

    @builtins.property
    @jsii.member(jsii_name="attrSpec")
    def attr_spec(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Spec: The instance type of the GA instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrSpec"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: duration: The Duration of the GA instance
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "duration"))

    @duration.setter
    def duration(
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
        jsii.set(self, "duration", value)

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
    @jsii.member(jsii_name="pricingCycle")
    def pricing_cycle(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: pricingCycle: The PricingCycle of the GA instance.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "pricingCycle"))

    @pricing_cycle.setter
    def pricing_cycle(
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
        jsii.set(self, "pricingCycle", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: spec: The instance type of the GA instance
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "spec"))

    @spec.setter
    def spec(self, value: typing.Union[builtins.str, ros_cdk_core.IResolvable]) -> None:
        if __debug__:
            def stub(
                value: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spec", value)

    @builtins.property
    @jsii.member(jsii_name="acceleratorName")
    def accelerator_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: acceleratorName: The Name of the GA instance
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "acceleratorName"))

    @accelerator_name.setter
    def accelerator_name(
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
        jsii.set(self, "acceleratorName", value)

    @builtins.property
    @jsii.member(jsii_name="autoPay")
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoPay: The AutoPay of the GA instance.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "autoPay"))

    @auto_pay.setter
    def auto_pay(
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
        jsii.set(self, "autoPay", value)

    @builtins.property
    @jsii.member(jsii_name="autoUseCoupon")
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoUseCoupon: The AutoUseCoupon of the GA instance.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "autoUseCoupon"))

    @auto_use_coupon.setter
    def auto_use_coupon(
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
        jsii.set(self, "autoUseCoupon", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosAcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "pricing_cycle": "pricingCycle",
        "spec": "spec",
        "accelerator_name": "acceleratorName",
        "auto_pay": "autoPay",
        "auto_use_coupon": "autoUseCoupon",
    },
)
class RosAcceleratorProps:
    def __init__(
        self,
        *,
        duration: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        pricing_cycle: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        spec: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        accelerator_name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auto_pay: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::Accelerator``.

        :param duration: 
        :param pricing_cycle: 
        :param spec: 
        :param accelerator_name: 
        :param auto_pay: 
        :param auto_use_coupon: 
        '''
        if __debug__:
            def stub(
                *,
                duration: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                pricing_cycle: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                spec: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                accelerator_name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auto_pay: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument pricing_cycle", value=pricing_cycle, expected_type=type_hints["pricing_cycle"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument accelerator_name", value=accelerator_name, expected_type=type_hints["accelerator_name"])
            check_type(argname="argument auto_pay", value=auto_pay, expected_type=type_hints["auto_pay"])
            check_type(argname="argument auto_use_coupon", value=auto_use_coupon, expected_type=type_hints["auto_use_coupon"])
        self._values: typing.Dict[str, typing.Any] = {
            "duration": duration,
            "pricing_cycle": pricing_cycle,
            "spec": spec,
        }
        if accelerator_name is not None:
            self._values["accelerator_name"] = accelerator_name
        if auto_pay is not None:
            self._values["auto_pay"] = auto_pay
        if auto_use_coupon is not None:
            self._values["auto_use_coupon"] = auto_use_coupon

    @builtins.property
    def duration(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: duration: The Duration of the GA instance
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def pricing_cycle(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: pricingCycle: The PricingCycle of the GA instance.
        '''
        result = self._values.get("pricing_cycle")
        assert result is not None, "Required property 'pricing_cycle' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def spec(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: spec: The instance type of the GA instance
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def accelerator_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: acceleratorName: The Name of the GA instance
        '''
        result = self._values.get("accelerator_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoPay: The AutoPay of the GA instance.
        '''
        result = self._values.get("auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoUseCoupon: The AutoUseCoupon of the GA instance.
        '''
        result = self._values.get("auto_use_coupon")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosAcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosBandwidthPackage(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosBandwidthPackage",
):
    '''A ROS template type:  ``ALIYUN::GA::BandwidthPackage``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosBandwidthPackageProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::BandwidthPackage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosBandwidthPackageProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAutoPay")
    def attr_auto_pay(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AutoPay: The AutoPay of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoPay"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoUseCoupon")
    def attr_auto_use_coupon(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AutoUseCoupon: The AutoUseCoupon  of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAutoUseCoupon"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidth")
    def attr_bandwidth(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Bandwidth: The bandwidth provided by the bandwidth plan.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageId")
    def attr_bandwidth_package_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: BandwidthPackageId: The Resource ID of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageId"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageName")
    def attr_bandwidth_package_name(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: BandwidthPackageName: The Resource name of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageName"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthType")
    def attr_bandwidth_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: BandwidthType: the bandwidth BandwidthType of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthType"))

    @builtins.property
    @jsii.member(jsii_name="attrBillingType")
    def attr_billing_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: BillingType: The BillingType of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBillingType"))

    @builtins.property
    @jsii.member(jsii_name="attrCbnGeographicRegionIdA")
    def attr_cbn_geographic_region_id_a(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: CbnGeographicRegionIdA: The CbnGeographicRegionIdA  of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrCbnGeographicRegionIdA"))

    @builtins.property
    @jsii.member(jsii_name="attrCbnGeographicRegionIdB")
    def attr_cbn_geographic_region_id_b(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: CbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrCbnGeographicRegionIdB"))

    @builtins.property
    @jsii.member(jsii_name="attrChargeType")
    def attr_charge_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ChargeType: The ChargeType of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrChargeType"))

    @builtins.property
    @jsii.member(jsii_name="attrPaymentType")
    def attr_payment_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: PaymentType: The Payment Type of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrPaymentType"))

    @builtins.property
    @jsii.member(jsii_name="attrRatio")
    def attr_ratio(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Ratio: The Ratio of the bandwidth
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrRatio"))

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: Type: The type of the bandwidth plan
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrType"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
        '''
        :Property: bandwidth: The bandwidth provided by the bandwidth plan.
        '''
        return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(
        self,
        value: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value)

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
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: type: The type of the bandwidth plan
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
    @jsii.member(jsii_name="autoPay")
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoPay: Specifies whether to enable automatic payment.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], jsii.get(self, "autoPay"))

    @auto_pay.setter
    def auto_pay(
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
        jsii.set(self, "autoPay", value)

    @builtins.property
    @jsii.member(jsii_name="autoUseCoupon")
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoUseCoupon: The AutoUseCoupon  of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "autoUseCoupon"))

    @auto_use_coupon.setter
    def auto_use_coupon(
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
        jsii.set(self, "autoUseCoupon", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthType")
    def bandwidth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: bandwidthType: the bandwidth BandwidthType of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "bandwidthType"))

    @bandwidth_type.setter
    def bandwidth_type(
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
        jsii.set(self, "bandwidthType", value)

    @builtins.property
    @jsii.member(jsii_name="billingType")
    def billing_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: billingType: The BillingType of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "billingType"))

    @billing_type.setter
    def billing_type(
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
        jsii.set(self, "billingType", value)

    @builtins.property
    @jsii.member(jsii_name="cbnGeographicRegionIdA")
    def cbn_geographic_region_id_a(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: cbnGeographicRegionIdA: The CbnGeographicRegionIdA  of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "cbnGeographicRegionIdA"))

    @cbn_geographic_region_id_a.setter
    def cbn_geographic_region_id_a(
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
        jsii.set(self, "cbnGeographicRegionIdA", value)

    @builtins.property
    @jsii.member(jsii_name="cbnGeographicRegionIdB")
    def cbn_geographic_region_id_b(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: cbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "cbnGeographicRegionIdB"))

    @cbn_geographic_region_id_b.setter
    def cbn_geographic_region_id_b(
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
        jsii.set(self, "cbnGeographicRegionIdB", value)

    @builtins.property
    @jsii.member(jsii_name="chargeType")
    def charge_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: chargeType: The ChargeType of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "chargeType"))

    @charge_type.setter
    def charge_type(
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
        jsii.set(self, "chargeType", value)

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: duration:
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "duration"))

    @duration.setter
    def duration(
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
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="pricingCycle")
    def pricing_cycle(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: pricingCycle:
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "pricingCycle"))

    @pricing_cycle.setter
    def pricing_cycle(
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
        jsii.set(self, "pricingCycle", value)

    @builtins.property
    @jsii.member(jsii_name="ratio")
    def ratio(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: ratio: The Ratio of the bandwidth
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "ratio"))

    @ratio.setter
    def ratio(
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
        jsii.set(self, "ratio", value)


class RosBandwidthPackageAcceleratorAddition(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosBandwidthPackageAcceleratorAddition",
):
    '''A ROS template type:  ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosBandwidthPackageAcceleratorAdditionProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosBandwidthPackageAcceleratorAdditionProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAcceleratorId")
    def attr_accelerator_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AcceleratorId: The ID of the Global Accelerator instance
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAcceleratorId"))

    @builtins.property
    @jsii.member(jsii_name="attrBandwidthPackageId")
    def attr_bandwidth_package_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: BandwidthPackageId: The ID of the bandwidth package which is associated
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrBandwidthPackageId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorId")
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        acceleratorId: The ID of the Global Accelerator instance with which you want to associate the bandwidth
        plan.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "acceleratorId"))

    @accelerator_id.setter
    def accelerator_id(
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
        jsii.set(self, "acceleratorId", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthPackageId")
    def bandwidth_package_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: bandwidthPackageId: The ID of the bandwidth package to associate.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "bandwidthPackageId"))

    @bandwidth_package_id.setter
    def bandwidth_package_id(
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
        jsii.set(self, "bandwidthPackageId", value)

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


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosBandwidthPackageAcceleratorAdditionProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "bandwidth_package_id": "bandwidthPackageId",
    },
)
class RosBandwidthPackageAcceleratorAdditionProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        bandwidth_package_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::BandwidthPackageAcceleratorAddition``.

        :param accelerator_id: 
        :param bandwidth_package_id: 
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                bandwidth_package_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument bandwidth_package_id", value=bandwidth_package_id, expected_type=type_hints["bandwidth_package_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "bandwidth_package_id": bandwidth_package_id,
        }

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        acceleratorId: The ID of the Global Accelerator instance with which you want to associate the bandwidth
        plan.
        '''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def bandwidth_package_id(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: bandwidthPackageId: The ID of the bandwidth package to associate.
        '''
        result = self._values.get("bandwidth_package_id")
        assert result is not None, "Required property 'bandwidth_package_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosBandwidthPackageAcceleratorAdditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosBandwidthPackageProps",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "type": "type",
        "auto_pay": "autoPay",
        "auto_use_coupon": "autoUseCoupon",
        "bandwidth_type": "bandwidthType",
        "billing_type": "billingType",
        "cbn_geographic_region_id_a": "cbnGeographicRegionIdA",
        "cbn_geographic_region_id_b": "cbnGeographicRegionIdB",
        "charge_type": "chargeType",
        "duration": "duration",
        "pricing_cycle": "pricingCycle",
        "ratio": "ratio",
    },
)
class RosBandwidthPackageProps:
    def __init__(
        self,
        *,
        bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
        type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        auto_pay: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        bandwidth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        billing_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        cbn_geographic_region_id_a: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        cbn_geographic_region_id_b: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        charge_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        duration: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        pricing_cycle: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ratio: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::BandwidthPackage``.

        :param bandwidth: 
        :param type: 
        :param auto_pay: 
        :param auto_use_coupon: 
        :param bandwidth_type: 
        :param billing_type: 
        :param cbn_geographic_region_id_a: 
        :param cbn_geographic_region_id_b: 
        :param charge_type: 
        :param duration: 
        :param pricing_cycle: 
        :param ratio: 
        '''
        if __debug__:
            def stub(
                *,
                bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                auto_pay: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                auto_use_coupon: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                bandwidth_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                billing_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                cbn_geographic_region_id_a: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                cbn_geographic_region_id_b: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                charge_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                duration: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                pricing_cycle: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ratio: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument auto_pay", value=auto_pay, expected_type=type_hints["auto_pay"])
            check_type(argname="argument auto_use_coupon", value=auto_use_coupon, expected_type=type_hints["auto_use_coupon"])
            check_type(argname="argument bandwidth_type", value=bandwidth_type, expected_type=type_hints["bandwidth_type"])
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument cbn_geographic_region_id_a", value=cbn_geographic_region_id_a, expected_type=type_hints["cbn_geographic_region_id_a"])
            check_type(argname="argument cbn_geographic_region_id_b", value=cbn_geographic_region_id_b, expected_type=type_hints["cbn_geographic_region_id_b"])
            check_type(argname="argument charge_type", value=charge_type, expected_type=type_hints["charge_type"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument pricing_cycle", value=pricing_cycle, expected_type=type_hints["pricing_cycle"])
            check_type(argname="argument ratio", value=ratio, expected_type=type_hints["ratio"])
        self._values: typing.Dict[str, typing.Any] = {
            "bandwidth": bandwidth,
            "type": type,
        }
        if auto_pay is not None:
            self._values["auto_pay"] = auto_pay
        if auto_use_coupon is not None:
            self._values["auto_use_coupon"] = auto_use_coupon
        if bandwidth_type is not None:
            self._values["bandwidth_type"] = bandwidth_type
        if billing_type is not None:
            self._values["billing_type"] = billing_type
        if cbn_geographic_region_id_a is not None:
            self._values["cbn_geographic_region_id_a"] = cbn_geographic_region_id_a
        if cbn_geographic_region_id_b is not None:
            self._values["cbn_geographic_region_id_b"] = cbn_geographic_region_id_b
        if charge_type is not None:
            self._values["charge_type"] = charge_type
        if duration is not None:
            self._values["duration"] = duration
        if pricing_cycle is not None:
            self._values["pricing_cycle"] = pricing_cycle
        if ratio is not None:
            self._values["ratio"] = ratio

    @builtins.property
    def bandwidth(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
        '''
        :Property: bandwidth: The bandwidth provided by the bandwidth plan.
        '''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

    @builtins.property
    def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: type: The type of the bandwidth plan
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def auto_pay(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoPay: Specifies whether to enable automatic payment.
        '''
        result = self._values.get("auto_pay")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def auto_use_coupon(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: autoUseCoupon: The AutoUseCoupon  of the bandwidth
        '''
        result = self._values.get("auto_use_coupon")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def bandwidth_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: bandwidthType: the bandwidth BandwidthType of the bandwidth
        '''
        result = self._values.get("bandwidth_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def billing_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: billingType: The BillingType of the bandwidth
        '''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def cbn_geographic_region_id_a(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: cbnGeographicRegionIdA: The CbnGeographicRegionIdA  of the bandwidth
        '''
        result = self._values.get("cbn_geographic_region_id_a")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def cbn_geographic_region_id_b(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: cbnGeographicRegionIdB: The CbnGeographicRegionIdB of the bandwidth
        '''
        result = self._values.get("cbn_geographic_region_id_b")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def charge_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: chargeType: The ChargeType of the bandwidth
        '''
        result = self._values.get("charge_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def duration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: duration:
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def pricing_cycle(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: pricingCycle:
        '''
        result = self._values.get("pricing_cycle")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def ratio(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: ratio: The Ratio of the bandwidth
        '''
        result = self._values.get("ratio")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosBandwidthPackageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosEndpointGroup(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosEndpointGroup",
):
    '''A ROS template type:  ``ALIYUN::GA::EndpointGroup``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosEndpointGroupProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::EndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosEndpointGroupProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrEndpointGroupId")
    def attr_endpoint_group_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: EndpointGroupId: The ID of the endpoint group.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrEndpointGroupId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorId")
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the Global Accelerator instance with which the endpoint group will be associated.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "acceleratorId"))

    @accelerator_id.setter
    def accelerator_id(
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
        jsii.set(self, "acceleratorId", value)

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
    @jsii.member(jsii_name="endpointConfigurations")
    def endpoint_configurations(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosEndpointGroup.EndpointConfigurationsProperty"]]]:
        '''
        :Property: endpointConfigurations:
        '''
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosEndpointGroup.EndpointConfigurationsProperty"]]], jsii.get(self, "endpointConfigurations"))

    @endpoint_configurations.setter
    def endpoint_configurations(
        self,
        value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosEndpointGroup.EndpointConfigurationsProperty"]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosEndpointGroup.EndpointConfigurationsProperty]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="endpointGroupRegion")
    def endpoint_group_region(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: endpointGroupRegion: The region ID of the endpoint group.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "endpointGroupRegion"))

    @endpoint_group_region.setter
    def endpoint_group_region(
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
        jsii.set(self, "endpointGroupRegion", value)

    @builtins.property
    @jsii.member(jsii_name="listenerId")
    def listener_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: listenerId: The ID of the listener to be associated with the endpoint group.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "listenerId"))

    @listener_id.setter
    def listener_id(
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
        jsii.set(self, "listenerId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: description: The description of the endpoint group.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "description"))

    @description.setter
    def description(
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
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="endpointGroupType")
    def endpoint_group_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        endpointGroupType: The type of the endpoint group. Valid values:
        default: The endpoint group is a default endpoint group. This is the default value.
        virtual: The endpoint group is a virtual endpoint group.
        Note Only HTTP and HTTPS listeners support virtual endpoint groups.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "endpointGroupType"))

    @endpoint_group_type.setter
    def endpoint_group_type(
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
        jsii.set(self, "endpointGroupType", value)

    @builtins.property
    @jsii.member(jsii_name="endpointRequestProtocol")
    def endpoint_request_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        endpointRequestProtocol: The protocol used by the backend service. Valid values:
        http: This is the default value.
        https
        Note: You can set this parameter only when the listener that is associated with the endpoint group uses HTTP or HTTPS.
        For an HTTP listener, the backend service protocol must be HTTP.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "endpointRequestProtocol"))

    @endpoint_request_protocol.setter
    def endpoint_request_protocol(
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
        jsii.set(self, "endpointRequestProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckEnabled: Specifies whether to enable the health check feature.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], jsii.get(self, "healthCheckEnabled"))

    @health_check_enabled.setter
    def health_check_enabled(
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
        jsii.set(self, "healthCheckEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckIntervalSeconds: The interval between two consecutive health checks. Unit: seconds.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "healthCheckIntervalSeconds"))

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(
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
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckPath: The path set as the destination on the targets for health checks.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(
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
        jsii.set(self, "healthCheckPath", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckPort: The port that is used to connect with the targets for health checks.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "healthCheckPort"))

    @health_check_port.setter
    def health_check_port(
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
        jsii.set(self, "healthCheckPort", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        healthCheckProtocol: The protocol that is used to connect with the targets for health checks.
        tcp: TCP protocol
        http: HTTP protocol
        https: HTTPS protocol
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "healthCheckProtocol"))

    @health_check_protocol.setter
    def health_check_protocol(
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
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: name: The name of the endpoint group.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "name"))

    @name.setter
    def name(
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
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdCount")
    def threshold_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        thresholdCount: The number of consecutive health check failures that must occur before a healthy endpoint is considered unhealthy, or the number of consecutive health check successes that must occur before an unhealthy endpoint is considered healthy.
        Valid values: 2 to 10. Default value: 3.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "thresholdCount"))

    @threshold_count.setter
    def threshold_count(
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
        jsii.set(self, "thresholdCount", value)

    @builtins.property
    @jsii.member(jsii_name="trafficPercentage")
    def traffic_percentage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        trafficPercentage: The weight of the endpoint group when the corresponding listener is associated with
        multiple endpoint groups.
        '''
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], jsii.get(self, "trafficPercentage"))

    @traffic_percentage.setter
    def traffic_percentage(
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
        jsii.set(self, "trafficPercentage", value)

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-ga.RosEndpointGroup.EndpointConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "type": "type",
            "weight": "weight",
            "enable_client_ip_preservation": "enableClientIpPreservation",
            "enable_proxy_protocol": "enableProxyProtocol",
        },
    )
    class EndpointConfigurationsProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            weight: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
            enable_client_ip_preservation: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            enable_proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        ) -> None:
            '''
            :param endpoint: 
            :param type: 
            :param weight: 
            :param enable_client_ip_preservation: 
            :param enable_proxy_protocol: 
            '''
            if __debug__:
                def stub(
                    *,
                    endpoint: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                    type: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                    weight: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                    enable_client_ip_preservation: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                    enable_proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
                check_type(argname="argument enable_client_ip_preservation", value=enable_client_ip_preservation, expected_type=type_hints["enable_client_ip_preservation"])
                check_type(argname="argument enable_proxy_protocol", value=enable_proxy_protocol, expected_type=type_hints["enable_proxy_protocol"])
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint": endpoint,
                "type": type,
                "weight": weight,
            }
            if enable_client_ip_preservation is not None:
                self._values["enable_client_ip_preservation"] = enable_client_ip_preservation
            if enable_proxy_protocol is not None:
                self._values["enable_proxy_protocol"] = enable_proxy_protocol

        @builtins.property
        def endpoint(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: endpoint: The IP address or domain name of endpoint in the endpoint group.
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        @builtins.property
        def type(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property:

            type: The type of endpoint in the endpoint group. Valid values:
            Domain: a custom domain name
            EIP: eip address
            Ip: a custom IP address
            PublicIp: a public IP address provided by Alibaba Cloud
            ECS: an Elastic Compute Service (ECS) instance
            SLB: a Server Load Balancer (SLB) instance
            ALB: an Application Load Balancer (ALB) instance
            OSS: an Object Storage Service (OSS) bucket
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        @builtins.property
        def weight(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
            '''
            :Property: weight: The weight of endpoint N in the endpoint group.
            '''
            result = self._values.get("weight")
            assert result is not None, "Required property 'weight' is missing"
            return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

        @builtins.property
        def enable_client_ip_preservation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            enableClientIpPreservation: Specifies whether to obtain and preserve the IP addresses of clients that access the endpoint by using the TCP Option Address (TOA) module. Valid values:
            true: yes
            false (default): no
            '''
            result = self._values.get("enable_client_ip_preservation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        @builtins.property
        def enable_proxy_protocol(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            enableProxyProtocol: Specifies whether to obtain and preserve the IP addresses of clients that access the endpoint by using the TCP Option Address (TOA) module. Valid values:
            true: yes
            false (default): no
            '''
            result = self._values.get("enable_proxy_protocol")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosEndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "endpoint_configurations": "endpointConfigurations",
        "endpoint_group_region": "endpointGroupRegion",
        "listener_id": "listenerId",
        "description": "description",
        "endpoint_group_type": "endpointGroupType",
        "endpoint_request_protocol": "endpointRequestProtocol",
        "health_check_enabled": "healthCheckEnabled",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "name": "name",
        "threshold_count": "thresholdCount",
        "traffic_percentage": "trafficPercentage",
    },
)
class RosEndpointGroupProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        endpoint_configurations: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosEndpointGroup.EndpointConfigurationsProperty, typing.Dict[str, typing.Any]]]]],
        endpoint_group_region: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        listener_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        endpoint_group_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        endpoint_request_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        health_check_interval_seconds: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        health_check_path: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        health_check_port: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        health_check_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        threshold_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
        traffic_percentage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::EndpointGroup``.

        :param accelerator_id: 
        :param endpoint_configurations: 
        :param endpoint_group_region: 
        :param listener_id: 
        :param description: 
        :param endpoint_group_type: 
        :param endpoint_request_protocol: 
        :param health_check_enabled: 
        :param health_check_interval_seconds: 
        :param health_check_path: 
        :param health_check_port: 
        :param health_check_protocol: 
        :param name: 
        :param threshold_count: 
        :param traffic_percentage: 
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                endpoint_configurations: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosEndpointGroup.EndpointConfigurationsProperty, typing.Dict[str, typing.Any]]]]],
                endpoint_group_region: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                listener_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                endpoint_group_type: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                endpoint_request_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                health_check_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                health_check_interval_seconds: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                health_check_path: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                health_check_port: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                health_check_protocol: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                threshold_count: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
                traffic_percentage: typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument endpoint_configurations", value=endpoint_configurations, expected_type=type_hints["endpoint_configurations"])
            check_type(argname="argument endpoint_group_region", value=endpoint_group_region, expected_type=type_hints["endpoint_group_region"])
            check_type(argname="argument listener_id", value=listener_id, expected_type=type_hints["listener_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint_group_type", value=endpoint_group_type, expected_type=type_hints["endpoint_group_type"])
            check_type(argname="argument endpoint_request_protocol", value=endpoint_request_protocol, expected_type=type_hints["endpoint_request_protocol"])
            check_type(argname="argument health_check_enabled", value=health_check_enabled, expected_type=type_hints["health_check_enabled"])
            check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument threshold_count", value=threshold_count, expected_type=type_hints["threshold_count"])
            check_type(argname="argument traffic_percentage", value=traffic_percentage, expected_type=type_hints["traffic_percentage"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "endpoint_configurations": endpoint_configurations,
            "endpoint_group_region": endpoint_group_region,
            "listener_id": listener_id,
        }
        if description is not None:
            self._values["description"] = description
        if endpoint_group_type is not None:
            self._values["endpoint_group_type"] = endpoint_group_type
        if endpoint_request_protocol is not None:
            self._values["endpoint_request_protocol"] = endpoint_request_protocol
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if name is not None:
            self._values["name"] = name
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if traffic_percentage is not None:
            self._values["traffic_percentage"] = traffic_percentage

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the Global Accelerator instance with which the endpoint group will be associated.
        '''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def endpoint_configurations(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosEndpointGroup.EndpointConfigurationsProperty]]]:
        '''
        :Property: endpointConfigurations:
        '''
        result = self._values.get("endpoint_configurations")
        assert result is not None, "Required property 'endpoint_configurations' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosEndpointGroup.EndpointConfigurationsProperty]]], result)

    @builtins.property
    def endpoint_group_region(
        self,
    ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: endpointGroupRegion: The region ID of the endpoint group.
        '''
        result = self._values.get("endpoint_group_region")
        assert result is not None, "Required property 'endpoint_group_region' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def listener_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: listenerId: The ID of the listener to be associated with the endpoint group.
        '''
        result = self._values.get("listener_id")
        assert result is not None, "Required property 'listener_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: description: The description of the endpoint group.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def endpoint_group_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        endpointGroupType: The type of the endpoint group. Valid values:
        default: The endpoint group is a default endpoint group. This is the default value.
        virtual: The endpoint group is a virtual endpoint group.
        Note Only HTTP and HTTPS listeners support virtual endpoint groups.
        '''
        result = self._values.get("endpoint_group_type")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def endpoint_request_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        endpointRequestProtocol: The protocol used by the backend service. Valid values:
        http: This is the default value.
        https
        Note: You can set this parameter only when the listener that is associated with the endpoint group uses HTTP or HTTPS.
        For an HTTP listener, the backend service protocol must be HTTP.
        '''
        result = self._values.get("endpoint_request_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckEnabled: Specifies whether to enable the health check feature.
        '''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_interval_seconds(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckIntervalSeconds: The interval between two consecutive health checks. Unit: seconds.
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckPath: The path set as the destination on the targets for health checks.
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_port(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property: healthCheckPort: The port that is used to connect with the targets for health checks.
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def health_check_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        healthCheckProtocol: The protocol that is used to connect with the targets for health checks.
        tcp: TCP protocol
        http: HTTP protocol
        https: HTTPS protocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: name: The name of the endpoint group.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def threshold_count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        thresholdCount: The number of consecutive health check failures that must occur before a healthy endpoint is considered unhealthy, or the number of consecutive health check successes that must occur before an unhealthy endpoint is considered healthy.
        Valid values: 2 to 10. Default value: 3.
        '''
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def traffic_percentage(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        trafficPercentage: The weight of the endpoint group when the corresponding listener is associated with
        multiple endpoint groups.
        '''
        result = self._values.get("traffic_percentage")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, ros_cdk_core.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosEndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosIpSets(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosIpSets",
):
    '''A ROS template type:  ``ALIYUN::GA::IpSets``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosIpSetsProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::IpSets``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosIpSetsProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrAccelerateRegionIds")
    def attr_accelerate_region_ids(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: AccelerateRegionIds: The ID list of the accelerate region.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrAccelerateRegionIds"))

    @builtins.property
    @jsii.member(jsii_name="attrIpSetIds")
    def attr_ip_set_ids(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: IpSetIds: The ID list of the ip set.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrIpSetIds"))

    @builtins.property
    @jsii.member(jsii_name="attrIpVersions")
    def attr_ip_versions(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: IpVersions: The IP version list of the accelerate region.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrIpVersions"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="accelerateRegion")
    def accelerate_region(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosIpSets.AccelerateRegionProperty"]]]:
        '''
        :Property: accelerateRegion:
        '''
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosIpSets.AccelerateRegionProperty"]]], jsii.get(self, "accelerateRegion"))

    @accelerate_region.setter
    def accelerate_region(
        self,
        value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosIpSets.AccelerateRegionProperty"]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosIpSets.AccelerateRegionProperty]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accelerateRegion", value)

    @builtins.property
    @jsii.member(jsii_name="acceleratorId")
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the GA instance.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "acceleratorId"))

    @accelerator_id.setter
    def accelerator_id(
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
        jsii.set(self, "acceleratorId", value)

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

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-ga.RosIpSets.AccelerateRegionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accelerate_region_id": "accelerateRegionId",
            "bandwidth": "bandwidth",
            "ip_version": "ipVersion",
        },
    )
    class AccelerateRegionProperty:
        def __init__(
            self,
            *,
            accelerate_region_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
            ip_version: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        ) -> None:
            '''
            :param accelerate_region_id: 
            :param bandwidth: 
            :param ip_version: 
            '''
            if __debug__:
                def stub(
                    *,
                    accelerate_region_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                    bandwidth: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                    ip_version: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument accelerate_region_id", value=accelerate_region_id, expected_type=type_hints["accelerate_region_id"])
                check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
                check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            self._values: typing.Dict[str, typing.Any] = {
                "accelerate_region_id": accelerate_region_id,
                "bandwidth": bandwidth,
            }
            if ip_version is not None:
                self._values["ip_version"] = ip_version

        @builtins.property
        def accelerate_region_id(
            self,
        ) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: accelerateRegionId: The ID of the region where traffic is to be accelerated.
            '''
            result = self._values.get("accelerate_region_id")
            assert result is not None, "Required property 'accelerate_region_id' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        @builtins.property
        def bandwidth(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
            '''
            :Property:

            bandwidth: The bandwidth allocated to the acceleration region. Unit: Mbit/s.
            Note
            The minimum bandwidth allocated to each accelerated region is 2 Mbit/s.
            The total bandwidth for all regions must not exceed the amount included in your basic
            bandwidth plan.
            '''
            result = self._values.get("bandwidth")
            assert result is not None, "Required property 'bandwidth' is missing"
            return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

        @builtins.property
        def ip_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
            '''
            :Property: ipVersion: IP version. Valid values: IPv4, IPv6
            '''
            result = self._values.get("ip_version")
            return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccelerateRegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosIpSetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerate_region": "accelerateRegion",
        "accelerator_id": "acceleratorId",
    },
)
class RosIpSetsProps:
    def __init__(
        self,
        *,
        accelerate_region: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosIpSets.AccelerateRegionProperty, typing.Dict[str, typing.Any]]]]],
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::IpSets``.

        :param accelerate_region: 
        :param accelerator_id: 
        '''
        if __debug__:
            def stub(
                *,
                accelerate_region: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosIpSets.AccelerateRegionProperty, typing.Dict[str, typing.Any]]]]],
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerate_region", value=accelerate_region, expected_type=type_hints["accelerate_region"])
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerate_region": accelerate_region,
            "accelerator_id": accelerator_id,
        }

    @builtins.property
    def accelerate_region(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosIpSets.AccelerateRegionProperty]]]:
        '''
        :Property: accelerateRegion:
        '''
        result = self._values.get("accelerate_region")
        assert result is not None, "Required property 'accelerate_region' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosIpSets.AccelerateRegionProperty]]], result)

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the GA instance.
        '''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosIpSetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosListener(
    ros_cdk_core.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-ga.RosListener",
):
    '''A ROS template type:  ``ALIYUN::GA::Listener``.'''

    def __init__(
        self,
        scope: ros_cdk_core.Construct,
        id: builtins.str,
        props: typing.Union["RosListenerProps", typing.Dict[str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''Create a new ``ALIYUN::GA::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            def stub(
                scope: ros_cdk_core.Construct,
                id: builtins.str,
                props: typing.Union[RosListenerProps, typing.Dict[str, typing.Any]],
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
    @jsii.member(jsii_name="attrListenerId")
    def attr_listener_id(self) -> ros_cdk_core.IResolvable:
        '''
        :Attribute: ListenerId: The ID of the listener.
        '''
        return typing.cast(ros_cdk_core.IResolvable, jsii.get(self, "attrListenerId"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorId")
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the Global Accelerator instance to which the listener will be added.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "acceleratorId"))

    @accelerator_id.setter
    def accelerator_id(
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
        jsii.set(self, "acceleratorId", value)

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
    @jsii.member(jsii_name="portRanges")
    def port_ranges(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.PortRangesProperty"]]]:
        '''
        :Property: portRanges:
        '''
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.PortRangesProperty"]]], jsii.get(self, "portRanges"))

    @port_ranges.setter
    def port_ranges(
        self,
        value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.PortRangesProperty"]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.PortRangesProperty]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRanges", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        protocol: The network transmission protocol of the listener. Valid values:
        tcp: TCP protocol
        udp: UDP protocol
        http: HTTP protocolhttps: HTTPS protocol.
        '''
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(
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
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.CertificatesProperty"]]]]:
        '''
        :Property: certificates:
        '''
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.CertificatesProperty"]]]], jsii.get(self, "certificates"))

    @certificates.setter
    def certificates(
        self,
        value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, "RosListener.CertificatesProperty"]]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.CertificatesProperty]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificates", value)

    @builtins.property
    @jsii.member(jsii_name="clientAffinity")
    def client_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        clientAffinity: Specifies whether to enable client affinity for the listener.
        If you do not specify the default value in the parameter, client affinity is disabled.
        When client affinity is disabled, the connections from a specific source (client)
        IP address are not always routed to the same endpoint.
        If you set the value to SOURCE_IP, client affinity is enabled. When client affinity is enabled, the connections from
        a specific source (client) IP address are always routed to the same endpoint.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "clientAffinity"))

    @client_affinity.setter
    def client_affinity(
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
        jsii.set(self, "clientAffinity", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: description: The description of the listener.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "description"))

    @description.setter
    def description(
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
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        name: The name of the listener.
        The name must be 2 to 128 characters in length and can contain letters, digits, underscores
        (_), and hyphens (-). It must start with a letter or Chinese character.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "name"))

    @name.setter
    def name(
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
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="proxyProtocol")
    def proxy_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        proxyProtocol: Specifies whether to preserve client IP addresses. Valid values:
        true: preserves client IP addresses. After this feature is enabled, backend servers can retrieve client IP addresses.
        false (default): does not preserve client IP addresses.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], jsii.get(self, "proxyProtocol"))

    @proxy_protocol.setter
    def proxy_protocol(
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
        jsii.set(self, "proxyProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="securityPolicyId")
    def security_policy_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        securityPolicyId: The ID of the security policy. Valid values:
        tls_cipher_policy_1_0
        tls_cipher_policy_1_1
        tls_cipher_policy_1_2
        tls_cipher_policy_1_2_strict
        tls_cipher_policy_1_2_strict_with_1_3
        Note Only HTTPS listeners support this parameter.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], jsii.get(self, "securityPolicyId"))

    @security_policy_id.setter
    def security_policy_id(
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
        jsii.set(self, "securityPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="xForwardedForConfig")
    def x_forwarded_for_config(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, "RosListener.XForwardedForConfigProperty"]]:
        '''
        :Property: xForwardedForConfig: The configuration of the XForward field.
        '''
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, "RosListener.XForwardedForConfigProperty"]], jsii.get(self, "xForwardedForConfig"))

    @x_forwarded_for_config.setter
    def x_forwarded_for_config(
        self,
        value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, "RosListener.XForwardedForConfigProperty"]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[ros_cdk_core.IResolvable, RosListener.XForwardedForConfigProperty]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedForConfig", value)

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-ga.RosListener.CertificatesProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class CertificatesProperty:
        def __init__(
            self,
            *,
            id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        ) -> None:
            '''
            :param id: 
            '''
            if __debug__:
                def stub(
                    *,
                    id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
            '''
            :Property: id: The ID of the SSL certificate.
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-ga.RosListener.PortRangesProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangesProperty:
        def __init__(
            self,
            *,
            from_port: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
            to_port: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
        ) -> None:
            '''
            :param from_port: 
            :param to_port: 
            '''
            if __debug__:
                def stub(
                    *,
                    from_port: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                    to_port: typing.Union[jsii.Number, ros_cdk_core.IResolvable],
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[str, typing.Any] = {
                "from_port": from_port,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
            '''
            :Property:

            fromPort: The first listening port of the port range specified for receiving and forwarding
            requests to endpoints.
            '''
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

        @builtins.property
        def to_port(self) -> typing.Union[jsii.Number, ros_cdk_core.IResolvable]:
            '''
            :Property:

            toPort: The last listening port of the port range specified for receiving and forwarding requests
            to endpoints.
            '''
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return typing.cast(typing.Union[jsii.Number, ros_cdk_core.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@alicloud/ros-cdk-ga.RosListener.XForwardedForConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "x_forwarded_for_ga_ap_enabled": "xForwardedForGaApEnabled",
            "x_forwarded_for_ga_id_enabled": "xForwardedForGaIdEnabled",
            "x_forwarded_for_port_enabled": "xForwardedForPortEnabled",
            "x_forwarded_for_proto_enabled": "xForwardedForProtoEnabled",
            "x_real_ip_enabled": "xRealIpEnabled",
        },
    )
    class XForwardedForConfigProperty:
        def __init__(
            self,
            *,
            x_forwarded_for_ga_ap_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            x_forwarded_for_ga_id_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            x_forwarded_for_port_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            x_forwarded_for_proto_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
            x_real_ip_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        ) -> None:
            '''
            :param x_forwarded_for_ga_ap_enabled: 
            :param x_forwarded_for_ga_id_enabled: 
            :param x_forwarded_for_port_enabled: 
            :param x_forwarded_for_proto_enabled: 
            :param x_real_ip_enabled: 
            '''
            if __debug__:
                def stub(
                    *,
                    x_forwarded_for_ga_ap_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                    x_forwarded_for_ga_id_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                    x_forwarded_for_port_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                    x_forwarded_for_proto_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                    x_real_ip_enabled: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                ) -> None:
                    ...
                type_hints = typing.get_type_hints(stub)
                check_type(argname="argument x_forwarded_for_ga_ap_enabled", value=x_forwarded_for_ga_ap_enabled, expected_type=type_hints["x_forwarded_for_ga_ap_enabled"])
                check_type(argname="argument x_forwarded_for_ga_id_enabled", value=x_forwarded_for_ga_id_enabled, expected_type=type_hints["x_forwarded_for_ga_id_enabled"])
                check_type(argname="argument x_forwarded_for_port_enabled", value=x_forwarded_for_port_enabled, expected_type=type_hints["x_forwarded_for_port_enabled"])
                check_type(argname="argument x_forwarded_for_proto_enabled", value=x_forwarded_for_proto_enabled, expected_type=type_hints["x_forwarded_for_proto_enabled"])
                check_type(argname="argument x_real_ip_enabled", value=x_real_ip_enabled, expected_type=type_hints["x_real_ip_enabled"])
            self._values: typing.Dict[str, typing.Any] = {}
            if x_forwarded_for_ga_ap_enabled is not None:
                self._values["x_forwarded_for_ga_ap_enabled"] = x_forwarded_for_ga_ap_enabled
            if x_forwarded_for_ga_id_enabled is not None:
                self._values["x_forwarded_for_ga_id_enabled"] = x_forwarded_for_ga_id_enabled
            if x_forwarded_for_port_enabled is not None:
                self._values["x_forwarded_for_port_enabled"] = x_forwarded_for_port_enabled
            if x_forwarded_for_proto_enabled is not None:
                self._values["x_forwarded_for_proto_enabled"] = x_forwarded_for_proto_enabled
            if x_real_ip_enabled is not None:
                self._values["x_real_ip_enabled"] = x_real_ip_enabled

        @builtins.property
        def x_forwarded_for_ga_ap_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            xForwardedForGaApEnabled: Specifies whether to use the GA-AP header to retrieve the information about the acceleration area. Valid values:
            true: yes
            false (default): no
            Note Only HTTP and HTTPS listeners support this parameter.
            '''
            result = self._values.get("x_forwarded_for_ga_ap_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        @builtins.property
        def x_forwarded_for_ga_id_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            xForwardedForGaIdEnabled: Specifies whether to use the GA-ID header to retrieve the ID of the GA instance. Valid values:
            true: yes
            false (default): no
            Note Only HTTP and HTTPS listeners support this parameter.
            '''
            result = self._values.get("x_forwarded_for_ga_id_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        @builtins.property
        def x_forwarded_for_port_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            xForwardedForPortEnabled: Specifies whether to use the GA-X-Forward-Port header to retrieve the listener ports of the GA instance. Valid values:
            true: yes
            false (default): no
            Note Only HTTP and HTTPS listeners support this parameter.
            '''
            result = self._values.get("x_forwarded_for_port_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        @builtins.property
        def x_forwarded_for_proto_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            xForwardedForProtoEnabled: Specifies whether to use the GA-X-Forward-Proto header to retrieve the listener protocol of the GA instance. Valid values:
            true: yes
            false (default): no
            Note Only HTTP and HTTPS listeners support this parameter.
            '''
            result = self._values.get("x_forwarded_for_proto_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        @builtins.property
        def x_real_ip_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
            '''
            :Property:

            xRealIpEnabled: Specifies whether to use the X-Real-IP header to retrieve client IP addresses. Valid values:
            true: yes
            false (default): no
            Note Only HTTP and HTTPS listeners support this parameter.
            '''
            result = self._values.get("x_real_ip_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XForwardedForConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-ga.RosListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_id": "acceleratorId",
        "port_ranges": "portRanges",
        "protocol": "protocol",
        "certificates": "certificates",
        "client_affinity": "clientAffinity",
        "description": "description",
        "name": "name",
        "proxy_protocol": "proxyProtocol",
        "security_policy_id": "securityPolicyId",
        "x_forwarded_for_config": "xForwardedForConfig",
    },
)
class RosListenerProps:
    def __init__(
        self,
        *,
        accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        port_ranges: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.PortRangesProperty, typing.Dict[str, typing.Any]]]]],
        protocol: typing.Union[builtins.str, ros_cdk_core.IResolvable],
        certificates: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.CertificatesProperty, typing.Dict[str, typing.Any]]]]]] = None,
        client_affinity: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
        security_policy_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
        x_forwarded_for_config: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.XForwardedForConfigProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``ALIYUN::GA::Listener``.

        :param accelerator_id: 
        :param port_ranges: 
        :param protocol: 
        :param certificates: 
        :param client_affinity: 
        :param description: 
        :param name: 
        :param proxy_protocol: 
        :param security_policy_id: 
        :param x_forwarded_for_config: 
        '''
        if __debug__:
            def stub(
                *,
                accelerator_id: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                port_ranges: typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.PortRangesProperty, typing.Dict[str, typing.Any]]]]],
                protocol: typing.Union[builtins.str, ros_cdk_core.IResolvable],
                certificates: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Sequence[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.CertificatesProperty, typing.Dict[str, typing.Any]]]]]] = None,
                client_affinity: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                description: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                name: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                proxy_protocol: typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]] = None,
                security_policy_id: typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]] = None,
                x_forwarded_for_config: typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.Union[RosListener.XForwardedForConfigProperty, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument accelerator_id", value=accelerator_id, expected_type=type_hints["accelerator_id"])
            check_type(argname="argument port_ranges", value=port_ranges, expected_type=type_hints["port_ranges"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument client_affinity", value=client_affinity, expected_type=type_hints["client_affinity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument proxy_protocol", value=proxy_protocol, expected_type=type_hints["proxy_protocol"])
            check_type(argname="argument security_policy_id", value=security_policy_id, expected_type=type_hints["security_policy_id"])
            check_type(argname="argument x_forwarded_for_config", value=x_forwarded_for_config, expected_type=type_hints["x_forwarded_for_config"])
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_id": accelerator_id,
            "port_ranges": port_ranges,
            "protocol": protocol,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if proxy_protocol is not None:
            self._values["proxy_protocol"] = proxy_protocol
        if security_policy_id is not None:
            self._values["security_policy_id"] = security_policy_id
        if x_forwarded_for_config is not None:
            self._values["x_forwarded_for_config"] = x_forwarded_for_config

    @builtins.property
    def accelerator_id(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property: acceleratorId: The ID of the Global Accelerator instance to which the listener will be added.
        '''
        result = self._values.get("accelerator_id")
        assert result is not None, "Required property 'accelerator_id' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def port_ranges(
        self,
    ) -> typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.PortRangesProperty]]]:
        '''
        :Property: portRanges:
        '''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.PortRangesProperty]]], result)

    @builtins.property
    def protocol(self) -> typing.Union[builtins.str, ros_cdk_core.IResolvable]:
        '''
        :Property:

        protocol: The network transmission protocol of the listener. Valid values:
        tcp: TCP protocol
        udp: UDP protocol
        http: HTTP protocolhttps: HTTPS protocol.
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.Union[builtins.str, ros_cdk_core.IResolvable], result)

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.CertificatesProperty]]]]:
        '''
        :Property: certificates:
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, typing.List[typing.Union[ros_cdk_core.IResolvable, RosListener.CertificatesProperty]]]], result)

    @builtins.property
    def client_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        clientAffinity: Specifies whether to enable client affinity for the listener.
        If you do not specify the default value in the parameter, client affinity is disabled.
        When client affinity is disabled, the connections from a specific source (client)
        IP address are not always routed to the same endpoint.
        If you set the value to SOURCE_IP, client affinity is enabled. When client affinity is enabled, the connections from
        a specific source (client) IP address are always routed to the same endpoint.
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property: description: The description of the listener.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        name: The name of the listener.
        The name must be 2 to 128 characters in length and can contain letters, digits, underscores
        (_), and hyphens (-). It must start with a letter or Chinese character.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def proxy_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        proxyProtocol: Specifies whether to preserve client IP addresses. Valid values:
        true: preserves client IP addresses. After this feature is enabled, backend servers can retrieve client IP addresses.
        false (default): does not preserve client IP addresses.
        '''
        result = self._values.get("proxy_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def security_policy_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]]:
        '''
        :Property:

        securityPolicyId: The ID of the security policy. Valid values:
        tls_cipher_policy_1_0
        tls_cipher_policy_1_1
        tls_cipher_policy_1_2
        tls_cipher_policy_1_2_strict
        tls_cipher_policy_1_2_strict_with_1_3
        Note Only HTTPS listeners support this parameter.
        '''
        result = self._values.get("security_policy_id")
        return typing.cast(typing.Optional[typing.Union[builtins.str, ros_cdk_core.IResolvable]], result)

    @builtins.property
    def x_forwarded_for_config(
        self,
    ) -> typing.Optional[typing.Union[ros_cdk_core.IResolvable, RosListener.XForwardedForConfigProperty]]:
        '''
        :Property: xForwardedForConfig: The configuration of the XForward field.
        '''
        result = self._values.get("x_forwarded_for_config")
        return typing.cast(typing.Optional[typing.Union[ros_cdk_core.IResolvable, RosListener.XForwardedForConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Accelerator",
    "AcceleratorProps",
    "BandwidthPackage",
    "BandwidthPackageAcceleratorAddition",
    "BandwidthPackageAcceleratorAdditionProps",
    "BandwidthPackageProps",
    "EndpointGroup",
    "EndpointGroupProps",
    "IpSets",
    "IpSetsProps",
    "Listener",
    "ListenerProps",
    "RosAccelerator",
    "RosAcceleratorProps",
    "RosBandwidthPackage",
    "RosBandwidthPackageAcceleratorAddition",
    "RosBandwidthPackageAcceleratorAdditionProps",
    "RosBandwidthPackageProps",
    "RosEndpointGroup",
    "RosEndpointGroupProps",
    "RosIpSets",
    "RosIpSetsProps",
    "RosListener",
    "RosListenerProps",
]

publication.publish()
