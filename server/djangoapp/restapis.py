# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import logging

import requests 

# Get an instance of a logger
logger = logging.getLogger(__name__)

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        result = response.json()
        print(f"Response from {request_url}: {result}")
        return result
    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")
        return []

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url, timeout=1)  # Add a short timeout
        return response.json()
    except Exception as err:
        # Just log to debug level rather than printing to console
        logger.debug(f"Sentiment analysis service unavailable")
        
        # Simple keyword-based sentiment analysis as fallback
        text_lower = text.lower()
        
        # Positive keywords
        positive_words = ['happy', 'great', 'excellent', 'good', 'best', 'amazing', 'love', 
                         'wonderful', 'fantastic', 'dream', 'perfect', 'awesome']
        # Negative keywords
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'poor', 'disappointing', 
                         'hate', 'horrible', 'unfortunate', 'mediocre', 'regret']
        
        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Determine sentiment based on word counts
        if positive_count > negative_count:
            return {"sentiment": "positive"}
        elif negative_count > positive_count:
            return {"sentiment": "negative"}
        else:
            return {"sentiment": "neutral"}

def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
