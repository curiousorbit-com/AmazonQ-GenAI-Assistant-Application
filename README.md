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

## TODO
[X] Create a Boto3 session using SSO
[X] Create a Boto3 client connection to Amazon Q
[X] Create a Q application
[X] Create a Q index
[X] Create a waiter - use a while loop - no boto3 waiters
[X] Create a Q retriever
[X] Create a web experience
[X] Test just to see what happens?
[X] Create a web crawler data source

NOTE: we had to use Source Sitemap to crawl all the documents on the website. If we used the Source URL Q crawled only
a subset of the data on the site

## Future Ideas
[X] Add logic to avoid the ongoing deletion/creation process used during the stream!
[ ] Create required CFN templates
    [ ] IAM Resources
        [ ] Application Role
        [ ] Data source Role
        [ ] Web experience role
    [ ] Secrets Manager resources
    [ ] S3 resources
    [ ] CMK
[ ] Look into Validation exception errors in boto3 - can we get a useful message?
[ ] Add a web Q crawler to the application - deployed via boto3
[ ] Add additional data sources
    [ ] Add an Identity crawler - controls what we can query via the AI Assistant
    [ ] Add a Slack Q crawler
    [ ] Add a JIRA Q crawler