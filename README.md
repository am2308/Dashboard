# Dashboard View
This utility will run as a python agent to monitor service level logs along with some custom metrics. Also this will help in showcasing the same on Grafana Dashboard.

## Tool Stack
```
OS Platform - Linux
```
```
Cloud Platform - AWS
```
```
Datasource - Cloudwatch
```
```
Dashbaord Tool - Grafana
```
```
Language - Python, Shell
```
```
Infrastructure Provisioning Tool - Terraform
```
## Working Process
* aws-cloudwatch-log agent will pull apache level logs and will push them to cloudwatch. It will capture both access logs as well as error logs.[LogMonitoring.sh] will help in automatically configuring the same.
* python script is going to fecth mertics like cpu utilization, memory utilization , disksapace utilization etc and will push data on cloudwatch. [MetricsCollection.py] script first willc all [LogMonitoring.sh] to push service level logs then it will push metrics to cloudwatch.
* Now [MetricMonitoring.service] will run python script as service. This service is configured to run in such a way that it will push data every 5 minute.

## Outcome
* [Grafana] (http://grafana-724446699.us-east-1.elb.amazonaws.com/). There would be 3 dashboard in dashboard sections with name ApacheServerLogsView, EC2ServerMonitoring, ServerMonitoring.
* [Cloudwatch] for apache logs level view.

## Future Scope
* As part of Iac(Infrastructure as Code), we can run [UserData] script in userdata section of ec2 instance whenever we are going to provision. This will help in enabling the automatic monitoring of underlying infrastructure.
* We can set alerting mechinism in Grafana itself to notify team. Slack/Email/PagerDuty/MicroSoft Teams are the examples that we can use for notification



