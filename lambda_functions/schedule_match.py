import json
import requests
import pymysql
import os
from datetime import datetime

def lambda_handler(event, context):
    # Database connection set up
    connection = pymysql.connect(
        host=os.environ['RDS_HOST'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        db=os.environ['RDS_DB'],
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:
            # Retrieve all team IDs from RDS database, unique ID assigned by Football API
            cursor.execute("SELECT api_id FROM team")
            teams = cursor.fetchall()
            
            #Iterate over all the teams
            for team in teams:
                team_id = team[0]

                # Setting up the API request for each team, matching the ID number
                url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
                querystring = {"team": str(team_id), "next": "1"}
                headers = {
                    "X-RapidAPI-Key": os.environ['API_FOOTBALL_KEY'],
                    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()
                data = response.json()

                if not data['response']:
                    continue  # No upcoming matches found for this team

                match_info = data['response'][0]
                match_datetime_str = match_info['fixture']['date']
                match_datetime = datetime.fromisoformat(match_datetime_str)

                # Update the next game time for the team
                update_sql = "UPDATE team SET next_game = %s WHERE api_id = %s"
                cursor.execute(update_sql, (match_datetime, team_id))

            connection.commit()  # Commit after processing all teams

        return {'statusCode': 200, 'body': json.dumps('Operation completed for all teams')}

    except requests.RequestException as e:
        return {'statusCode': 500, 'body': json.dumps(f"Error fetching data from API: {str(e)}")}
    except pymysql.MySQLError as e:
        return {'statusCode': 500, 'body': json.dumps(f"Database connection failed: {str(e)}")}
    finally:
        # Make sure to close connection, therefore in finally block
        if connection:
            connection.close()

