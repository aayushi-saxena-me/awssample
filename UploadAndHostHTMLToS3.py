import boto3
from botocore.exceptions import ClientError


def upload_file_to_s3(bucket_name, file_name, region="us-east-1"):
    """
    Upload an HTML file to an S3 bucket, enable static website hosting, and 
    make the file public.

    :param bucket_name: str - The name of the S3 bucket
    :param file_name: str - The path to the HTML file to upload
    :param region: str - The AWS region for the S3 bucket
    :return: str - The URL of the hosted website
    """
    try:
        # Create an S3 client
        s3_client = boto3.client('s3', region_name=region)

        # Create the S3 bucket
        try:
            if region == "us-east-1":
                # In us-east-1 region, LocationConstraint is not needed
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Bucket '{bucket_name}' created successfully.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                print(f"Bucket '{bucket_name}' already exists and is owned by you.")
            else:
                print(f"Error creating bucket: {e}")
                return None

        # Upload the HTML file to the bucket
        s3_client.upload_file(file_name, bucket_name, "index.html", ExtraArgs={'ContentType': "text/html"})
        print(f"File '{file_name}' uploaded as 'index.html'.")

        # Enable public read permissions for the object
        s3_client.put_object_acl(ACL="public-read", Bucket=bucket_name, Key="index.html")
        print(f"Made 'index.html' publicly readable.")

        # Enable static website hosting
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
            },
        )
        print(f"Static website hosting enabled for bucket '{bucket_name}'.")

        # Generate the website URL
        website_url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
        print(f"Website URL: {website_url}")

        return website_url

    except ClientError as e:
        print(f"Error: {e}")
        return None


# Example - Usage
if __name__ == "__main__":
    # Replace these values with your information
    bucket_name = "aayushi-home"  # A unique bucket name
    html_file = "helloWorld.html"  # HTML file to upload
    aws_region = "us-east-1"  # AWS region for your bucket (e.g., "ap-south-1")

    # Call the function to upload and host the file
    website = upload_file_to_s3(bucket_name, html_file, region=aws_region)
    if website:
        print(f"Your website is live at: {website}")