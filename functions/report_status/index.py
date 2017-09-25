import logging
import boto3
import time


def handle(event, context):
    logger = logging.getLogger(__name__)
    logger.info("report_status: %r", event)

    timestamp = int(time.time())
    if event['ami_status'] == 'failed':
        post_metric(event, timestamp, 1, 'count', 'ec2backup.failed')
        post_metric(event, timestamp, event['InstanceName'], 'gauge', 'ec2backup.images.failed')
        logger.info("ami_status: failed reported to datadog")
    if event['ami_status'] == 'available':
        post_metric(event, timestamp, 1, 'count', 'ec2backup.available')
        logger.info("ami_status: available reported to datadog")
    if 'ami_cleans' in event and event['ami_cleans'] > 0:
        post_metric(event, timestamp, event['ami_cleans'], 'count', 'ec2backup.cleans')
    if 'ami_clean_fails' in event and event['ami_clean_fails'] > 0:
        post_metric(event, timestamp, event['ami_clean_fails'], 'count', 'ec2backup.cleanfails')

    return event


def post_metric(event, timestamp, value, type, name, tags=None):
    if not tags:
        tags = [
            'InstanceName:{}'.format(event['InstanceName']),
            'InstanceId:{}'.format(event['InstanceId'])
        ]
    print('MONITORING|{0}|{1}|{2}|{3}|#{4}'.format(
        timestamp,
        value,
        type,
        name,
        ','.join(tags)
    ))
