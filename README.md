# Building a QBusiness Application using Boto3
NOTE: This project is very much a work in progress. The intention of the project is to learn more about
GenAI in general and AmazonQ in particular.

This solution should not be used in production, and your mileage may vary. If you decide to deploy the 
solution, please ensure you are aware of the pricing models and how deploying this may effect your
AWS consumption.

## Prerequisites
This project relies on a number of items being in place for a successful deployment.

1. The project relies on AWS IAM Identity Center for authentication.
2. The project is written using Python and requires the Boto3 SDK to be installed.
3. In addition to Boto3, the project uses a library to help streamline SSO authentication.
4. Currently, you need to deploy an IAM role used by the QBusiness Application prior to running the script.

NOTES: 
- Make sure you review the requirements.txt file before attempting to deploy the solution.
- You can find information about the IAM Role mentioned above in the [AWS documentation](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/iam-roles.html)

## Configuration file
All configuration information required by the script is stored in a YAML file called config.yaml.

As part of the project, we included a sample-config.yaml file. You need to update this file prior to deployment.

Below is an example of the current configuration file and an explanation of the values.

```
sso_config:
  sso_start_url: <Add IAM Identity Center URL - including https://>
  sso_region: <Add the AWS region where Identity Center is running>
  account_id: <Add the 12-digit account ID where you'd like to deploy AmazonQ for business
  role_name: <Add the IAM role you'd like to use to access your AWS account>
deployment_config:
  aws_region: <Add the AWS region identifier where you'd like to deploy AmazonQ>
  q_app_name: AQBusinessPOC
  q_app_description: A POC for QBusiness
  q_index_name: AQBusinessIndexPOC
  q_index_description: A POC Index for QBusiness
  q_retriever_name: AQBusinessRetrieverPOC
  q_retriever_description: A POC Retriever for QBusiness
  q_application_role_arn: <Add the ARN for the service role>
  q_application_webcrawler_data_source_arn: <Add the ARN for the webcrawler role>
  q_application_web_experience_arn: <Add the ARN for the web experience role>
  environment: dev
```

The section entitled 'sso-config' contains the information required to use AWS IAM Identity Center to authenticate you 
before deployment.

- sso_start_url: The HTTPS address of your AWS IAM Identity Center instance
- sso_region: The AWS region where your Identity Center instance is running
- account_id: The 12-digit AWS account ID where you will be deploying the solution
- role_name: The name of the IAM Role you'll be assuming to perform the deployment

The section entitled 'deployment_config' contains the information required for the deployment of the Amazon Q application.

- aws_region: The AWS region where you would like to deploy AmazonQ
- q_app_name: The name of your QBusiness application - spaces are not allowed
- q_app_description: The description of your QBusiness application
- q_index_name: The name of your QBusiness Index - spaces are not allowed
- q_index_description: The description of your QBusiness application
- q_retriever_name: The name of your QBusiness retriever - spaces are not allowed
- q_retriever_description: The description of your QBusiness retriever - not currently used, but must be present
- q_application_role_arn: The ARN of the IAM role used by your QBusiness application
- q_application_webcrawler_data_source_arn: The ARN of the IAM role used by your QBusiness web crawler - not currently used, but must be present
- q_application_web_experience_arn: The ARN of the IAM role used by your QBusiness web experience - not currently used, but must be present
- environment: The name of your environment - defaults to dev

## TODO
- [X] Create a Boto3 session using SSO
- [X] Create a Boto3 client connection to Amazon Q
- [X] Create a Q application
- [X] Create a Q index
- [X] Create a waiter - use a while loop - no boto3 waiters
- [X] Create a Q retriever
- [X] Create a web experience
- [X] Test just to see what happens?
- [X] Create a web crawler data source

NOTE: we had to use Source Sitemap to crawl all the documents on the website. If we used the Source URL Q crawled only
a subset of the data on the site

## Future Ideas
- [X] Add logic to avoid the ongoing deletion/creation process used during the stream!
- [ ] Create required CFN templates
    - [ ] IAM Resources
        - [ ] Application Role
        - [ ] Data source Role
        - [ ] Web experience role
    - [ ] Secrets Manager resources
    - [ ] S3 resources
    - [ ] CMK
- [ ] Look into Validation exception errors in boto3 - can we get a useful message?
- [ ] Add a web Q crawler to the application - deployed via boto3
- [ ] Add additional data sources
    - [ ] Add an Identity crawler - controls what we can query via the AI Assistant
    - [ ] Add a Slack Q crawler
    - [ ] Add a JIRA Q crawler