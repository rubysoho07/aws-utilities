import boto3
import botocore

client = boto3.client('iam')
iam = boto3.resource('iam')

policies = client.list_policies(Scope='Local')['Policies']

def delete_all_policy_versions(policy_arn: str):
    versions = client.list_policy_versions(PolicyArn=policy_arn)['Versions']

    # To retain default version of a policy, starts with second version.
    for version in versions[1:]:
        v = iam.PolicyVersion(policy_arn, version['VersionId'])
        v.delete()

for policy in policies:
    p = iam.Policy(policy['Arn'])

    try:
        if p.attachment_count == 0:
            print(f"IAM Policy {policy['PolicyName']} not attached, so it will be deleted...", end='')
            p.delete()
            print("COMPLETED!")
    except botocore.exceptions.ClientError as err:
        error_code = err.response['Error']['Code']

        if error_code == 'DeleteConflict':
            delete_all_policy_versions(policy['Arn'])
            p.delete()
            print("COMPLETED!")
        else:
            print(f"NOT COMPLETED BECAUSE OF EXCEPTION ({err.response['Error']['Code']})")