import boto3
import schedule

ec2_client=boto3.client("ec2",region_name="us-east-1")

def Backup_Volumes():
    volumes=ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'tag:env',
                'Values':['prod']
            }
        ]
    )
    for volume in volumes['Volumes']:
        try:
            new_snapshot=ec2_client.create_snapshot(
                VolumeId=volume['VolumeId']
            )
            print(new_snapshot)
        except:
            print("Can't create snapshot")

schedule.every().day.at("00:00").do(Backup_Volumes)
while True:
    schedule.run_pending()