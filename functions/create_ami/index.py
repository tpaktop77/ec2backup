import logging
import boto3
from datetime import datetime
from utils.utils import get_tag
import time


# For testing purpose please use { "InstanceId": "i-1538b0ed" }


def handle(event, context):
    logger = logging.getLogger(__name__)
    logger.info("create_ami: %r", event)

    event['StartTime'] = int(time.time())

    instance_id = event.get('InstanceId')
    if instance_id:
        success = False
        now = datetime.utcnow()
        ec2_client = boto3.client('ec2')
        ec2_resource = boto3.resource('ec2')

        instance = ec2_resource.Instance(instance_id)
        event['InstanceName'] = get_tag(instance.tags, 'Name')
        create_request = ec2_client.create_image(
            InstanceId=instance_id,
            Name="{}-{}-{}".format(
                event['InstanceName'],
                now.date(),
                int(time.time())
            ),
            Description="Automated backup by ec2backup/step/lambda/functions",
            NoReboot=True,
        )
        event['ImageId'] = create_request['ImageId']

        start = int(time.time())
        while not success and time.time() < (start + 15):
            try:
                image = ec2_resource.Image(event['ImageId'])
                image.create_tags(Tags=[dict(Key='amibackup', Value='true')])
                success = True
            except Exception as e:
                logger.exception(e)
                time.sleep(2)
    return event
