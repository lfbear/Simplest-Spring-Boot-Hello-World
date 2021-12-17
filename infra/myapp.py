from typing import Protocol
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
)
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_cloudwatch_actions as cw_actions
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as sns_subs
import aws_cdk.aws_logs as logs
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
from aws_cdk.core import CfnOutput, Stack, CfnParameter
from constructs import Construct


class MyAppStack(Stack):
    def __init__(self, scope: Construct, id: str, version: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create VPC and Fargate Cluster
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)
        cluster = ecs.Cluster(self, "Ec2Cluster", vpc=vpc)

        # create serverless config(TaskDefinition)
        repository = ecr.Repository.from_repository_arn(
            self,
            id,
            "arn:aws:ecr:%s:%d:repository/%s"
            % (
                "us-west-2",
                237794796217,
                id,
            ),  # todo: replace with AWS_DEFAULT_REGION and AWS_ACCESS_KEY_ID
        )

        task_definition = ecs.TaskDefinition(
            self,
            "TaskDefinition",
            compatibility=ecs.Compatibility.FARGATE,
            cpu="256",
            memory_mib="512",
        )

        log_group = logs.LogGroup(
            self, "LogGroup", log_group_name="myapp"
        )  # log group for logging app's output and creating metric filter later, alarm will depend this.

        task_definition.add_container(
            id,
            container_name="web",
            port_mappings=[
                ecs.PortMapping(container_port=9092)
            ],  # todo: replace with port in dockerfile env
            image=ecs.ContainerImage.from_ecr_repository(repository, version),
            logging=ecs.LogDriver.aws_logs(
                log_group=log_group, stream_prefix="[myapp]"
            ),
        )

        # service and loadbalancer
        service = ecs.FargateService(
            self,
            "FargateService",
            cluster=cluster,
            task_definition=task_definition,
        )

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        listener = lb.add_listener("Listener", port=80)

        service.register_load_balancer_targets(
            ecs.EcsTarget(
                container_name="web",
                new_target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(
                    listener, protocol=elbv2.ApplicationProtocol.HTTP
                ),
            )
        )

        # meric and sns subscriptions
        metric_name = "errors"
        metric_namespace = "myapp"
        metric = cloudwatch.Metric(metric_name=metric_name, namespace=metric_namespace)

        logs.MetricFilter(
            self,
            "MetricFilter",
            log_group=log_group,
            metric_namespace=metric_namespace,
            metric_name=metric_name,
            filter_pattern=logs.FilterPattern().all_terms("error"),
        )

        cw = cloudwatch.Alarm(
            self,
            "Errors",
            metric=metric,
            alarm_name="myAppErrors",
            actions_enabled=True,
            evaluation_periods=1,
            threshold=1,
        )
        topic = sns.Topic(self, "ErrorLog")
        topic.add_subscription(sns_subs.EmailSubscription("email@yourcompany.com"))
        cw.add_alarm_action(cw_actions.SnsAction(topic))

        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=listener.load_balancer.load_balancer_dns_name,
        )
