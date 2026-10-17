import json
import os
import boto3
from botocore.exceptions import ClientError

def create_task_definition():

    commit_sha = os.environ.get("GITHUB_SHA", "unknown")[:8]
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID", "")

    task_definition = {
        "family": "amazon-fe",
        "containerDefinitions": [
            {
                "name": "chatbot-ui",
                "image": f"{aws_account_id}.dkr.ecr.eu-central-1.amazonaws.com/amazon-fe:{commit_sha}",
                "cpu": 0,
                "portMappings": [
                    {
                        "name": "chatbot-ui-8501-tcp",
                        "containerPort": 8501,
                        "hostPort": 8501,
                        "protocol": "tcp",
                        "appProtocol": "http"
                    }
                ],
                "essential": True,
                "environment": [
                    {
                        "name": "API_URL",
                        "value": "http://api:8000"
                    }
                ],
                "mountPoints": [],
                "volumesFrom": [],
                "secrets": [],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/amazon-fe",
                        "mode": "non-blocking",
                        "awslogs-create-group": "true",
                        "max-buffer-size": "25m",
                        "awslogs-region": "eu-central-1",
                        "awslogs-stream-prefix": "ecs"
                    }
                },
                "systemControls": []
            }
        ],
        "taskRoleArn": f"arn:aws:iam::{aws_account_id}:role/amazon-fe-task-role",
        "executionRoleArn": f"arn:aws:iam::{aws_account_id}:role/ecsTaskExecutionRole",
        "networkMode": "awsvpc",
        "volumes": [],
        "placementConstraints": [],
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "cpu": "512",
        "memory": "2048",
        "runtimePlatform": {
            "cpuArchitecture": "X86_64",
            "operatingSystemFamily": "LINUX"
        },
        "enableFaultInjection": False,
        "tags": [
            {
                "key": "CommitSHA",
                "value": commit_sha
            },
            {
                "key": "ManagedBy",
                "value": "GitHub-Actions"
            }
        ]
    }

    try:
        ecs_client = boto3.client('ecs')
        
        response = ecs_client.register_task_definition(**task_definition)
        
        print(f"✅ Task definition registered successfully!")
        print(f"Task Definition ARN: {response['taskDefinition']['taskDefinitionArn']}")
        print(f"Revision: {response['taskDefinition']['revision']}")
        print(f"Commit SHA: {commit_sha}")
        
        return response
        
    except ClientError as e:
        print(f"❌ Error registering task definition: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":

    print("Creating ECS Task Definition...")
    create_task_definition()