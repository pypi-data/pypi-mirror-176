import boto3
import datetime
import os 
import pandas as pd
import csv
class utility:

    def __init__(self):
        print("constructor created")


    def boto_session(self,aws_secret_access_key,aws_access_key_id,aws_session_token,region_name):
        global session
        global region
        session = boto3.session.Session(
        aws_access_key_id=aws_secret_access_key,
        aws_secret_access_key=aws_access_key_id,
        aws_session_token=aws_session_token,
        region_name=region_name
        )
        print("Boto3 Session Started")
        return session

    def list_users(self,day):
        iam = session.client(
        service_name='iam'
        )

        paginator = iam.get_paginator('list_users')
        tz = datetime.datetime.now().astimezone().tzinfo
        currentdate = datetime.datetime.now(tz)
        result = {"username":[],"Userid":[],"arn":[],"days":[],"groupName":[]}

        for response in paginator.paginate():
            for user in response["Users"]:
                userGroups = iam.list_groups_for_user(UserName=user['UserName'])
                for groupName in userGroups['Groups']:
                    try:
                        activity = user['PasswordLastUsed']
                        days = currentdate - activity
                        if days.days >= day:
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
                    except KeyError:
                        activity = user['CreateDate']
                        days = currentdate - activity
                        if days.days >= day:
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
            

        df = pd.DataFrame(result)
        df.to_csv ('_iam_userlist.csv', index = None)

    def ebs_volume_report(self):

        ec2_client = session.client('ec2')

        paginator = ec2_client.get_paginator('describe_volumes')

        response_iterator = paginator.paginate()
        header = ['InstanceId','VolumeID', 'Size(GB)', 'Availability Zone','Volume Type','Status','IOPS']
        with open('ebs_report.csv','w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for page in response_iterator:
                cnt = 1
                for  volume in page['Volumes']:

                    print(cnt)
                    for att in volume['Attachments']:
                        print('Instance ID =', att['InstanceId'])
                        inst = att['InstanceId']
                        print('Volume ID = ', volume['VolumeId']) 
                        print('Volume Size =' , volume['Size'],"GB")
                        print("AvailabilityZone = ", volume['AvailabilityZone'])
                        print("Volume Type = ", volume['VolumeType'])
                        print("Volume Status =", volume['State'])
                            #print("IOPS =", volume['Iops'])
                        print("--------")
                        cnt = cnt + 1
                        data = [inst,volume['VolumeId'],volume['Size'],volume['AvailabilityZone'],volume['VolumeType'],volume['State'],volume['Iops']]

            writer.writerow(data)


    def keys_lsit(self):

        iam = session.client(
        service_name='iam'
        )

        KEY = 'LastUsedDate'

        for user in resource.users.all():
            Metadata = client.list_access_keys(UserName=user.user_name)
            if Metadata['AccessKeyMetadata'] :
                for key in user.access_keys.all():
                    AccessId = key.access_key_id
                    Status = key.status
                    LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)
                    if (Status == "Active"):
                        if KEY in LastUsed['AccessKeyLastUsed']:
                            print("User: " , user.user_name ,  "Key: " , AccessId , "AK Last Used: " , LastUsed['AccessKeyLastUsed'][KEY])
                        else:
                            print("User: ", user.user_name  , "Key: ",  AccessId , "Key is Active but NEVER USED")
                    else:
                        print("User: ", user.user_name  , "Key: ",  AccessId , "Keys is InActive")
            else:
                print ("User: ", user.user_name  , "No KEYS for this USER")     #".. proof: " , Metadata
