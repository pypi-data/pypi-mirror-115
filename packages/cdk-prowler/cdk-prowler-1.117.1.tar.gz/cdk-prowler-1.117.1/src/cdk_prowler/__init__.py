'''
[![NPM version](https://badge.fury.io/js/cdk-prowler.svg)](https://badge.fury.io/js/cdk-prowler)
[![PyPI version](https://badge.fury.io/py/cdk-prowler.svg)](https://badge.fury.io/py/cdk-prowler)
[![.NET version](https://img.shields.io/nuget/v/com.github.mmuller88.awsCdkBuildBadge.svg?style=flat-square)](https://www.nuget.org/packages/com.github.mmuller88.cdkProwler/)
![Release](https://github.com/mmuller88/cdk-prowler/workflows/Release/badge.svg)

# cdk-prowler

An AWS CDK custom construct for deploying Prowler to you AWS Account. The following description about Prowler is taken from https://github.com/toniblyx/prowler:

Prowler is a security tool to perform AWS security best practices assessments, audits, incident response, continuous monitoring, hardening and forensics readiness. It contains all CIS controls listed here https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf and more than 100 additional checks that help on GDPR, HIPAA…

# Example

...

# Misc

yes | yarn destroy && yarn deploy --require-approval never

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
        logs_retention_in_days: aws_cdk.aws_logs.RetentionDays,
        prowler_scheduler: builtins.str,
        service_name: builtins.str,
        prowler_options: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param logs_retention_in_days: Specifies the number of days you want to retain CodeBuild run log events in the specified log group. Junit reports are kept for 30 days, HTML reports in S3 are not deleted Default: : 3
        :param prowler_scheduler: The time when Prowler will run in cron format. Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html. Default: 'cron(0 22 * * ? *)'
        :param service_name: Specifies the service name used within component naming. Default: : prowler
        :param prowler_options: Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports. Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q" Default: 'no options'
        '''
        props = ProwlerAuditProps(
            logs_retention_in_days=logs_retention_in_days,
            prowler_scheduler=prowler_scheduler,
            service_name=service_name,
            prowler_options=prowler_options,
        )

        jsii.create(ProwlerAudit, self, [parent, id, props])


@jsii.data_type(
    jsii_type="cdk-prowler.ProwlerAuditProps",
    jsii_struct_bases=[],
    name_mapping={
        "logs_retention_in_days": "logsRetentionInDays",
        "prowler_scheduler": "prowlerScheduler",
        "service_name": "serviceName",
        "prowler_options": "prowlerOptions",
    },
)
class ProwlerAuditProps:
    def __init__(
        self,
        *,
        logs_retention_in_days: aws_cdk.aws_logs.RetentionDays,
        prowler_scheduler: builtins.str,
        service_name: builtins.str,
        prowler_options: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param logs_retention_in_days: Specifies the number of days you want to retain CodeBuild run log events in the specified log group. Junit reports are kept for 30 days, HTML reports in S3 are not deleted Default: : 3
        :param prowler_scheduler: The time when Prowler will run in cron format. Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html. Default: 'cron(0 22 * * ? *)'
        :param service_name: Specifies the service name used within component naming. Default: : prowler
        :param prowler_options: Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports. Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q" Default: 'no options'
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "logs_retention_in_days": logs_retention_in_days,
            "prowler_scheduler": prowler_scheduler,
            "service_name": service_name,
        }
        if prowler_options is not None:
            self._values["prowler_options"] = prowler_options

    @builtins.property
    def logs_retention_in_days(self) -> aws_cdk.aws_logs.RetentionDays:
        '''Specifies the number of days you want to retain CodeBuild run log events in the specified log group.

        Junit reports are kept for 30 days, HTML reports in S3 are not deleted

        :default: : 3
        '''
        result = self._values.get("logs_retention_in_days")
        assert result is not None, "Required property 'logs_retention_in_days' is missing"
        return typing.cast(aws_cdk.aws_logs.RetentionDays, result)

    @builtins.property
    def prowler_scheduler(self) -> builtins.str:
        '''The time when Prowler will run in cron format.

        Default is daily at 22:00h or 10PM 'cron(0 22 * * ? *)', for every 5 hours also works 'rate(5 hours)'. More info here https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html.

        :default: 'cron(0 22 * * ? *)'
        '''
        result = self._values.get("prowler_scheduler")
        assert result is not None, "Required property 'prowler_scheduler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Specifies the service name used within component naming.

        :default: : prowler
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prowler_options(self) -> typing.Optional[builtins.str]:
        '''Options to pass to Prowler command, make sure at least -M junit-xml is used for CodeBuild reports.

        Use -r for the region to send API queries, -f to filter only one region, -M output formats, -c for comma separated checks, for all checks do not use -c or -g, for more options see -h. For a complete assessment use  "-M text,junit-xml,html,csv,json", for SecurityHub integration use "-r region -f region -M text,junit-xml,html,csv,json,json-asff -S -q"

        :default: 'no options'
        '''
        result = self._values.get("prowler_options")
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
