import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upload_to_s3(file_name, bucket_name, object_name=None):
    """
    Upload a file to an S3 bucket.

    :param file_name: str - The file to upload
    :param bucket_name: str - The name of the S3 bucket
    :param object_name: str (optional) - S3 object name. If not specified, file_name is used.
    :return: True if file was uploaded, else False
    """
    # If S3 object_name not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Upload the file to the bucket
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name} as {object_name}.")
        return True
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


# Usage example
if __name__ == "__main__":
    local_file_name = "example.txt"
    target_bucket_name = "your-s3-bucket-name"  # Replace with your S3 bucket name
    target_object_name = "folder1/example.txt"  # Optional: specify path inside the bucket

    # Call the function to upload the file
    upload_success = upload_to_s3(local_file_name, target_bucket_name, target_object_name)
    if upload_success:
        print("Upload completed.")
    else:
        print("Upload failed.")