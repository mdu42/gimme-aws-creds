import json
import os
from gimme_aws_creds.ui import CLIUserInterface
from gimme_aws_creds.main import GimmeAWSCreds

def lambda_handler(event, context):
    try:
        cli = CLIUserInterface(argv=[
            'mycommand', '-t', '--profile', 'DEFAULT', '-u', event['username'], '-x', event['password']
            ])
        response = GimmeAWSCreds(ui=cli).run()
        if response['SAMLResponse'] is not None:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'Role': 'arn:aws:iam::000000000000:role/MyUserS3AccessRole', # The user will be authenticated if and only if the Role field is not blank
                    'Policy': '', # Optional JSON blob to further restrict this user's permissions
                    'HomeDirectory': '/' # Not required, defaults to '/'
                })
            }
        # Return HTTP status 200 but with no role in the response to indicate authentication failure
        return {
            'statusCode': 200,
            'body': json.dumps({})
        }

    except Exception:
        # Return HTTP status 200 but with no role in the response to indicate authentication failure
        return {
            'statusCode': 200,
            'body': json.dumps({})
        }

def main():
    event = {
        'username': 'my_user',
        'password': 'test'
    }
    print(lambda_handler(event, {}))

if __name__ == "__main__": main()