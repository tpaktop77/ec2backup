# ec2backup
Very simple and effective service for EC2 backups. Based on AWS Step and Lambda functions.
 Permissions and Events to call it must be created manually.

It consists of:
    ./functions/ - Lamda functions
    ./state_machines/ - Step functions
    ./utils/ - utils
    
Also this service posting log messages in Datadog format.
If you are using Datadog you will have metrics that could be used to monitor backups.
