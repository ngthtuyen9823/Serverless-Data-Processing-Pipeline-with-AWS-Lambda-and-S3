import boto3
import logging
import json
import uuid
import os
from urllib.parse import unquote_plus

from my_module.comprehend_analysis import comprehend_analysis
from my_module.process_error import process_error
from my_module.extract_text import extract_text
from my_module.process_image import resize_image, process_image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    try:
        if "Records" in event:
            # Extract information about the uploaded file from the S3 event
            file_obj = event["Records"][0]
            bucketname = str(file_obj["s3"]["bucket"]["name"])
            filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))

            logging.info(f"Processing file: {filename} from bucket: {bucketname}")

            # Check the file extension of the uploaded file
            file_extension = os.path.splitext(filename)[1].lower()
            
            # If the file is not a text file or unsupported file type, perform text analysis
            if file_extension in {'.pdf', '.png', '.jpeg', '.jpg'}:
                # Extract text from the image using the custom 'extract_text' function
                raw_text = extract_text(bucketname, filename, extract_by="LINE")
                logging.info(raw_text)

                # If text is detected, call AWS Comprehend for text analysis
                if raw_text:
                    entities, sentiment = comprehend_analysis("\n".join(raw_text))
                    logging.info(f"Entities: {entities}")
                    logging.info(f"Sentiment: {sentiment}")

                    # Save results to S3
                    output_body = "\n".join(raw_text + [f"Entities: {entities}", f"Sentiment: {sentiment}"])
                    output_key = f"output/{filename.split('/')[-1]}_{uuid.uuid4().hex}.txt"
                    s3.put_object(
                        Bucket=f'{bucketname}-resized',
                        Key=output_key,
                        Body=output_body,
                    )
                else:
                    logging.info("No text detected in the image. Skipping text analysis.")
            else:
                logging.info("Unsupported file type for text analysis.")
                
            # If the file is an image, process it directly
            if file_extension in {'.png', '.jpeg', '.jpg'}:
                process_image(bucketname, filename)
                
            return {
                    "statusCode": 200,
                    "body": json.dumps("Action processed successfully!"),
            }

    except Exception as e:
        # Capture and log any exceptions that occur during processing
        error_msg = process_error()
        logger.error(error_msg)
        return {"statusCode": 500, "body": json.dumps(f"Error processing the document: {str(e)}")}

    return {"statusCode": 500, "body": json.dumps("Unexpected error occurred!")}