'''
[![GitHub](https://img.shields.io/github/license/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt?style=flat-square)](https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/blob/main/LICENSE)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt?sort=semver&style=flat-square)](https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/releases)
[![npm (scoped)](https://img.shields.io/npm/v/cdk-lambda-token-authorizer-jwt?style=flat-square)](https://www.npmjs.com/package/cdk-lambda-token-authorizer-jwt)
[![PyPI](https://img.shields.io/pypi/v/cloudy-with-a-chance-of-meatballs.cdk-lambda-token-authorizer-jwt?style=flat-square)](https://pypi.org/project/cloudy-with-a-chance-of-meatballs.cdk-lambda-token-authorizer-jwt/)
[![Nuget](https://img.shields.io/nuget/v/CloudyWithAchanceOfMeatballs.CdkLambdaTokenAuthorizerJwt?style=flat-square)](https://www.nuget.org/packages/CloudyWithAchanceOfMeatballs.CdkLambdaTokenAuthorizerJwt/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/release/main?label=release&style=flat-square)](https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/actions/workflows/release.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/10f0734997f4d96da662/maintainability)](https://codeclimate.com/github/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/maintainability)
[![codecov](https://codecov.io/gh/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt/branch/main/graph/badge.svg?token=86HXCCHOGJ)](https://codecov.io/gh/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt)

# CDK Lambda TokenAuthorizer JWT

Add a lambda function to your project which can be used as a apigateway token authorizer

## Install

### TypeScript

```shell
npm install @cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt
yarn add @cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt
```

### Python

```shell
pip install cloudy-with-a-chance-of-meatballs.cdk-lambda-token-authorizer-jwt
```

## Usage

```python

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

//### EXAMPLE: import the function
import { TokenAuthorizerJwtFunction } from "@cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt";
//### END

export class HelloworldStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const api = new apigateway.RestApi(this, 'ApiName', {});

    //### EXAMPLE: init the function
    const tokenAuthFunction = new TokenAuthorizerJwtFunction(this, 'lambdaFunctionName', {
      environment: {
        // PROVIDE VARIABLES
        TOKEN_AUTHORIZER_JWKS_URI: 'https://example.auth0.com/.well-known/jwks.json',
        TOKEN_AUTHORIZER_JWKS_KID: 'SOME_KID_FROM_JWKS_RESPONSE',
        // OR
        TOKEN_AUTHORIZER_JWT_VERIFICATION_SECRET: 'A_PUBLIC_KEY_OR_SYMETRIC_SECRET'
      }
    });
    //### END

    const tokenAuthorizer = new apigateway.TokenAuthorizer(this, 'tokenAuthorizerName', {
      //### EXAMPLE: use as handler
      handler: tokenAuthFunction
      //### END
    });

    // ...
    const someMethod = SOMEAPIRESOURCE.addMethod("GET", SOMETARGETINTEGRATION, { authorizer: tokenAuthorizer });
  }
}
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

import aws_cdk
import aws_cdk.aws_codeguruprofiler
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_sqs
import constructs


class TokenAuthorizerJwtFunction(
    aws_cdk.aws_lambda.Function,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-token-authorizer-jwt.TokenAuthorizerJwtFunction",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[aws_cdk.aws_lambda.Architecture] = None,
        code_signing_config: typing.Optional[aws_cdk.aws_lambda.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[aws_cdk.aws_lambda.VersionOptions, typing.Dict[str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        events: typing.Optional[typing.Sequence[aws_cdk.aws_lambda.IEventSource]] = None,
        filesystem: typing.Optional[aws_cdk.aws_lambda.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        insights_version: typing.Optional[aws_cdk.aws_lambda.LambdaInsightsVersion] = None,
        layers: typing.Optional[typing.Sequence[aws_cdk.aws_lambda.ILayerVersion]] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[aws_cdk.aws_lambda.LogRetentionRetryOptions, typing.Dict[str, typing.Any]]] = None,
        log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[aws_cdk.aws_codeguruprofiler.IProfilingGroup] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        max_event_age: typing.Optional[aws_cdk.Duration] = None,
        on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination] = None,
        on_success: typing.Optional[aws_cdk.aws_lambda.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                allow_all_outbound: typing.Optional[builtins.bool] = None,
                allow_public_subnet: typing.Optional[builtins.bool] = None,
                architecture: typing.Optional[aws_cdk.aws_lambda.Architecture] = None,
                code_signing_config: typing.Optional[aws_cdk.aws_lambda.ICodeSigningConfig] = None,
                current_version_options: typing.Optional[typing.Union[aws_cdk.aws_lambda.VersionOptions, typing.Dict[str, typing.Any]]] = None,
                dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue] = None,
                dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
                description: typing.Optional[builtins.str] = None,
                environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                environment_encryption: typing.Optional[aws_cdk.aws_kms.IKey] = None,
                events: typing.Optional[typing.Sequence[aws_cdk.aws_lambda.IEventSource]] = None,
                filesystem: typing.Optional[aws_cdk.aws_lambda.FileSystem] = None,
                function_name: typing.Optional[builtins.str] = None,
                initial_policy: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
                insights_version: typing.Optional[aws_cdk.aws_lambda.LambdaInsightsVersion] = None,
                layers: typing.Optional[typing.Sequence[aws_cdk.aws_lambda.ILayerVersion]] = None,
                log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
                log_retention_retry_options: typing.Optional[typing.Union[aws_cdk.aws_lambda.LogRetentionRetryOptions, typing.Dict[str, typing.Any]]] = None,
                log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
                memory_size: typing.Optional[jsii.Number] = None,
                profiling: typing.Optional[builtins.bool] = None,
                profiling_group: typing.Optional[aws_cdk.aws_codeguruprofiler.IProfilingGroup] = None,
                reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
                role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
                security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
                timeout: typing.Optional[aws_cdk.Duration] = None,
                tracing: typing.Optional[aws_cdk.aws_lambda.Tracing] = None,
                vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
                vpc_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
                max_event_age: typing.Optional[aws_cdk.Duration] = None,
                on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination] = None,
                on_success: typing.Optional[aws_cdk.aws_lambda.IDestination] = None,
                retry_attempts: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_lambda.FunctionOptions(
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "TokenAuthorizerJwtFunction",
]

publication.publish()
