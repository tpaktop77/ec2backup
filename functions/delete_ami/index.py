import logging
import boto3


def handle(event, context):
    logger = logging.getLogger(__name__)
    logger.info("delete_ami: %r", event)

    ec2_resource = boto3.resource('ec2')

    image = ec2_resource.Image(event['ImageId'])
    image.deregister()

    return event
