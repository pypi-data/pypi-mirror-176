'''
# replace this
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

import aws_cdk.aws_dynamodb
import constructs


class DDBGoated(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="farazgoated.DDBGoated",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        billing_mode: aws_cdk.aws_dynamodb.BillingMode,
        partition_key: typing.Mapping[typing.Any, typing.Any],
        table_class: aws_cdk.aws_dynamodb.TableClass,
        read_capacity: typing.Optional[jsii.Number] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param billing_mode: 
        :param partition_key: 
        :param table_class: 
        :param read_capacity: 
        :param write_capacity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DDBGoated.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DDBGoatedProps(
            billing_mode=billing_mode,
            partition_key=partition_key,
            table_class=table_class,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_dynamodb.Table:
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "table"))

    @table.setter
    def table(self, value: aws_cdk.aws_dynamodb.Table) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(DDBGoated, "table").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)


@jsii.data_type(
    jsii_type="farazgoated.DDBGoatedProps",
    jsii_struct_bases=[],
    name_mapping={
        "billing_mode": "billingMode",
        "partition_key": "partitionKey",
        "table_class": "tableClass",
        "read_capacity": "readCapacity",
        "write_capacity": "writeCapacity",
    },
)
class DDBGoatedProps:
    def __init__(
        self,
        *,
        billing_mode: aws_cdk.aws_dynamodb.BillingMode,
        partition_key: typing.Mapping[typing.Any, typing.Any],
        table_class: aws_cdk.aws_dynamodb.TableClass,
        read_capacity: typing.Optional[jsii.Number] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param billing_mode: 
        :param partition_key: 
        :param table_class: 
        :param read_capacity: 
        :param write_capacity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DDBGoatedProps.__init__)
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument table_class", value=table_class, expected_type=type_hints["table_class"])
            check_type(argname="argument read_capacity", value=read_capacity, expected_type=type_hints["read_capacity"])
            check_type(argname="argument write_capacity", value=write_capacity, expected_type=type_hints["write_capacity"])
        self._values: typing.Dict[str, typing.Any] = {
            "billing_mode": billing_mode,
            "partition_key": partition_key,
            "table_class": table_class,
        }
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity

    @builtins.property
    def billing_mode(self) -> aws_cdk.aws_dynamodb.BillingMode:
        result = self._values.get("billing_mode")
        assert result is not None, "Required property 'billing_mode' is missing"
        return typing.cast(aws_cdk.aws_dynamodb.BillingMode, result)

    @builtins.property
    def partition_key(self) -> typing.Mapping[typing.Any, typing.Any]:
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(typing.Mapping[typing.Any, typing.Any], result)

    @builtins.property
    def table_class(self) -> aws_cdk.aws_dynamodb.TableClass:
        result = self._values.get("table_class")
        assert result is not None, "Required property 'table_class' is missing"
        return typing.cast(aws_cdk.aws_dynamodb.TableClass, result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DDBGoatedProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DDBGoated",
    "DDBGoatedProps",
]

publication.publish()
