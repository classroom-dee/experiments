### poc
- [x] weather
- [ ] OpenAQ for air quality
- [ ] crime: https://opendata.cityofnewyork.us
- [ ] news: https://www.nyc.gov/news -> uses quary params

### Notes
- check weather api interval

### Arch

*Turn off EC2 when not using*

Main Pipeline
1. EventBridge Scheduler -> 
2. Step Function -> : use Standard not Express
3. Lambda ETL jobs -> S3 Lakehouse (Iceberg format)
4. On failure -> Step functions retry/catch -> SQS DLQ(failed job) + SNS alert topic(notification)
5. On success -> small Lambda for graph/cache refreshing
6. Ec2 spot instance serves the dashboard with graphs

Monitoring
1. CloudTrail -> account activity to cloudwatch
2. CloudWatch -> alert to SNS on critical failure / serious violation: use short log retention for cost reduction

Cost Management
1. A EC2 spot instance to serve dashboard from Cost Explorer API
2. AWS Budget alerts to SNS

Alert
1. SNS gathers all alerts and a small Lambda sends alerts to Discord

API Gateway
- GET /ingest/status
- POST /ingest/action/manual
- POST /rebuild-summary

CloudFormation
- Tag things for clean orchestration
- Deploy the whole infra
- S3 cleanup and logs + Delete the whole infra (bash script + aws cli)