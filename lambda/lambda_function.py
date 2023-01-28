import boto3
import botocore
import logging
import os
import pytz
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_rds_snapshots(rds_client):
    """
    Get all manual RDS snapshots using the provided RDS client.
    :param rds_client: boto3 RDS client
    :return: list of RDS snapshots
    """
    response = rds_client.describe_db_snapshots(SnapshotType='manual')
    snapshots = response['DBSnapshots']
    while 'Marker' in response:
        response = rds_client.describe_db_snapshots(
            Marker=response['Marker'],
            SnapshotType='manual'
        )
        snapshots.extend(response['DBSnapshots'])
    return snapshots


def delete_rds_snapshot(rds_client, snapshot_id):
    """
    Delete an RDS snapshot using the provided RDS client.
    :param rds_client: boto3 RDS client
    :param snapshot_id: string, snapshot identifier
    :return: string message indicating success or failure
    """
    try:
        response = rds_client.delete_db_snapshot(
            DBSnapshotIdentifier=snapshot_id
        )
        return f'Deleted "{snapshot_id}" is successfully.'
    except botocore.exceptions.ClientError as err:
        return f'Failed to delete "{snapshot_id}" ({str(err)}).'


def lambda_handler(event, context):
    """
    AWS Lambda function that finds and deletes RDS snapshots that have:
    - Name contains "xxx" or "yyy" or something
    - Age more than X days
    :param event: AWS Lambda event
    :param context: AWS Lambda context
    :return: None
    """
    name_contains = [name.strip() for name in os.environ.get('SNAPSHOT_NAME_CONTAINS').split(',')]
    age_threshold = int(os.environ.get('SNAPSHOT_AGE_THRESHOLD'))
    rds_client = boto3.client('rds')
    snapshots = get_rds_snapshots(rds_client)
    now = datetime.now(pytz.utc)
    count = 0
    for snapshot in snapshots:
        if any(x in snapshot['DBSnapshotIdentifier'] for x in name_contains):
            age = (now - snapshot['SnapshotCreateTime']).days
            if age > age_threshold:
                logger.info(f'Snapshot age of "{snapshot["DBSnapshotIdentifier"]}" ({age} days) more than threshold ({age_threshold} days), deleting...')
                result = delete_rds_snapshot(rds_client, snapshot['DBSnapshotIdentifier'])
                if 'Deleted' in result:
                    logger.info(result)
                else:
                    logger.error(result)
                count += 1
    if count == 0:
        logger.info('Not found any snapshots to delete.')
