import boto3

ec2_client_1=boto3.client("ec2",region_name="us-east-1")
ec2_resource_1=boto3.resource("ec2",region_name="us-east-1")
ec2_client_2=boto3.client("ec2",region_name="us-east-2")
ec2_resource_2=boto3.resource("ec2",region_name="us-east-2")
instances_Ids=[]

Reservations=ec2_client_1.describe_instances()['Reservations']
for Reservation in  Reservations :
    instances=Reservation['Instances']
    for  instance in  instances:
        instances_Ids.append(instance['InstanceId'])

response = ec2_resource_1.create_tags(
    Resources=instances_Ids,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

instances_Ids=[]

Reservations=ec2_client_2.describe_instances()['Reservations']
for Reservation in  Reservations :
    instances=Reservation['Instances']
    for  instance in  instances:
        instances_Ids.append(instance['InstanceId'])

response = ec2_resource_2.create_tags(
    Resources=instances_Ids,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)