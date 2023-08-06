'''
# Welcome to your CDK TypeScript Construct Library project!

You should explore the contents of this project. It demonstrates a CDK Construct Library that includes a construct (`MyConstruct`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The construct defines an interface (`MyConstructProps`) to configure the visibility timeout of the queue.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class MyConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="my-construct.MyConstruct",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_description: typing.Optional[builtins.str] = None,
        api_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_description: 
        :param api_name: 

        :stability: experimental
        '''
        props = MyConstructProps(api_description=api_description, api_name=api_name)

        jsii.create(MyConstruct, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiDescription")
    def api_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiDescription"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiName")
    def api_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiName"))


@jsii.data_type(
    jsii_type="my-construct.MyConstructProps",
    jsii_struct_bases=[],
    name_mapping={"api_description": "apiDescription", "api_name": "apiName"},
)
class MyConstructProps:
    def __init__(
        self,
        *,
        api_description: typing.Optional[builtins.str] = None,
        api_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_description: 
        :param api_name: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if api_description is not None:
            self._values["api_description"] = api_description
        if api_name is not None:
            self._values["api_name"] = api_name

    @builtins.property
    def api_description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("api_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MyConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MyConstruct",
    "MyConstructProps",
]

publication.publish()
