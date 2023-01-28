# Automatic RDS Snapshot Deletion with AWS Lambda
This is a Lambda function written in Python that finds and deletes old RDS snapshots. It's triggered by EventBridge on a schedule set in the SAM template. Users can customize the schedule, snapshot name filter and age threshold in the SAM template parameters.

## Prerequisites
- AWS CLI
- AWS SAM CLI
- Make
- Python 3.6+ (I use 3.10 for development)

## Deployment
1. Clone the repository:
```bash
git clone https://github.com/nopnithi/aws-rds-snapshot-deletion-lambda
```

2. Navigate to the root directory of the project
```bash
cd aws-rds-snapshot-deletion-lambda
```

3. Use the Makefile to build and deploy the project:
```bash
make deploy
```

This will provision the necessary resources in your AWS account:
- A Lambda function with Python code
- An IAM role with required policies
- An EventBridge rule with schedule expression
- A CloudWatch log group

## Parameters
You can customize the following parameters in the SAM template:
- `SnapshotNameContains` The Lambda function will only delete snapshots whose name contains this value. Default is "jenkins,instance-scheduler".
- `SnapshotAgeThreshold` The Lambda function will only delete snapshots that are older than this value (in days). Default is 30 days.
- `FunctionScheduleExpression` The schedule expression for the EventBridge rule that triggers the Lambda function. Default is cron(0 17 * * ? *) (00:00 UTC+7).
- `FunctionLogRetentionInDays` The number of days to retain CloudWatch logs for the Lambda function. Default is 30 days.

## Usage
After deploying, you can test the function by either creating a test event in the Lambda console, which will trigger the function immediately, or by waiting for the EventBridge rule to trigger the function automatically.

You can view the logs of the function by going to the CloudWatch Logs for the function's log group.

## Cleanup
```bash
make destroy
```
This will delete the CloudFormation stack and all associated resources.
