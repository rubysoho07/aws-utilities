import boto3

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
        client.delete_security_group(GroupId=security_group['GroupId'])
        print(f"Security Group {security_group['GroupId']}({security_group['GroupName']}) Deleted")

