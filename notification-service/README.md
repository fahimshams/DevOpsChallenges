# Canvas Course Notification Service

This project is a notification service that fetches course details from the Canvas API and publishes them to an AWS SNS topic. It is designed to help automate the process of retrieving course information and notifying users via SNS.

## Features

- Fetches a list of courses from the Canvas API.
- Retrieves detailed information for specific courses.
- Formats the course details.
- Publishes the formatted course details to an AWS SNS topic.

## Prerequisites

- Python 3.6+
- AWS account with SNS permissions
- Canvas API key

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/notification-service.git
    cd notification-service
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment:**

    - For Windows:
    
        ```bash
        .venv\Scripts\activate
        ```
    
    - For macOS/Linux:
    
        ```bash
        source .venv/bin/activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    CANVAS_DOMAIN=https://your_canvas_domain
    CANVAS_API_KEY=your_canvas_api_key
    SNS_TOPIC_ARN=your_sns_topic_arn
    ```

## Usage

1. **Run the notification service:**

    ```bash
    python src/notification_service.py
    ```

2. The service will fetch the course details from the Canvas API and publish them to the specified SNS topic.

## Code Overview

- [notification_service.py](http://_vscodecontentref_/0): Main script that contains the logic for fetching course details and publishing to SNS.

## Error Handling

The service includes error handling for network requests and SNS publishing. If an error occurs, it will be printed to the console.
