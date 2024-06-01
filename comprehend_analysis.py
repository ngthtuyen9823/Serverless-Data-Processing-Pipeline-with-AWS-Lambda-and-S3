import boto3

def comprehend_analysis(text):
    # Create a Comprehend client using Boto3
    comprehend = boto3.client("comprehend")
    
    # Use Comprehend's detect_entities method to extract entities from the text
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    
    # Extract the 'Entities' field from the response
    entities = response['Entities']
    
    # Use Comprehend's detect_sentiment method to analyze the sentiment of the text
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    
    # Extract the 'Sentiment' field from the sentiment analysis response
    sentiment = sentiment_response['Sentiment']
    
    # Return the detected entities and sentiment
    return entities, sentiment