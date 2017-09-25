import logging
import boto3
from datetime import datetime
import time

DAILY_TO_KEEP = 7
WEEKLY_TO_KEEP = 7


def handle(event, context):
    logger = logging.getLogger(__name__)
    logger.info("cleam_ami_images: %r", event)

    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    event['ami_clean_fails'] = 0
    event['ami_cleans'] = 0

    filters = [
        dict(Name='state', Values=['available']),
        dict(Name='name', Values=['{}-*'.format(event['InstanceName'])])
    ]
    images = list(ec2_resource.images.filter(Filters=filters))
    weekly_to_keep = []
    current_week = datetime.utcnow().isocalendar()[1]

    daily_to_purge = sorted(images, key=lambda x: x.creation_date, reverse=True)[DAILY_TO_KEEP:]

    for image in daily_to_purge:
        image_week = datetime.strptime(image.creation_date, '%Y-%m-%dT%H:%M:%S.%fZ').isocalendar()[1]
        if image_week != current_week:
            weekly_to_keep.append(image)
            current_week = image_week
        if len(weekly_to_keep) >= WEEKLY_TO_KEEP:
            break

    purgeable = [i for i in daily_to_purge if i not in weekly_to_keep]
    logger.info("purgeable: {}".format(str(purgeable)))
    if len(purgeable) > 0:
        for image in purgeable:
            try:
                ec2_client.deregister_image(ImageId=image.id)
                event['ami_cleans'] += 1
            except Exception as e:
                logger.warning(e.message)
                event['ami_clean_fails'] += 1

    return event
