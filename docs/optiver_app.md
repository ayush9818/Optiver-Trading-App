# Optiver Database App Documentation

Navigate to optiver_app directory
```bash
cd optiver_app/
```

## Initial Setup

- To Create DB Schema
    ```bash
    python src/schema.py --create-schema
    ```

- To Run initial Data Ingestion
    ```bash
    - nohup python app/ingest_data.py \
                --data-path data/optiver_train.csv \
                --batch-size 5000 \
                --commit > logs/ingestion_logs.log 2>&1 &
    ```

## Building and Running Dockerfile in Local

- Create .env file and fill the necessary credentials
    ```bash
    touch .env 
    copy env_copy .env
    ```

- To Build Optiver DB APP 
    ```bash
    docker build -f dockerfiles/Dockerfile.app -t optiver-db-app .
    ```

- To run the Optiver DB APP 
    ```bash
    docker run -d --env-file $(pwd)/.env -p 80:80 optiver-db-app
    ```

## Pushing image to ECR

- Create a ECR Repository using AWS console

- Change "AWS_ECR_REPO_URI" and "ECR_REPO_NAME" variables in ecr_push.sh according to your configuration

- Push the image to ECR
    ```bash
    sh ecr_push.sh <local_image_name> <ecr_version>
    ```

- Example
    ```bash
    sh ecr_push.sh optiver-db-app v1
    ```


## Deploy ECS Tasks and Services

- Create or chose an existing cluster
- Create a ECS Fargate Tasks with the container image and environment variables
- Deploy the task as ECS Service
- Configure Security Groups and Load Balancer to route traffic