import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NotificationService:
    def __init__(self):
        self.canvas_domain = os.getenv('CANVAS_DOMAIN')
        self.api_key = os.getenv('CANVAS_API_TOKEN')

    def get_canvas_courses(self):
        """Get list of courses from Canvas API"""
        url = f"{self.canvas_domain}/api/v1/courses"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching courses: {response.text}")
            return None
        
    
    def get_specific_course_details(self, course_id, assignment_id):
        """Get details for a specific course"""
        url = f"{self.canvas_domain}/api/v1/courses/{course_id}/enrollments"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        print(f"Headers: {headers}")  # Debugging line

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching course details: {response.text}")
            return None



def main():
    notification_service = NotificationService()
    courses = notification_service.get_specific_course_details(2066, 81288)
    if courses:
        print(json.dumps(courses, indent=2))


if __name__ == '__main__':
    main()



