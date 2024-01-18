import boto3
import json
import os

def lambda_handler(event, context):
    # Parse the event data to get the team name
    # Note: This function will be activated by EventBridge and scheduled for match time
    
    team_name = event['team_name']

    # Define your ECS cluster and task definition
    ecs_cluster = 'PlayerTracker'
    ecs_task_definition = os.environ['ECS_TASK_DEFINITION'] 

    # Initialize the ECS client
    ecs_client = boto3.client('ecs')

    try:
        # Run the ECS task with the necessary environment variable
        # Most of this is just configuring it with sdk then running it
        response = ecs_client.run_task(
            cluster=ecs_cluster,
            taskDefinition=ecs_task_definition,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['subnet-00779c7addf7627aa', 'subnet-0a74df4736be36bf3', 'subnet-0aa3ebf28c77244dc', 'subnet-0bc788dfbb2d97cb9', 'subnet-0a67a9470cf54583e', 'subnet-05de121ce195f4c07'],
                    'securityGroups': ['sg-0d3e085f237a45649', 'sg-0a3d098765c735d5c'],
                    'assignPublicIp': 'ENABLED'
                }
            },
            # Here is where we specify the team
            overrides={
                'containerOverrides': [
                    {
                        'name': 'pitchpulse-container',  
                        'environment': [
                            {
                                'name': 'TEAM_NAME',
                                'value': team_name
                            }
                        ]
                    }
                ]
            }
        )
    except Exception as e:
        print(f"Error running ECS task for team {team_name}: {e}")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps(f'ECS task started successfully for team {team_name}')
    }