import time
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def check_and_create_s3_bucket(bucket_name, region=None):
    """
    Check if you have access to an S3 bucket, and create it if not found.

    :param bucket_name: str - The name of the S3 bucket
    :param region: str - AWS region to create the bucket in (if it doesn't exist)
    :return: True if access is verified or bucket is created, else False
    """
    # Create an S3 client
    s3_client = boto3.client('s3', region_name=region)

    try:
        # Attempt to list objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        if 'Contents' in response:
            print(f"Access verified. Bucket '{bucket_name}' contains objects.")
        else:
            print(f"Access verified. Bucket '{bucket_name}' is empty.")
        return True
    except NoCredentialsError:
        print("No credentials provided or available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except ClientError as e:
        # Handle specific errors such as Access Denied (403) or Bucket Not Found (404)
        error_code = e.response['Error']['Code']
        print(error_code)
        if error_code == "403":
            print(f"Access denied to bucket '{bucket_name}'.")
        elif error_code == "NoSuchBucket":
            print(f"Bucket '{bucket_name}' not found. Attempting to create it...")
            try:
                create_bucket_params = {"Bucket": bucket_name}
                # If a region is specified, include it in the request

                s3_client.create_bucket(**create_bucket_params)
                print(f"Bucket '{bucket_name}' created successfully.")

                # Add a delay to allow bucket propagation
                time.sleep(5)  # 5-second delay

                # Verify bucket creation by listing buckets
                bucket_list = s3_client.list_buckets()
                bucket_names = [bucket["Name"] for bucket in bucket_list["Buckets"]]  # Get bucket names
                if bucket_name in bucket_names:
                    print(f"Bucket '{bucket_name}' is now available.")
                    return True
                else:
                    print(f"Bucket '{bucket_name}' creation failed to propagate.")
                    return False
            except Exception as create_error:
                print(f"Failed to create bucket '{bucket_name}': {create_error}")
        else:
            print(f"An unexpected error occurred: {e}{error_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


# Usage example
if __name__ == "__main__":
    bucket_name_to_check = "aayushi-home"  # Replace with your S3 bucket name
    aws_region = "us-east-1"  # Replace with the correct AWS region

    # Call the function to check access and create the bucket if it doesn't exist
    has_access = check_and_create_s3_bucket(bucket_name_to_check, region=aws_region)
    if has_access:
        print("S3 access is verified or bucket is created.")
    else:
        print("Failed to verify S3 access or create the bucket.")