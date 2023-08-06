import boto3
import datetime
import os 
import pandas as pd
def list_users(aws_secret_access_key,aws_access_key_id,aws_session_token,region_name):
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
                print(user)
                userGroups = iam.list_groups_for_user(UserName=user['UserName'])
                for groupName in userGroups['Groups']:
                    try:
                        activity = user['PasswordLastUsed']
                        days = currentdate - activity
                        print(currentdate)
                        print(activity)
                        if days.days >= 5:
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
                    except KeyError:
                        activity = user['CreateDate']
                        days = currentdate - activity
                        print(currentdate)
                        print(activity)
                        if days.days >= 180:
                            result["username"].append(user['UserName'])
                            result["Userid"].append(user['UserId'])
                            result["arn"].append(user['Arn'])
                            result["days"].append(days)
                            result["groupName"].append(groupName['GroupName'])
            

        df = pd.DataFrame(result)
        df.to_csv ('report.csv', index = None)

list_users('ASIA54R2F7JLGCMU76A6','yAF/KVDGpGpEci7J2MWAcLWItwp2V4mxqB0I4Opx','IQoJb3JpZ2luX2VjEGIaCXVzLWVhc3QtMSJHMEUCIDk8KndUw0jycLRAXmspPADRQ2FsFOOAYlnEdHkXvXSfAiEAtArk/9imYiFg04nM5oXWx6wszaBI02mUunHF2s9UQrwqpQMIWhACGgw5NTQ2Nzg1MDgxMTgiDFLAmAU8Dq37U+HsMiqCA3Wjxsc/AsHf5AEcFeX+ENOt6oBk2FkYEK7cl2gYSw4WR9X9X5zsb15hv0a6EyjJcXty8wTobof+ulpURaRY/wFeVFno/vFlHgmZpv1iRMOdiUOQYtIcjcllUm1XmsoI4HX1HyF52ECH0DpntNAMypLr+cUtVp1wFls4TDfmCvwD9RhgW8lTSZpxc8p9ee6joF/HMNe7xDHj1MA7a/DtDFWu+tGGmjI+zKVvMG3yuTZyJgZT5vvG7rz/auvqUzfIevH5tpBRxZMtPVmg+thK4949SBun8vmI5Cnb/hSuZFeoG2bWvvd+D9U8yQKLQwkbS9ote0qdn2fezcKid6GCKRNhkCNREQHg0gAfrJnf9jnOxCdLC0IPgVwz1V091BGamhjQ5OVMI7A/hWzACj4XrOjYjGTxaSHqGZpBq3CkDSUF11qTuY7aX98vDuru4QW7hYJQfO+rQJ65iJ7LfT5urhB5LspnEvBrC1MTst6EdS8rfjTfAIl9CDpM+d0QtU+GQTqjMKLirZsGOqYBKD8VEmiAH6yEpkRnVKfC6ygnS+4XgImaLRqBLOkczJqgfcHsXRJf8GEmRkdSyUm9p6NMkGWU/8MkQ6mCB9ofljAwJZQrQ+A22vjUOFfjqg+yN7h9fOdbhnp0fCyKradmfUKCB3AtwA36RX/4PgnkxUE01o0rloJJxSo+RyftjpyiIaiERhrG+iRPoLMy36vMasQutM8jhHH+WE08Uk7zYb+O0mFvCQ==','us-east-1')

    