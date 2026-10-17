import json
import os
import boto3
from botocore.exceptions import ClientError

def create_task_definition():

    commit_sha = os.environ.get("GITHUB_SHA", "unknown")[:8]
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID", "")

    task_definition = {
        "family": "amazon-be",
        "containerDefinitions": [
            {
                "name": "api",
                "image": f"{aws_account_id}.dkr.ecr.eu-central-1.amazonaws.com/amazon-be:{commit_sha}",
                "cpu": 0,
                "portMappings": [
                    {
                        "name": "api-8000-tcp",
                        "containerPort": 8000,
                        "hostPort": 8000,
                        "protocol": "tcp",
                        "appProtocol": "http"
                    }
                ],
                "essential": True,
                "environment": [
                    {
                        "name": "LANGSMITH_TRACING",
                        "value": "true"
                    },
                    {
                        "name": "LANGSMITH_ENDPOINT",
                        "value": "https://api.smith.langchain.com"
                    },
                    {
                        "name": "LANGSMITH_PROJECT",
                        "value": "rag-tracing"
                    }
                ],
                "mountPoints": [],
                "volumesFrom": [],
                "secrets": [
                    {
                        "name": "OPENAI_API_KEY",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/openai-api-key-Ljs6wb"
                    },
                    {
                        "name": "LANGSMITH_API_KEY",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/langsmith-api-key-KniQZV"
                    },
                    {
                        "name": "GROQ_API_KEY",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/groq-api-key-mL1InQ"
                    },
                    {
                        "name": "QDRANT_URL",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/qdrant-url-z2B40M"
                    },
                    {
                        "name": "QDRANT_API_KEY",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/qdrant-api-key-ZaVqmv"
                    },
                    {
                        "name": "SUPABASE_URL",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/supabase-url-DGxHVn"
                    },
                    {
                        "name": "SUPABASE_LANGGRAPH_USER",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/supabase-langgraph-user-biENNL"
                    },
                    {
                        "name": "SUPABASE_LANGGRAPH_PASSWORD",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/supabase-langgraph-password-YgydAs"
                    },
                    {
                        "name": "SUPABASE_TOOLS_USER",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/supabase-tools-user-8Brbcb"
                    },
                    {
                        "name": "SUPABASE_TOOLS_PASSWORD",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/supabase-tools-password-Bg8bQb"
                    },
                    {
                        "name": "CO_API_KEY",
                        "valueFrom": f"arn:aws:secretsmanager:eu-central-1:{aws_account_id}:secret:shopping-assistant/co-api-key-25zpyK"
                    }
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/amazon-be",
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
        "taskRoleArn": f"arn:aws:iam::{aws_account_id}:role/amazon-be-task-role",
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