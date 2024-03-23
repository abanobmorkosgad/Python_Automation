import boto3
import schedule
import datetime

ec2_client = boto3.client("ec2", region_name="us-east-1")
ec2_resource = boto3.resource("ec2", region_name="us-east-1")


def check_instance_status():
    status_checks = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    print(datetime.datetime.today())
    for status_check in status_checks['InstanceStatuses']:
        instance_state = status_check['InstanceState']['Name']
        instance_status = status_check['InstanceStatus'].get('Status')
        system_status = status_check['SystemStatus'].get('Status')
        print(
            f"instance {status_check['InstanceId']} is {instance_state} with instance status: {instance_status} and system status: {system_status}")
    print("\n")

schedule.every(5).seconds.do(check_instance_status)
# schedule.every().hour.do(check_instance_status)
# schedule.every().day.at("10:30").do(check_instance_status)
while True:
    schedule.run_pending()

