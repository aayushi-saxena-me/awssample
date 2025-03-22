import boto3
import json
from botocore.exceptions import ClientError


def set_bucket_write_access(bucket_name, principal_arn):
    """
    Set a bucket policy to allow write (PUT Object) access to a specific IAM user or role.
    
    :param bucket_name: str - Name of the S3 bucket to update
    :param principal_arn: str - The ARN of the IAM user or role to grant access
    """
    try:
        # Create an S3 client
        s3_client = boto3.client('s3')

        # Define the bucket policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": principal_arn
                    },
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        # Convert the policy to JSON
        bucket_policy_json = json.dumps(bucket_policy)

        # Set the bucket policy
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
        print(f"Bucket policy updated to allow write access for {principal_arn}.")

    except ClientError as e:
        print(f"Error setting bucket policy: {e}")


# Example Usage
if __name__ == "__main__":
    # Replace these with your bucket name and IAM principal ARNs
    bucket_name = "aayushi-home"  # Name of an existing bucket
    principal_arn = "arn:aws:iam::439784357699:root"  # Replace with the IAM user's ARN

    set_bucket_write_access(bucket_name, principal_arn)