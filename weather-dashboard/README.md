# WeatherDashboard

WeatherDashboard is a Python-based application that fetches real-time weather data for multiple cities using the OpenWeather API and stores the data as JSON files in an Amazon S3 bucket. 
This project demonstrates how to integrate external APIs, process data, and interact with AWS services.

## Features

- Fetches weather data, including temperature, humidity, and conditions, for a list of cities.
- Automatically creates an S3 bucket if it does not already exist.
- Saves weather data in JSON format with timestamped filenames for historical tracking.
- Logs weather details and actions for monitoring and debugging.

## Prerequisites

1. **Python 3.8 or higher**: Make sure you have Python installed. [Download Python](https://www.python.org/downloads/)
2. **AWS Account**: Required to use Amazon S3.
3. **OpenWeather API Key**: Sign up and get your API key from the [OpenWeather website](https://openweathermap.org/api).
4. **AWS CLI configured**: Ensure AWS CLI is installed and configured with credentials. [Set up AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/DevOpsChallanges.git
   cd DevOpsChallenges
   cd weather-dashboard

2. Create a virtual environment and activate it:
   ```bash
  python3 -m venv venv
  source venv/bin/activate  # For Linux/Mac
  venv\Scripts\activate     # For Windows

3. Install the required dependencies
   ```bash
   pip install -r requirements.txt

4. Set up environment variables
   ```bash
   OPENWEATHER_API_KEY=your_openweather_api_key
   AWS_BUCKET_NAME=your_s3_bucket_name

5. Run the application
   ```bash
   python weather_dashboard.py
