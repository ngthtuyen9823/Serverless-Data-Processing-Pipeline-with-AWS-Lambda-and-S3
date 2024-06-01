from PIL import Image
import logging
import uuid
import boto3

def process_image(bucketname, filename):
    # Create an S3 client using Boto3
    s3 = boto3.client("s3")
    
    # Generate unique paths for downloading and uploading the image
    download_path = f'/tmp/{uuid.uuid4()}{filename}'
    upload_path = f'/tmp/resized-{uuid.uuid4()}{filename}'

    # Download the original image from the specified S3 bucket
    s3.download_file(bucketname, filename, download_path)
    
    # Resize the downloaded image
    resize_image(download_path, upload_path)
    
    # Upload the resized image to a new S3 bucket
    resized_bucket = f'{bucketname}-resized'
    s3.upload_file(upload_path, resized_bucket, f'resized-{filename}')
    
    # Log information about the upload
    logging.info(f"Upload complete for file: resized-{filename} to bucket: {resized_bucket}")

def resize_image(image_path, resized_path):
    # Open the image using the PIL library
    with Image.open(image_path) as image:
        # Convert the image to the RGB color mode
        rgb_image = image.convert('RGB')
        
        # Resize the image to have a maximum width or height of half the original size
        # The 'thumbnail' method maintains the aspect ratio of the image
        rgb_image.thumbnail(tuple(x / 2 for x in rgb_image.size))
        
        # Save the resized image in JPEG format
        rgb_image.save(resized_path, 'JPEG')
