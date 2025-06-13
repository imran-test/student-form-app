import json
import boto3
import urllib.parse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')

def lambda_handler(event, context):
    method = event.get("httpMethod")
    
    if method == "GET":
        # Return all students
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", [])),
            "headers": {"Content-Type": "application/json"}
        }

    elif method == "POST":
        # Get body data (application/x-www-form-urlencoded)
        body = urllib.parse.parse_qs(event.get("body", ""))
        
        student_id = body.get("student_id", [""])[0]
        name = body.get("name", [""])[0]
        age = body.get("age", [""])[0]
        course = body.get("course", [""])[0]

        table.put_item(Item={
            "student_id": student_id,
            "name": name,
            "age": age,
            "course": course
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Student saved"}),
            "headers": {"Content-Type": "application/json"}
        }

    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }
