import logging
import boto3
import time

PENDING_TIMEOUT = 60*60*10

def handle(event, context):
    logger = logging.getLogger(__name__)
    logger.info("check_ami_status: %r", event)

    ec2_resource = boto3.resource('ec2')
    image = ec2_resource.Image(event['ImageId'])
    event['ami_status'] = image.state

    if image.state != 'available':
        if int(time.time()) > (event['StartTime'] + (PENDING_TIMEOUT)):
            event['ami_status'] = 'failed'

    return event
