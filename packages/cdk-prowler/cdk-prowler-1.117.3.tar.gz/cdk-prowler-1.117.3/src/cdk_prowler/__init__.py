'''
[![NPM version](https://badge.fury.io/js/cdk-prowler.svg)](https://badge.fury.io/js/cdk-prowler)
[![PyPI version](https://badge.fury.io/py/cdk-prowler.svg)](https://badge.fury.io/py/cdk-prowler)
[![.NET version](https://img.shields.io/nuget/v/com.github.mmuller88.awsCdkBuildBadge.svg?style=flat-square)](https://www.nuget.org/packages/com.github.mmuller88.cdkProwler/)
![Release](https://github.com/mmuller88/cdk-prowler/workflows/Release/badge.svg)

# cdk-prowler

An AWS CDK custom construct for deploying Prowler to you AWS Account. The following description about Prowler is taken from https://github.com/toniblyx/prowler:

Prowler is a security tool to perform AWS security best practices assessments, audits, incident response, continuous monitoring, hardening and forensics readiness. It contains all CIS controls listed here https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf and more than 100 additional checks that help on GDPR, HIPAA…

# Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = App()

stack = Stack(app, "ProwlerAudit-stack")

ProwlerAudit(stack, "ProwlerAudit", enable_scheduler=True)
```

# Planned Features

* Supporting AWS SecurityHub https://github.com/toniblyx/prowler#security-hub-integration
* Triggering an event with SNS when prowler finishes the run
* AMI EC2 executable

# Misc

```sh
yes | yarn destroy && yarn deploy --require-approval never
```

Rerun Prowler on deploy

```sh
yarn deploy --require-approval never -c reRunProwler=true
```

# Thanks To

* My friend and fellaw ex colleague Tony de la Fuente (https://github.com/toniblyx https://twitter.com/ToniBlyx) for developing such a cool security tool as [Prowler](https://github.com/toniblyx/prowler)
* As always to the amazing CDK / Projen Community. Join us on [Slack](https://cdk-dev.slack.com)!
* [Projen](https://github.com/projen/projen) project and the community around it
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

import aws_cdk.aws_logs
import aws_cdk.core


class ProwlerAudit(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-prowler.ProwlerAudit",
):
    '''Creates a CodeBuild project to audit an AWS account with Prowler and stores the html report in a S3 bucket.

    This will run onece at the beginning and on a schedule afterwards. Partial contribution from https://github.com/stevecjones
    '''

    def __init__(
        self,
        parent: aws_cdk.core.Stack,
        id: builtins.str,
        *,
        enable_scheduler: typing.Optional[builtins.bool] = None,
        logs_retention_in_days: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        prowler_options: typing.Optional[builtins.str] = None,
        prowler_scheduler: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param enable_scheduler: enables the scheduler for running prowler periodically. Together with prowlerScheduler. Default: false
        :param logs_retention_in_days: Specifies the number of days you want to retain CodeBuild run log events in the specified log group. Junit reports are kept for 30 days, HTML reports in S3 are not deleted Default: : 3
        :param prowler_options: Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports. Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q" Default: '-M text,junit-xml,html,csv,json'
        :param prowler_scheduler: The time when Prowler will run in cron format. Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html. Default: 'cron(0 22 * * ? *)'
        :param service_name: Specifies the service name used within component naming. Default: : prowler
        '''
        props = ProwlerAuditProps(
            enable_scheduler=enable_scheduler,
            logs_retention_in_days=logs_retention_in_days,
            prowler_options=prowler_options,
            prowler_scheduler=prowler_scheduler,
            service_name=service_name,
        )

        jsii.create(ProwlerAudit, self, [parent, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableScheduler")
    def enable_scheduler(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableScheduler"))

    @enable_scheduler.setter
    def enable_scheduler(self, value: builtins.bool) -> None:
        jsii.set(self, "enableScheduler", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logsRetentionInDays")
    def logs_retention_in_days(self) -> aws_cdk.aws_logs.RetentionDays:
        return typing.cast(aws_cdk.aws_logs.RetentionDays, jsii.get(self, "logsRetentionInDays"))

    @logs_retention_in_days.setter
    def logs_retention_in_days(self, value: aws_cdk.aws_logs.RetentionDays) -> None:
        jsii.set(self, "logsRetentionInDays", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prowlerOptions")
    def prowler_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prowlerOptions"))

    @prowler_options.setter
    def prowler_options(self, value: builtins.str) -> None:
        jsii.set(self, "prowlerOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prowlerScheduler")
    def prowler_scheduler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prowlerScheduler"))

    @prowler_scheduler.setter
    def prowler_scheduler(self, value: builtins.str) -> None:
        jsii.set(self, "prowlerScheduler", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        jsii.set(self, "serviceName", value)


@jsii.data_type(
    jsii_type="cdk-prowler.ProwlerAuditProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_scheduler": "enableScheduler",
        "logs_retention_in_days": "logsRetentionInDays",
        "prowler_options": "prowlerOptions",
        "prowler_scheduler": "prowlerScheduler",
        "service_name": "serviceName",
    },
)
class ProwlerAuditProps:
    def __init__(
        self,
        *,
        enable_scheduler: typing.Optional[builtins.bool] = None,
        logs_retention_in_days: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        prowler_options: typing.Optional[builtins.str] = None,
        prowler_scheduler: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_scheduler: enables the scheduler for running prowler periodically. Together with prowlerScheduler. Default: false
        :param logs_retention_in_days: Specifies the number of days you want to retain CodeBuild run log events in the specified log group. Junit reports are kept for 30 days, HTML reports in S3 are not deleted Default: : 3
        :param prowler_options: Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports. Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q" Default: '-M text,junit-xml,html,csv,json'
        :param prowler_scheduler: The time when Prowler will run in cron format. Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html. Default: 'cron(0 22 * * ? *)'
        :param service_name: Specifies the service name used within component naming. Default: : prowler
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_scheduler is not None:
            self._values["enable_scheduler"] = enable_scheduler
        if logs_retention_in_days is not None:
            self._values["logs_retention_in_days"] = logs_retention_in_days
        if prowler_options is not None:
            self._values["prowler_options"] = prowler_options
        if prowler_scheduler is not None:
            self._values["prowler_scheduler"] = prowler_scheduler
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def enable_scheduler(self) -> typing.Optional[builtins.bool]:
        '''enables the scheduler for running prowler periodically.

        Together with prowlerScheduler.

        :default: false
        '''
        result = self._values.get("enable_scheduler")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logs_retention_in_days(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''Specifies the number of days you want to retain CodeBuild run log events in the specified log group.

        Junit reports are kept for 30 days, HTML reports in S3 are not deleted

        :default: : 3
        '''
        result = self._values.get("logs_retention_in_days")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def prowler_options(self) -> typing.Optional[builtins.str]:
        '''Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports.

        Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use  "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q"

        :default: '-M text,junit-xml,html,csv,json'
        '''
        result = self._values.get("prowler_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prowler_scheduler(self) -> typing.Optional[builtins.str]:
        '''The time when Prowler will run in cron format.

        Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html.

        :default: 'cron(0 22 * * ? *)'
        '''
        result = self._values.get("prowler_scheduler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the service name used within component naming.

        :default: : prowler
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProwlerAuditProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ProwlerAudit",
    "ProwlerAuditProps",
]

publication.publish()
