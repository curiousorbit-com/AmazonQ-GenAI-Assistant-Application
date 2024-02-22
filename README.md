# QBusinessApplication

## Prereqs
- Create an IAM role for Q Business application to access CloudWatch and CloudWatch Logs

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