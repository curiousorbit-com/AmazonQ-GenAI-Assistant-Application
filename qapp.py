import boto3
import time
import botocore
import yaml
from aws_sso_lib import get_boto3_session

Q_APP_NAME = 'ATwitchDemoApp'
Q_INDEX_NAME = 'ATwitchDemoIndex'


def list_q_apps(client):
    app_exists = False
    app_id = ''
    try:
        response = client.list_applications()
        for item in response['applications']:
            if item['displayName'] == Q_APP_NAME:
                app_exists = True
                app_id = item['applicationId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])

    return app_exists, app_id


def list_q_indexes(client, q_app_id):
    q_index_exists = False
    q_index_id = ''
    try:
        response = client.list_indices(
            applicationId=q_app_id
        )
        for item in response['indices']:
            if item['displayName'] == Q_INDEX_NAME:
                q_index_exists = True
                q_index_id = item['indexId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])

    return q_index_exists, q_index_id


def list_q_retrievers(client, q_app_id):
    q_retriever_exists = False
    q_retriever_id = ''

    try:
        response = client.list_retrievers(
            applicationId=q_app_id
        )
        for item in response['retrievers']:
            if item['displayName'] == 'ATwitchDemoRetriever':
                q_retriever_exists = True
                q_retriever_id = item['retrieverId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])

    return q_retriever_exists, q_retriever_id


def list_q_web_experiences(client, q_app_id):
    q_web_experience_exists = False
    q_web_experience_id = ''

    try:
        response = client.list_web_experiences(
            applicationId=q_app_id
        )
        for item in response['webExperiences']:
            if item['status'] == 'ACTIVE':
                q_web_experience_exists = True
                q_web_experience_id = item['webExperienceId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])

    return q_web_experience_exists, q_web_experience_id


def get_app_details(client, q_app_id):
    try:
        response = client.get_application(
            applicationId=q_app_id
        )
        q_app_arn = response['applicationArn']
        q_app_id = response['applicationId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])

    return q_app_arn, q_app_id


def create_q_application(client, q_app_desc, q_app_name, q_app_role_arn, q_environment):
    print('Creating a Q application...')
    try:
        response = client.create_application(
            description=q_app_desc,
            displayName=q_app_name,
            roleArn=q_app_role_arn,
            tags=[
                {'key': 'owner', 'value': 'CuriosOrbit'},
                {'key': 'ownerEmail', 'value': 'twitch@curiousorbit.com'},
                {'key': 'environment', 'value': q_environment},
            ]
        )
        return response['applicationArn'], response['applicationId']
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ConflictException':
            print('A Q business application with that name already exists. Exiting.')
            exit(1)
        else:
            print(error.response['Error']['Code'])


def create_q_index(client, q_app_id, q_index_cap_units, q_index_desc, q_index_name, q_environment):
    print('Creating a Q Index...')
    try:
        response = client.create_index(
            applicationId=q_app_id,
            capacityConfiguration={
                'units': q_index_cap_units
            },
            description=q_index_desc,
            displayName=q_index_name,
            tags=[
                {'key': 'owner', 'value': 'CuriosOrbit'},
                {'key': 'ownerEmail', 'value': 'twitch@curiousorbit.com'},
                {'key': 'environment', 'value': q_environment},
            ]
        )
        return response['indexArn'], response['indexId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])


def create_q_retriever(client, q_app_id, q_index_id, q_retriever_name, q_retriever_type, q_environment):
    print('Creating a Q retriever...')
    try:
        response = client.create_retriever(
            applicationId=q_app_id,
            configuration={
                'nativeIndexConfiguration': {
                    'indexId': q_index_id
                }
            },
            displayName=q_retriever_name,
            type=q_retriever_type,
            tags=[
                {'key': 'owner', 'value': 'CuriosOrbit'},
                {'key': 'ownerEmail', 'value': 'twitch@curiousorbit.com'},
                {'key': 'environment', 'value': q_environment},
            ]
        )
        return response['retrieverArn'], response['retrieverId']
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])
    except botocore.exceptions.ParamValidationError as error:
        print(error.response['Error']['Code'])


def create_q_web_experience(client, q_app_id, q_web_prompt_mode, q_web_subtitle, q_web_title, q_web_welcome_msg, q_environment):
    print('Creating a Q web experience...')
    try:
        response = client.create_web_experience(
            applicationId=q_app_id,
            samplePromptsControlMode=q_web_prompt_mode,
            subtitle=q_web_subtitle,
            title=q_web_title,
            welcomeMessage=q_web_welcome_msg,
            tags=[
                {'key': 'owner', 'value': 'CuriosOrbit'},
                {'key': 'ownerEmail', 'value': 'twitch@curiousorbit.com'},
                {'key': 'environment', 'value': q_environment},
            ]
        )
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])


def main():
    # Grab the configuration values we need for the rest of the script
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    sso_start_url = config['sso_config']['sso_start_url']
    sso_region = config['sso_config']['sso_region']
    account_id = config['sso_config']['account_id']
    role_name = config['sso_config']['role_name']
    aws_region = config['deployment_config']['aws_region']
    environment = config['deployment_config']['environment']
    q_application_role_arn = config['deployment_config']['q_application_role_arn']
    q_application_webcrawler_data_source_arn = config['deployment_config']['q_application_webcrawler_data_source_arn']
    q_application_web_experience_arn = config['deployment_config']['q_application_web_experience_arn']

    # Connect to the demo account using AWS Identity Center
    boto3_session = get_boto3_session(sso_start_url, sso_region, account_id, role_name, region=aws_region,
                                      login=True)

    # Create a boto3 client for the QBusiness service
    q_client = boto3_session.client('qbusiness')

    # Check to see if a QBusiness application with the defined name already exists. If it doesn't create it
    # if it does, grab the info we need and continue
    app_exists, app_id = list_q_apps(q_client)
    if app_exists:
        print('A Q Business application with that name already exists.')
        # Since the application already exists, we'll grab the ARN and ID, so we can continue with the script
        q_app_arn, q_app_id = get_app_details(q_client, app_id)
    else:
        print('A Q Business application with that name does not exist. Creating it now.')
        # Before creating the Q application, check to make sure one doesn't already exist with the same name.
        q_app_arn, q_app_id = create_q_application(q_client, 'A Twitch Demo Application', Q_APP_NAME,
                                                   q_application_role_arn, environment)

    # Check to see if an index already exists, if not create it. If it does, grab the info we need and continue.
    q_index_exists, q_index_id = list_q_indexes(q_client, q_app_id)
    if q_index_exists:
        print('A Q Index with that name already exists.')
    else:
        print('A Q Index with that name does not exist. Creating it now.')
        # Before creating the Q Index, check to make sure one doesn't already exist with the same name.
        q_index_arn, q_index_id = create_q_index(q_client, q_app_id, 1, 'A Twitch Demo Index',
                                                 'ATwitchDemoIndex', environment)

        # We need to wait on the Index, before we can create the retriever
        index_created = False

        while not index_created:
            try:
                response = q_client.get_index(
                    applicationId=q_app_id,
                    indexId=q_index_id
                )
                if response['status'] == 'ACTIVE':
                    index_created = True
            except botocore.exceptions.ClientError as error:
                print(error.response['Error']['Code'])
            print('Waiting on the Q Index to be created ...')
            time.sleep(30)

    # Check to see if the Q retriever already exists, if not create it. If it does, grab the info we need and continue.
    q_retriever_exists, q_retriever_id = list_q_retrievers(q_client, q_app_id)
    if q_retriever_exists:
        print('A Q Retriever with that name already exists.')
    else:
        print('A Q Retriever with that name does not exist. Creating it now.')
        create_q_retriever(q_client, q_app_id, q_index_id, 'ATwitchDemoRetriever', 'NATIVE_INDEX',
                           environment)

    # Create a web experience
    q_web_experience_exists, q_web_experience_id = list_q_web_experiences(q_client, q_app_id)
    if q_web_experience_exists:
        print('A Q Web Experience with that name already exists.')
    else:
        print('A Q Web Experience does not exist. Creating it now.')
        create_q_web_experience(q_client, q_app_id, 'DISABLED', 'A Twitch Demo Web Experience',
                                'A Twitch Demo Web Experience', 'Say \'Hi\' to Gordo - he\'s here to help!', environment)

    # Close the client
    q_client.close()


main()
