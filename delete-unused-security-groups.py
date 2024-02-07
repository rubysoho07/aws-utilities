import boto3
import botocore

client = boto3.client('ec2')

security_groups = client.describe_security_groups()['SecurityGroups']

for security_group in security_groups:
    if security_group['GroupName'] == 'default':
        continue

    references = client.describe_network_interfaces(
        Filters=[{
            "Name": "group-id",
            "Values": [security_group['GroupId']]
        }]
    )['NetworkInterfaces']

    if len(references) == 0:
        try:
            client.delete_security_group(GroupId=security_group['GroupId'])
            print(f"Security Group {security_group['GroupId']}({security_group['GroupName']}) DELETED")
        except botocore.exceptions.ClientError as err:
            error_code = err.response['Error']['Code']
            if error_code == 'DependencyViolation':
                print(f"Security Group {security_group['GroupId']}({security_group['GroupName']}) SKIPPED (Due to DependencyViolation)")
            else:
                raise err
