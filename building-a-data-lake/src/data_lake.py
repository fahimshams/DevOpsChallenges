import requests
import os
from dotenv import load_dotenv
import boto3
import json
import time

load_dotenv()

# AWS Configuration
bucket_name = "nfl-data-2025-1"
glue_database_name = "glue_nfl_data_lake"
athena_output_location = f"s3://{bucket_name}/athena_results"

api_key = os.getenv("API_KEY")
nfl_endpoint = os.getenv("NFL_ENDPOINT")


# AWS Clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')
athena_client = boto3.client('athena')


# Create s3 bucket

def create_s3_bucket(bucket_name):
        
        """Check if the bucket exists"""

        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f'Bucket {bucket_name} exists')
        except:
            print(f'Creating bucket {bucket_name}')

        """Create an S3 bucket"""

        try:
            # In us-east-1, no LocationConstraint is needed 
            s3_client.create_bucket(Bucket=bucket_name)

            print(f"Bucket {bucket_name} created successfully ")
        except Exception as e:
            print(f"Error creating bucket: {e}")

def convert_to_line_delimited_json(data):
    """Convert JSON to line-delimited JSON"""
    try:
        return "\n".join([json.dumps(record) for record in data])
    except Exception as e:
        print(f"Error converting to line-delimited JSON: {e}")
        return ""


def upload_data_to_s3(data):
    """Upload data to S3 bucket"""
    try:
        line_delimeted_data = convert_to_line_delimited_json(data)
        # define s3 object key
        file_key = "raw-data/nfl_player_data.json"

        # upload data to s3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimeted_data
            )

        print(f"Data uploaded to s3://{bucket_name}/{file_key}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


# Create a glue database
def create_glue_database(database_name):
    """Create a Glue database"""
    try:
        glue_client.create_database(
            DatabaseInput={
                'Name': database_name
            }
        )
        print(f"Database {database_name} created successfully")
    except Exception as e:
        print(f"Error creating database: {e}")


# Create a Glue table
def create_glue_table():
    """Create a Glue table"""

    try:
        glue_client.create_table(
            DatabaseName=glue_database_name,
            TableInput={
                'Name': 'nfl_player_data',
                'Description': 'NFL player data',
                'StorageDescriptor': {
                    'Columns': [
                        {
                            'Name': 'PlayerID',
                            'Type': 'int'
                        },
                        {
                            'Name': 'FirstName',
                            'Type': 'string'
                        },
                        {
                            'Name': 'LastName',
                            'Type': 'string'
                        },
                        {
                            'Name': 'Position',
                            'Type': 'string'
                        },
                        {
                            'Name': 'College',
                            'Type': 'string'
                        },
                        {
                            'Name': 'Height',
                            'Type': 'string'
                        },
                        {
                            'Name': 'Weight',
                            'Type': 'string'
                        },
                        {
                            'Name': 'BirthDate',
                            'Type': 'string'
                        }
                    ],
                    'Location': f"s3://{bucket_name}/raw-data/",
                    'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                    'Compressed': False,
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.openx.data.jsonserde.JsonSerDe'
                    }
                },
                'TableType': 'EXTERNAL_TABLE'
            }
        )
        print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
        
def configure_athena():
    """Setup Athena output location"""
    try:
        athena_client.start_query_execution(
            QueryString="CREATE DATABASE IF NOT EXISTS nfl_analytics",
            QueryExecutionContext={
                'Database': glue_database_name
            },
            ResultConfiguration={
                'OutputLocation': athena_output_location
            }
        )
        print("Athena output location configured successfully")
    except Exception as e:
        print(f"Error configuring Athena: {e}")


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
    

def main():

    print("Setting up data lake for nfl analytics")

    # Fetch NFL data
    nfl_data = get_nba_data()


    # Create S3 bucket
    create_s3_bucket(bucket_name)
    time.sleep(5) # wait for bucket to be created
    
    # Upload data to S3
    upload_data_to_s3(nfl_data)
    
    # Create Glue database
    create_glue_database(glue_database_name)
    
    # Create Glue table
    create_glue_table()
    
    # Configure Athena
    configure_athena()
    
    print("Data lake setup completed")


if __name__ == "__main__":
        main()


