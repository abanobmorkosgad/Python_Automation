import boto3

ec2_client=boto3.client("ec2",region_name="us-east-1")
ec2_resource=boto3.resource("ec2",region_name="us-east-1")

print("\nEC2's Info:")
Reservations=ec2_client.describe_instances()['Reservations']
for Reservation in  Reservations :
    instances=Reservation['Instances']
    for  instance in  instances:
        print(f"instance: {instance['Tags'][0]['Value']} of id: {instance['InstanceId']} and IP: {instance.get('PublicIpAddress')} --> {instance['State']['Name']}")

print("\nStatus Checks:")

status_checks=ec2_client.describe_instance_status()
for status_check in status_checks['InstanceStatuses']:
    instance_state=status_check['InstanceState']['Name']
    instance_status=status_check['InstanceStatus'].get('Status')
    system_status=status_check['SystemStatus'].get('Status')
    print(f"instance {status_check['InstanceId']} is {instance_state} with instance status: {instance_status} and system status: {system_status}")
    # print(instance_status)
