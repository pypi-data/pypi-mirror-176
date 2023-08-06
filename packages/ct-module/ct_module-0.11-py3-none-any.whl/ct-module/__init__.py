class utility:
    def __init__(self):
        print("constructor created")

    
    def list_users(self,aws_secret_access_key,aws_access_key_id,aws_session_token,region_name):
        global aws_env, report_file_location
        aws_envs_list = AWS_ENVS.split(';')
        iam_users_list = iam_usernames.split(',')

        report_file_location = dir_path + "/" + aws_env +  report_file_name
        session = boto3.session.Session(
        aws_access_key_id=aws_secret_access_key,
        aws_secret_access_key=aws_access_key_id,
        aws_session_token=aws_session_token,
        region_name=region_name
        )
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
                        if days.days >= int(os.environ['RD_OPTION_ENV_DAY']):
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
                    except KeyError:
                        activity = user['CreateDate']
                        days = currentdate - activity
                        if days.days >= int(os.environ['RD_OPTION_ENV_DAY']):
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
            

        df = pd.DataFrame(result)
        df.to_csv (report_file_location, index = None)
