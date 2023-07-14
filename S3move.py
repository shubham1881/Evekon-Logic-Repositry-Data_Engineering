import boto3

def move_files(source_bucket, source_prefix, destination_bucket, destination_prefix):
    # Create a Boto3 S3 client with explicit credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id='your access key',
        aws_secret_access_key='your secret access key'
    )

    # List objects in the source directory
    response = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)

    # Iterate over the objects and move them
    for obj in response['Contents']:
        # Construct the new key by replacing the source prefix with the destination prefix
        new_key = obj['Key'].replace(source_prefix, destination_prefix, 1)

        # Copy the object to the destination bucket with the new key
        s3.copy_object(
            Bucket=destination_bucket,
            Key=new_key,
            CopySource={'Bucket': source_bucket, 'Key': obj['Key']}
        )

        # Delete the object from the source bucket
        s3.delete_object(Bucket=source_bucket, Key=obj['Key'])

# Usage example
source_bucket = 'new-evekon'
source_prefix = 'gmail_input/algo_check/'
destination_bucket = 'new-evekon'
destination_prefix = 'gmail_input/first_new/'

move_files(source_bucket, source_prefix, destination_bucket, destination_prefix)
