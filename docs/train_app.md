# Train and Inference App Documentation

Navigate to train-app directory

## Local Setup 

- Create and fill the env file
    ```bash
    touch .env
    copy env_copy .env
    ```

- To Build Train APPP
    ```bash
    docker build -f dockerfiles/Dockerfile.train -t optiver-train-app .
    ```

- To run the Optiver Train APP 
    ```bash
    docker run -d --env-file $(pwd)/.env -p 80:80 --name train-app optiver-train-app
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
    sh ecr_push.sh optiver-train-app v1
    ```


## Deploy ECS Tasks and Services

- Create or chose an existing cluster
- Create a ECS Fargate Tasks with the container image and environment variables
- Deploy the task as ECS Service
- Configure Security Groups and Load Balancer to route traffic


