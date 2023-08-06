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

import cdktf_cdktf_provider_aws.data_aws_iam_policy_document
import cdktf_cdktf_provider_aws.s3_bucket
import constructs


class Bucket(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="workshop-code.Bucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        block_all_public_access: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        sse_enabled: typing.Optional[builtins.bool] = None,
        versioning_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param block_all_public_access: The path for the role. Default: true
        :param name: The name to identify the bucket. Will be appended to the prefix 'secure-bucket-'.
        :param sse_enabled: The path for the role. Default: false
        :param versioning_enabled: Whether to enable versioning or not on the bucket. Default: false
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                block_all_public_access: typing.Optional[builtins.bool] = None,
                name: typing.Optional[builtins.str] = None,
                sse_enabled: typing.Optional[builtins.bool] = None,
                versioning_enabled: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BucketConfig(
            block_all_public_access=block_all_public_access,
            name=name,
            sse_enabled=sse_enabled,
            versioning_enabled=versioning_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="attachBucketPolicy")
    def attach_bucket_policy(
        self,
        policy: cdktf_cdktf_provider_aws.data_aws_iam_policy_document.DataAwsIamPolicyDocument,
    ) -> None:
        '''
        :param policy: -
        '''
        if __debug__:
            def stub(
                policy: cdktf_cdktf_provider_aws.data_aws_iam_policy_document.DataAwsIamPolicyDocument,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachBucketPolicy", [policy]))

    @jsii.member(jsii_name="blockAllPublicAccess")
    def block_all_public_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "blockAllPublicAccess", []))

    @jsii.member(jsii_name="enableSSE")
    def enable_sse(self, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: -
        '''
        if __debug__:
            def stub(kms_key_id: typing.Optional[builtins.str] = None) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        return typing.cast(None, jsii.invoke(self, "enableSSE", [kms_key_id]))

    @jsii.member(jsii_name="enableVersioning")
    def enable_versioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "enableVersioning", []))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> cdktf_cdktf_provider_aws.s3_bucket.S3Bucket:
        return typing.cast(cdktf_cdktf_provider_aws.s3_bucket.S3Bucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))


@jsii.data_type(
    jsii_type="workshop-code.BucketConfig",
    jsii_struct_bases=[],
    name_mapping={
        "block_all_public_access": "blockAllPublicAccess",
        "name": "name",
        "sse_enabled": "sseEnabled",
        "versioning_enabled": "versioningEnabled",
    },
)
class BucketConfig:
    def __init__(
        self,
        *,
        block_all_public_access: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        sse_enabled: typing.Optional[builtins.bool] = None,
        versioning_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param block_all_public_access: The path for the role. Default: true
        :param name: The name to identify the bucket. Will be appended to the prefix 'secure-bucket-'.
        :param sse_enabled: The path for the role. Default: false
        :param versioning_enabled: Whether to enable versioning or not on the bucket. Default: false
        '''
        if __debug__:
            def stub(
                *,
                block_all_public_access: typing.Optional[builtins.bool] = None,
                name: typing.Optional[builtins.str] = None,
                sse_enabled: typing.Optional[builtins.bool] = None,
                versioning_enabled: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument block_all_public_access", value=block_all_public_access, expected_type=type_hints["block_all_public_access"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            check_type(argname="argument versioning_enabled", value=versioning_enabled, expected_type=type_hints["versioning_enabled"])
        self._values: typing.Dict[str, typing.Any] = {}
        if block_all_public_access is not None:
            self._values["block_all_public_access"] = block_all_public_access
        if name is not None:
            self._values["name"] = name
        if sse_enabled is not None:
            self._values["sse_enabled"] = sse_enabled
        if versioning_enabled is not None:
            self._values["versioning_enabled"] = versioning_enabled

    @builtins.property
    def block_all_public_access(self) -> typing.Optional[builtins.bool]:
        '''The path for the role.

        :default: true
        '''
        result = self._values.get("block_all_public_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name to identify the bucket.

        Will be appended to the prefix 'secure-bucket-'.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_enabled(self) -> typing.Optional[builtins.bool]:
        '''The path for the role.

        :default: false
        '''
        result = self._values.get("sse_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def versioning_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable versioning or not on the bucket.

        :default: false
        '''
        result = self._values.get("versioning_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Bucket",
    "BucketConfig",
]

publication.publish()
