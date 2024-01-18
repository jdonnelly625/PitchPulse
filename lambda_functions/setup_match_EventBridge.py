import os
import json
import pymysql
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize clients
    eventbridge_client = boto3.client('events')
    #Keys stored as lambda environment variables
    rds_data = pymysql.connect(
        host=os.environ['RDS_HOST'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        db=os.environ['RDS_DB'],
        connect_timeout=5
    )

    try:
        with rds_data.cursor() as cursor:
            # Query to get the upcoming matches
            cursor.execute("SELECT name, next_game FROM team WHERE next_game IS NOT NULL")
            matches = cursor.fetchall()

            for match in matches:
                team_name, next_game = match
                schedule_expression = f"cron({next_game.minute} {next_game.hour} {next_game.day} {next_game.month} ? {next_game.year})"
                formatted_team_name = format_rule_name(team_name) # Cannot have spaces when creating rule names
                target_arn = os.environ[TARGET_ARN] # Target ARN stored as key

                try:
                    eventbridge_client.put_rule(
                        Name=formatted_team_name,
                        ScheduleExpression=schedule_expression,
                        State='ENABLED',
                    )
                    eventbridge_client.put_targets(
                        Rule=formatted_team_name,
                        Targets=[
                            {
                                'Id': f"TargetForTeam{team_name.replace(' ', '_')}",
                                'Arn': target_arn,
                                'Input': json.dumps({'teamName': team_name})
                            }
                        ]
                    )
                except ClientError as e:
                    print(f"Error creating rule for team {team_name}: {e}")

        return {'statusCode': 200, 'body': json.dumps('EventBridge rules updated successfully')}

    except pymysql.MySQLError as e:
        return {'statusCode': 500, 'body': json.dumps(f"Database connection failed: {str(e)}")}
    finally:
        if rds_data:
            rds_data.close()

def format_rule_name(team_name):
    # Replace spaces with a valid character like an underscore or hyphen
    return f"MatchScheduleForTeam{team_name.replace(' ', '_')}"