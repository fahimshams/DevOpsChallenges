import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

canvas_domain = os.getenv('CANVAS_DOMAIN')
api_key = os.getenv('CANVAS_API_KEY')

def get_canvas_courses():
        """Get list of courses from Canvas API"""
        url = f"{canvas_domain}/api/v1/courses"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching courses: {e}")
            return None
        
    
def get_specific_course_details(course_id):
        """Get details for a specific course"""
        url = f"{canvas_domain}/api/v1/courses/{course_id}/enrollments"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching courses: {e}")
            return None
        
def format_data(detail):
            user = detail['user']
            grades = detail['grades']['final_grade']
            return(f"User: {user['name']}, Grades: {grades}")

def lambda_handler(event, context):
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client('sns')
    courses = get_canvas_courses()
    messages = []
    if courses:
        for course in courses:
            if course.get('enrollment_term_id') == 212:
                course_id = course.get('id')
                course_details = get_specific_course_details(course_id)
                if course_details:
                    course_messages = [format_data(detail) for detail in course_details]
                    messages.append(f"\nCourse Name: {course['name']}\n------------------------------------------------")
                    messages.extend(course_messages)
                else:
                    messages.append("No course details found")
    else:
        messages.append("No courses found")
    
    message = "\n".join(messages)


    # Publish to SNS
    
    try:
        
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=messages,
            Subject='Canvas Course Grades'
        )
        print(f"Successfully published to SNS: {response}")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")   