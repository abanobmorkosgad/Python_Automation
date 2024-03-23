import boto3
from operator import itemgetter

ec2_client=boto3.client("ec2",region_name="us-east-1")
ec2_resource=boto3.resource("ec2",region_name="us-east-1")

instance_id="i-0b80517c500fea064"
volumes=ec2_client.describe_volumes(
        Filters=[
            {
                'Name':'attachment.instance-id',
                'Values':[instance_id]
            }
        ]
    )
instance_volume=volumes['Volumes'][0]

snapshots=ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters = [
            {
                'Name': 'volume-id',
                'Values': [instance_volume['VolumeId']]
            }
        ]
        )
sorted_snapshots=sorted(snapshots['Snapshots'],key=itemgetter('StartTime'),reverse=True) #sort snapshot by starttime
latest_snapshot=sorted_snapshots[0]

volume=ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone= 'us-east-1a',
    TagSpecifications = [
                        {
                            'ResourceType':'volume',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'prod'
                                }
                            ]
                        }
        ]
)

while True:  #while loop to wait till volume available
    vol = ec2_resource.Volume(volume['VolumeId'])
    if vol.state == "available":
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=volume['VolumeId'],
            Device='/dev/xvdc'
        )
        break
