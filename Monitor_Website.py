import time
import requests
import smtplib
import paramiko
import os
import boto3
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def check(msg):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)


def restart_server():
    print("Rebooting the Server...")
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    instance_id = 'i-0af1c548d798cf672'
    response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    time.sleep(60)


def restart_container():
    print("Restarting the App...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='54.224.48.240', username="ubuntu", key_filename="C:\\Users\\Kimo Store\\Downloads\\Test.pem")
    stdin, stdout, stderr = ssh.exec_command("sudo docker start nginx")
    print(stdout.readlines())
    ssh.close()
    print('App Restarted')


def monitor_app():
    try:
        response = requests.get("http://54.224.48.240:8080/")
        if response.status_code != 200:
            print("App Down!!")
            msg = f"Subject: SITE DOWN\nApp returned {response.status_code}"
            check(msg)
            restart_container()

        else:
            print("App is Running!")
    except Exception as ex:
        print(f'Connection error happened,{ex}')
        msg = "Subject: SITE DOWN\nApp not accessible"
        check(msg)
        restart_server()
        restart_container()


schedule.every(5).seconds.do(monitor_app)

while True:
    schedule.run_pending()
