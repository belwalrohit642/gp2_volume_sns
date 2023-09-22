import boto3
import json

# Define your AWS SNS topic ARN and AWS region
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:640284417783:gp2_volume'
AWS_REGION = 'us-east-1'

def check_ebs_volumes():
    try:
        ec2 = boto3.client('ec2', region_name=AWS_REGION)
        ebs_volumes = ec2.describe_volumes(Filters=[{'Name': 'volume-type', 'Values': ['gp2']}])['Volumes']

        if ebs_volumes:
            sns = boto3.client('sns', region_name=AWS_REGION)
            message = 'There are gp2 EBS volumes in your AWS account.'
            sns.publish(TopicArn=SNS_TOPIC_ARN, Subject='GP2 EBS Volumes Found', Message=message)
            return "There are gp2 EBS volumes in your AWS account."
        else:
            return "No gp2 EBS volumes found in your AWS account."

    except Exception as e:
        raise e

def check_ec2_instances():
    try:
        ec2 = boto3.client('ec2', region_name=AWS_REGION)
        environment_tag = 'environment'
        jira_tag = 'jira'

        ec2_instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}])

        instances_with_tags = []

        for reservation in ec2_instances['Reservations']:
            for instance in reservation['Instances']:
                tags = instance.get('Tags', [])
                has_environment_tag = False
                has_jira_tag = False

                for tag in tags:
                    if tag['Key'] == environment_tag:
                        has_environment_tag = True
                    if tag['Key'] == jira_tag:
                        has_jira_tag = True

                if has_environment_tag and has_jira_tag:
                    instances_with_tags.append(instance['InstanceId'])

        if instances_with_tags:
            sns = boto3.client('sns', region_name=AWS_REGION)
            message = f"EC2 instances with both 'environment' and 'jira' tags found: {', '.join(instances_with_tags)}"
            sns.publish(TopicArn=SNS_TOPIC_ARN, Subject='EC2 instance found with both tags', Message=message)
            return f"EC2 instances with both 'environment' and 'jira' tags found: {', '.join(instances_with_tags)}"
        else:
            return "No EC2 instances found with both 'environment' and 'jira' tags."

    except Exception as e:
        raise e

def check_available_ebs_volumes():
    try:
        ec2 = boto3.client('ec2', region_name=AWS_REGION)
        available_volume_ids = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

        if not available_volume_ids['Volumes']:
            return "No available EBS volumes found."
        else:
            sns = boto3.client('sns', region_name=AWS_REGION)
            message = "Available EBS Volumes:\n" + '\n'.join(f"Volume ID: {v['VolumeId']}" for v in available_volume_ids['Volumes'])
            sns.publish(TopicArn=SNS_TOPIC_ARN, Subject='EBS Volume is available', Message=message)
            return message

    except Exception as e:
        raise e

def lambda_handler(event, context):
    responses = []
    responses.append(check_ebs_volumes())
    responses.append(check_ec2_instances())
    responses.append(check_available_ebs_volumes())
    return "\n".join(responses)


