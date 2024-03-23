import boto3
from operator import itemgetter
import schedule
import datetime

ec2_client=boto3.client("ec2",region_name="us-east-1")

volumes=ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'tag:env',
                'Values':['prod']
            }
        ]
    )
def cleanup_older_snapshots():
    for volume in volumes['Volumes']:
        snapshots=ec2_client.describe_snapshots(
            OwnerIds=['self'],
        Filters = [
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
        )

        sorted_snapshots=sorted(snapshots['Snapshots'],key=itemgetter('StartTime'),reverse=True) #sort snapshot by starttime

        for snap in sorted_snapshots[2:]:
            try:
                response=ec2_client.delete_snapshot(
                    SnapshotId=snap['SnapshotId']
                )
                print(response)
            except:
                print("Can't delete snapshots")


def run_monthly_task():
    today = datetime.datetime.now()
    if today.day == 1:  # Check if it's the first day of the month
        cleanup_older_snapshots()

# Schedule the task to run every day
schedule.every().day.do(run_monthly_task)


while True:
    schedule.run_pending()