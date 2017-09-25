import logging
import boto3
import time


def handle(event, context):
	region = context.invoked_function_arn.split(":")[3]
	account = context.invoked_function_arn.split(":")[4]
	project = context.invoked_function_arn.split(":")[6].split("-")[1]

	print(region, account, project)

	logger = logging.getLogger(__name__)
	logger.info("check_ami_status: %r", event)

	sfn_client = boto3.client('stepfunctions')
	ec2_resource = boto3.resource('ec2')

	filters = [dict(Name='tag:Backup', Values=['yes','Yes','YEs','YeS','yES','yeS','YES'])]
	instances = sorted(
		ec2_resource.instances.filter(Filters=filters),
		key=lambda i: i.launch_time, reverse=True)
	for instance in instances:
		input_string = str({"InstanceId": instance.id}).replace('\'','"')
		logger.info("Starting state machine with input {}".format(input_string))
		sfn_client.start_execution(
			stateMachineArn="arn:aws:states:{}:{}:stateMachine:ec2backup-{}-core".format(region, account, project),
			input=input_string
		)
		time.sleep(0.1)
