import boto3

def extract_text(bucketname, filename, extract_by="LINE") -> list:
    # Create a Textract client using Boto3
    textract = boto3.client("textract")
    
    # Call Textract's detect_document_text method to extract text from the document in S3
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucketname,
                "Name": filename,
            }
        }
    )
    
    # Initialize an empty list to store the extracted text
    text = []
    
    # Iterate through the detected blocks in the Textract response
    for block in response["Blocks"]:
        # Check if the block type matches the specified type to extract ("LINE" by default)
        if block["BlockType"] == extract_by:
            # Append the text of the block to the list
            text.append(block["Text"])
    
    # Return the list of extracted text
    return text