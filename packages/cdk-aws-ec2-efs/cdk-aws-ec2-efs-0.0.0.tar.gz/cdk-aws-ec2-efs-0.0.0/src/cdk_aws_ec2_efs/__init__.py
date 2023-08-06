'''
# EC2 with EFS AWS CDK construct

This construct helps you to mount an EFS on EC2.
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

import aws_cdk.aws_ec2
import aws_cdk.aws_efs
import constructs


class Ec2WithEfs(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-ec2-efs.Ec2WithEfs",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        file_system: aws_cdk.aws_efs.FileSystem,
        instance: aws_cdk.aws_ec2.Instance,
        configure_connection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param file_system: The file system to mount *.
        :param instance: The instance to mount file system it must have yum. Amazo Linux 2 is recommended. *
        :param configure_connection: To configure the efs to allow connection to default port from ec2. Defaults too false. If you set it to true then it's not needed to allow connections manually. *
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                file_system: aws_cdk.aws_efs.FileSystem,
                instance: aws_cdk.aws_ec2.Instance,
                configure_connection: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2WithEfsProps(
            file_system=file_system,
            instance=instance,
            configure_connection=configure_connection,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-aws-ec2-efs.Ec2WithEfsProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system": "fileSystem",
        "instance": "instance",
        "configure_connection": "configureConnection",
    },
)
class Ec2WithEfsProps:
    def __init__(
        self,
        *,
        file_system: aws_cdk.aws_efs.FileSystem,
        instance: aws_cdk.aws_ec2.Instance,
        configure_connection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param file_system: The file system to mount *.
        :param instance: The instance to mount file system it must have yum. Amazo Linux 2 is recommended. *
        :param configure_connection: To configure the efs to allow connection to default port from ec2. Defaults too false. If you set it to true then it's not needed to allow connections manually. *
        '''
        if __debug__:
            def stub(
                *,
                file_system: aws_cdk.aws_efs.FileSystem,
                instance: aws_cdk.aws_ec2.Instance,
                configure_connection: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument configure_connection", value=configure_connection, expected_type=type_hints["configure_connection"])
        self._values: typing.Dict[str, typing.Any] = {
            "file_system": file_system,
            "instance": instance,
        }
        if configure_connection is not None:
            self._values["configure_connection"] = configure_connection

    @builtins.property
    def file_system(self) -> aws_cdk.aws_efs.FileSystem:
        '''The file system to mount *.'''
        result = self._values.get("file_system")
        assert result is not None, "Required property 'file_system' is missing"
        return typing.cast(aws_cdk.aws_efs.FileSystem, result)

    @builtins.property
    def instance(self) -> aws_cdk.aws_ec2.Instance:
        '''The instance to mount file system it must have yum.

        Amazo Linux 2 is recommended.
        *
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(aws_cdk.aws_ec2.Instance, result)

    @builtins.property
    def configure_connection(self) -> typing.Optional[builtins.bool]:
        '''To configure the efs to allow connection to default port from ec2.

        Defaults too false.
        If you set it to true then it's not needed to allow connections manually.
        *
        '''
        result = self._values.get("configure_connection")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2WithEfsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2WithEfs",
    "Ec2WithEfsProps",
]

publication.publish()
