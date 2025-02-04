import requests
import os
from dotenv import load_dotenv
import boto3
import json
import time

load_dotenv()

api_key = os.getenv("API_KEY")
nfl_endpoint = os.getenv("NFL_ENDPOINT")

# AWS Clients

s3_client = boto3.client('s3')



def create_s3_bucket(bucket_name):
        """Create an S3 bucket"""
        try:

            # Create the bucket
                # In us-east-1, no LocationConstraint is needed
            # s3_client.create_bucket(Bucket=bucket_name)
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Successfully created bucket {bucket_name}")
            print(f"Bucket {bucket_name} exists")

            print(f"Bucket {bucket_name} created successfully in ")
        except Exception as e:
            print(f"Error creating bucket: {e}")


def get_nba_data():
    """Fetch NFL data from the API"""
    try:
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }
        response = requests.get(nfl_endpoint, headers=headers)
        if response.status_code == 200:
            print("NFL data fetched successfully")
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"Error fetching NFL data: {e}")
        return []


# Create the S3 bucket
create_s3_bucket("nfl-data-2025-1")


