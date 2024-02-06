import boto3
import time
import botocore
import yaml
from aws_sso_lib import get_boto3_session


def main():
    # Grab the configuration values we need for the rest of the script
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    sso_start_url = config['config']['sso_start_url']
    sso_region = config['config']['sso_region']
    account_id = config['config']['account_id']
    role_name = config['config']['role_name']
    aws_region = config['config']['aws_region']

    # Connect to the demo account using AWS Identity Center
    boto3_session = get_boto3_session(sso_start_url, sso_region, account_id, role_name, region=aws_region,
                                      login=True)

    # Create a boto3 client for the QBusiness service
    q_client = boto3_session.client('qbusiness')

    # Close the client
    q_client.close()


main()
