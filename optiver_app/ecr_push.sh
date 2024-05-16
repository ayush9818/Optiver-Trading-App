#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <image_name> <image_tag>"
    exit 1
fi

# Assign command-line arguments to variables
IMAGE_NAME=$1
IMAGE_TAG=$2

# Define your AWS ECR repository URI
AWS_ECR_REPO_URI="058264109996.dkr.ecr.us-east-1.amazonaws.com"

# Authenticate Docker to your Amazon ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ECR_REPO_URI

# Build the Docker image
docker build -f dockerfiles/Dockerfile.app -t $IMAGE_NAME .

# Tag the Docker image
docker tag $IMAGE_NAME:latest $AWS_ECR_REPO_URI/optiver-db-app:$IMAGE_TAG

# Push the Docker image to the AWS ECR repository
docker push $AWS_ECR_REPO_URI/optiver-db-app:$IMAGE_TAG
