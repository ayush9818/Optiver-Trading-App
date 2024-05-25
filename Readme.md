# Optiver Trading App

## Introduction

The Optiver Trading App is designed to predict closing price movements of Nasdaq-listed stocks using order book data and various machine learning techniques. The project utilizes cloud engineering principles to ensure scalability, flexibility, and real-time processing, making it suitable for high-stakes environments where accurate price predictions are critical.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [API Endpoints](#api-endpoints)
7. [Model Training and Deployment](#model-training-and-deployment)
8. [Database Schema](#database-schema)
9. [Logging and Monitoring](#logging-and-monitoring)
10. [Contributors](#contributors)
11. [License](#license)

## Features

- **Real-Time Data Processing**: Utilizes AWS Kinesis Data Streams and Lambda for real-time data ingestion and processing.
- **Scalability**: Easily handles large datasets with the ability to scale resources up or down.
- **Machine Learning**: Implements XGBoost for incremental training and prediction.
- **Flexible Cloud Architecture**: Integrates various AWS services (ECS, RDS, S3) for a robust infrastructure.
- **Web Interface**: Provides a user-friendly interface for interacting with the application and visualizing performance.

## Installation

To set up the Optiver Trading App, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ayush9818/Optiver-Trading-App.git
   cd Optiver-Trading-App
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS Credentials**:
   Ensure that your AWS credentials are configured properly. This can be done using the AWS CLI:
   ```bash
   aws configure
   ```

## Usage

### Running the Application

1. **Start Data Ingestion**:
   ```bash
   python stream.py
   ```

2. **Launch the Web Interface**:
   ```bash
   python app.py
   ```

## Configuration

Configuration is managed through environment variables and AWS Secrets Manager for sensitive information.

### Environment Variables

- **API URLs**
- **Bucket Name**
- **Bucket Region**
- **Secret Name**

### Sensitive Information

- **RDS Credentials**
- **AWS Access Key and ID**

These are stored in AWS Secrets Manager to ensure security.

## API Endpoints

### Stock Data API
- **Endpoint**: `/stock_data/`
- **Methods**: `GET`, `POST`
- **Description**: Fetches and ingests stock data.

### Date Mappings API
- **Endpoint**: `/date_mappings/`
- **Methods**: `GET`, `POST`
- **Description**: Retrieves and adds date mappings.

### Model Inferences API
- **Endpoint**: `/model-inferences/`
- **Methods**: `GET`
- **Description**: Retrieves and posts inferences.

### Models API
- **Endpoint**: `/models/`
- **Methods**: `GET`
- **Description**: Fetches and adds model details.

## Model Training and Deployment

### Training Steps
1. Fetch data for the given date.
2. Retrieve the model to be fine-tuned.
3. Fine-tune the model with the provided data.
4. Upload the trained model artifact to S3.
5. Ingest trained model details into the database.

### Inference Steps
1. Fetch data corresponding to `date_id`.
2. Retrieve the model artifact from S3.
3. Run inference on the data and generate a CSV.
4. Upload the CSV file to S3 and update the database.

### Deployment Workflow
- **ECS Cluster**: Created using EC2 instances.
- **Task Definitions**: Specify Docker images, CPU, memory, and network settings.
- **Service Configuration**: Manage deployment and scaling of tasks.
- **Auto Scaling**: Policies to adjust running tasks based on resource utilization.
- **Load Balancer**: Deployed ALB for traffic distribution.
- **RDS Integration**: Reliable database backend.
- **Elastic Container Registry (ECR)**: For managing Docker images.

## Database Schema

The database schema includes tables for storing stock data, date mappings, model details, and inferences. Detailed schema information is provided in the source code.

## Logging and Monitoring

Logging and monitoring are handled using AWS CloudWatch. This includes tracking data ingestion, processing, and model performance metrics.

## Contributors

- **Ayush** - Initial development and deployment.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

For detailed information on each component, please refer to the [source code repository](https://github.com/ayush9818/Optiver-Trading-App).