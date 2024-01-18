# PitchPulse

Analyze the buzz around EPL players during match days!

## Overview

PitchPulse is an in-progress Python-based tool designed to track mentions of EPL soccer players in match threads on their subreddits. Utilizing a serverless architecture, the application employs AWS RDS for database management, AWS Lambda functions for processing, AWS EventBridge for event orchestration, and AWS ECS for containerized deployment. This setup allows PitchPulse to efficiently scale and handle multiple games simultaneously, providing real-time insights into player mentions during matches.

## Reddit Background
During soccer games, forums host live match threads that are flooded with user comments about the ongoing game. Many of these mention the player such as "Salah looks great today!". The basis of this project is to collect, count, and plot these mentions over time to visualize how player popularity/notoriety changes over the course of the game. 

## Serverless Architecture

- **AWS RDS**: Hosts the application database, providing scalability and reliability.
- **AWS Lambda**: Processes data and handles backend logic in a scalable, event-driven manner.
- **AWS EventBridge**: Manages event triggers for Lambda functions, ensuring timely execution of tasks.
- **AWS ECS**: Runs containerized applications, allowing for isolated environments and consistent deployment.

## Features

- **Real-time Tracking**: Monitors Reddit match threads for player mentions.
- **Serverless Backend**: Leverages AWS services for scalable, efficient processing.
- **Visual Analysis**: Generates plots using Matplotlib for real-time data visualization.
- **Dynamic Configuration**: Easily configurable player lists and nicknames.

## Prerequisites

- AWS Account with configured services (RDS, Lambda, EventBridge, ECS)
- Python 3.9
- PRAW (Reddit API library)
- Matplotlib
- Boto3 (AWS SDK)
- PySql
- SQLAlchemy
- Flask

## Setup & Installation

1. Clone the repository.
2. Navigate to the project directory and install dependencies: `pip install -r requirements.txt`
3. Configure AWS services:
   - Set up RDS for the database.
   - Deploy Lambda functions.
   - Configure EventBridge rules.
   - Set up ECS tasks for containerized deployment.
4. Set Reddit API credentials in Lambda environment variables or AWS Secrets Manager.
5. Run the ECS tasks or trigger the Lambda functions as required.

## How it Works
- **Scheduling**: Lambda function (schedule_match.py) set to check daily for matches with Football API and store next match in database. Another lambda function (setup_match_EventBridge.py) then uses AWS SDK to schedule the execution lambda (execute_match_tracker.py) function in EventBridge.
- **Data Collection**: ECS used to execute task based on docker container in repo repo, which is the Flask app contained in the ecs_tasks folder. When triggered by a lambda function set in EventBridge it scrapes Reddit match threads.
- **Data Processing**: Mentions are processed and stored in the AWS RDS database.
- **Visualization**: Data is retrieved and plotted in real-time using Matplotlib, facilitated by ECS tasks.

## Limitations and Considerations

- **Reddit API Rate Limits:** Reddit imposes rate limits on how often you can make requests. This is more of an issue for when the script tries to fetch comments from particularly active threads. The use of the PRAW library helps in respecting these limits by handling potential rate-limit errors and waiting as required.

- **Comment Fetching Limitations:** Due to the nature of the Reddit API and PRAW, there are constraints on the number of comments that can be fetched at once. To mitigate this, the tracker fetches comments in chunks, ensuring that it captures as many relevant comments as possible within the constraints by sorting by timeframe. This might occasionally mean that some comments are missed during peak activity periods, but for most match threads, the data should be representative.

- **Time Sensitivity:** PitchPulse is designed to analyze match threads in real-time. While it can be used post-match, its primary utility is during live matches where it continually polls for new comments and updates the analysis.

- **Search Precision:** The tool relies on specific search terms (like "Match Thread") to find relevant threads. Variations in naming or case sensitivity can affect the results. However, the script incorporates case-insensitive checks to enhance its search precision.

- **MoreComments Objects:** Due to the way PRAW structures comment trees, some comments are wrapped in "MoreComments" objects, especially in deeper comment chains. The script has logic to expand these when possible, but there's always a trade-off between completeness and performance.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

