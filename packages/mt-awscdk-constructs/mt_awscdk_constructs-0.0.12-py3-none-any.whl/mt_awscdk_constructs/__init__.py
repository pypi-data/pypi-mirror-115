'''
# Marley Tech AWS CDK Construct Library

A collection of useful AWS CDK Constructs.

## Constructs

### EventFunction

A Construct which provides the resource for triggering a Lambda Function via a EventBridge Rule. It includes the Dead Letter Queues for the delivery and the processing of the event.

![Event Function Architecture Diagram](docs/EventFunction/EventFunction.png)

The Event Function Lambda is given the following Environment Variables:

* `PROCESSING_DLQ_ARN` - the SQS Queue ARN of the Processing DLQ (to assist the Lambda Code to publish failed messages to this queue)
* `PROCESSING_DLQ_NAME` - the SQS Queue Name of the Processing DLQ (to assist the Lambda Code to publish failed messages to this queue)

#### Resources

This Construct deploy the following resources:

* Rule (EventBridge Rule) - The trigger or event rule which will be passed to the Event Function
* Event Function (Lambda Function) - The code which will be executed
* Delivery DLQ (SQS Queue) - A DLQ which undeliverable Events are pushed to (e.g. if the Event Function is unreachable)
* Processing DLQ (SQS Queue) - A DLQ which the Event Fucntion may push Events to if it considers the Event to be unprocessable (e.g. if the Event is in an unexpected structure)

##### Alarms

The SQS Queues which act as DLQs have Alarms configured which are triggered when messages are posted to them. To subscribe to these Alarms, provide an SNS Topic for each DLQ.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Contributor Code Of Conduct

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree
to abide [by its terms](CODE_OF_CONDUCT.md).
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

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.core


class EventFunction(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="mt-awscdk-constructs.EventFunction",
):
    '''EventFunction.

    A Lambda Function, triggered by an EventBridge Event

    Includes additional resources:

    - Configurable EventBridge Rule
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        function_props: aws_cdk.aws_lambda.FunctionProps,
        rule_props: aws_cdk.aws_events.RuleProps,
        delivery_dlq_alarm_topic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        delivery_dlq_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
        delivery_props: typing.Optional["EventFunctionDeliveryProps"] = None,
        processing_dlq_alarm_topic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        processing_dlq_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param function_props: Configuration of the Event Function Lambda.
        :param rule_props: The configuration and behaviour of the EventBridge Rule which links the EventBus and the Event Function Lambda.
        :param delivery_dlq_alarm_topic: SNS Topic to which any Alarms relating to the Delivery DLQ should be subscribed.
        :param delivery_dlq_props: Configuration of the Delivery DLQ.
        :param delivery_props: Configuration of the Delivery properties to the Event Function Lambda.
        :param processing_dlq_alarm_topic: SNS Topic to which any Alarms relating to the Processing DLQ should be subscribed.
        :param processing_dlq_props: Configuration of the Processing DLQ.
        '''
        props = EventFunctionProps(
            function_props=function_props,
            rule_props=rule_props,
            delivery_dlq_alarm_topic=delivery_dlq_alarm_topic,
            delivery_dlq_props=delivery_dlq_props,
            delivery_props=delivery_props,
            processing_dlq_alarm_topic=processing_dlq_alarm_topic,
            processing_dlq_props=processing_dlq_props,
        )

        jsii.create(EventFunction, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryDlq")
    def delivery_dlq(self) -> aws_cdk.aws_sqs.Queue:
        '''The SQS Queue which acts as a DLQ for any EventBridge Delivery failures.'''
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "deliveryDlq"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryDlqNotEmptyAlarm")
    def delivery_dlq_not_empty_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        '''An Alarm which is triggered if any messages are sent to the Delivery DLQ.'''
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "deliveryDlqNotEmptyAlarm"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.Function:
        '''Lambda Function which is the target of the Event.'''
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "handler"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="processingDlq")
    def processing_dlq(self) -> aws_cdk.aws_sqs.Queue:
        '''The SQS Queue which acts as a DLQ for any events which the Event Function is unable to process.'''
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "processingDlq"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="processingDlqNotEmptyAlarm")
    def processing_dlq_not_empty_alarm(self) -> aws_cdk.aws_cloudwatch.Alarm:
        '''An Alarm which is triggered if any messages are sent to the Processing DLQ.'''
        return typing.cast(aws_cdk.aws_cloudwatch.Alarm, jsii.get(self, "processingDlqNotEmptyAlarm"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rule")
    def rule(self) -> aws_cdk.aws_events.Rule:
        '''EventBridge Rule which controls when the Event Function is triggered.'''
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "rule"))


@jsii.data_type(
    jsii_type="mt-awscdk-constructs.EventFunctionDeliveryProps",
    jsii_struct_bases=[],
    name_mapping={"max_event_age": "maxEventAge", "retry_attempts": "retryAttempts"},
)
class EventFunctionDeliveryProps:
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[aws_cdk.core.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing.
        :param retry_attempts: The maximum number of times to retry when the function returns an error.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def max_event_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.'''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.'''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventFunctionDeliveryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="mt-awscdk-constructs.EventFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_props": "functionProps",
        "rule_props": "ruleProps",
        "delivery_dlq_alarm_topic": "deliveryDlqAlarmTopic",
        "delivery_dlq_props": "deliveryDlqProps",
        "delivery_props": "deliveryProps",
        "processing_dlq_alarm_topic": "processingDlqAlarmTopic",
        "processing_dlq_props": "processingDlqProps",
    },
)
class EventFunctionProps:
    def __init__(
        self,
        *,
        function_props: aws_cdk.aws_lambda.FunctionProps,
        rule_props: aws_cdk.aws_events.RuleProps,
        delivery_dlq_alarm_topic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        delivery_dlq_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
        delivery_props: typing.Optional[EventFunctionDeliveryProps] = None,
        processing_dlq_alarm_topic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        processing_dlq_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
    ) -> None:
        '''
        :param function_props: Configuration of the Event Function Lambda.
        :param rule_props: The configuration and behaviour of the EventBridge Rule which links the EventBus and the Event Function Lambda.
        :param delivery_dlq_alarm_topic: SNS Topic to which any Alarms relating to the Delivery DLQ should be subscribed.
        :param delivery_dlq_props: Configuration of the Delivery DLQ.
        :param delivery_props: Configuration of the Delivery properties to the Event Function Lambda.
        :param processing_dlq_alarm_topic: SNS Topic to which any Alarms relating to the Processing DLQ should be subscribed.
        :param processing_dlq_props: Configuration of the Processing DLQ.
        '''
        if isinstance(function_props, dict):
            function_props = aws_cdk.aws_lambda.FunctionProps(**function_props)
        if isinstance(rule_props, dict):
            rule_props = aws_cdk.aws_events.RuleProps(**rule_props)
        if isinstance(delivery_dlq_props, dict):
            delivery_dlq_props = aws_cdk.aws_sqs.QueueProps(**delivery_dlq_props)
        if isinstance(delivery_props, dict):
            delivery_props = EventFunctionDeliveryProps(**delivery_props)
        if isinstance(processing_dlq_props, dict):
            processing_dlq_props = aws_cdk.aws_sqs.QueueProps(**processing_dlq_props)
        self._values: typing.Dict[str, typing.Any] = {
            "function_props": function_props,
            "rule_props": rule_props,
        }
        if delivery_dlq_alarm_topic is not None:
            self._values["delivery_dlq_alarm_topic"] = delivery_dlq_alarm_topic
        if delivery_dlq_props is not None:
            self._values["delivery_dlq_props"] = delivery_dlq_props
        if delivery_props is not None:
            self._values["delivery_props"] = delivery_props
        if processing_dlq_alarm_topic is not None:
            self._values["processing_dlq_alarm_topic"] = processing_dlq_alarm_topic
        if processing_dlq_props is not None:
            self._values["processing_dlq_props"] = processing_dlq_props

    @builtins.property
    def function_props(self) -> aws_cdk.aws_lambda.FunctionProps:
        '''Configuration of the Event Function Lambda.'''
        result = self._values.get("function_props")
        assert result is not None, "Required property 'function_props' is missing"
        return typing.cast(aws_cdk.aws_lambda.FunctionProps, result)

    @builtins.property
    def rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''The configuration and behaviour of the EventBridge Rule which links the EventBus and the Event Function Lambda.'''
        result = self._values.get("rule_props")
        assert result is not None, "Required property 'rule_props' is missing"
        return typing.cast(aws_cdk.aws_events.RuleProps, result)

    @builtins.property
    def delivery_dlq_alarm_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''SNS Topic to which any Alarms relating to the Delivery DLQ should be subscribed.'''
        result = self._values.get("delivery_dlq_alarm_topic")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], result)

    @builtins.property
    def delivery_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Delivery DLQ.'''
        result = self._values.get("delivery_dlq_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    @builtins.property
    def delivery_props(self) -> typing.Optional[EventFunctionDeliveryProps]:
        '''Configuration of the Delivery properties to the Event Function Lambda.'''
        result = self._values.get("delivery_props")
        return typing.cast(typing.Optional[EventFunctionDeliveryProps], result)

    @builtins.property
    def processing_dlq_alarm_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''SNS Topic to which any Alarms relating to the Processing DLQ should be subscribed.'''
        result = self._values.get("processing_dlq_alarm_topic")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], result)

    @builtins.property
    def processing_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Processing DLQ.'''
        result = self._values.get("processing_dlq_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventFunction",
    "EventFunctionDeliveryProps",
    "EventFunctionProps",
]

publication.publish()
