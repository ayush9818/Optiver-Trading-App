### Data Streaming Documentation

---

## Data Streaming

The Data Streaming component is responsible for real-time data ingestion using AWS Kinesis Data Streams. It ensures that live market data is continuously fed into the system for processing and analysis.

### Steps to Set Up Data Streaming

1. **Create a Stream on AWS Kinesis**

   First, you need to create a stream on AWS Kinesis. Follow these steps:

   - Go to the AWS Management Console.
   - Navigate to the Kinesis service.
   - Click on "Create stream".
   - Enter the stream name (e.g., `optiver-stream`) and the number of shards.
   - Click on "Create stream".

2. **Build a Lambda Function**

   Next, you need to create an AWS Lambda function and configure it to process data from the Kinesis stream.

   - Go to the AWS Lambda service in the AWS Management Console.
   - Click on "Create function".
   - Choose "Author from scratch".
   - Enter a name for your function (e.g., `KinesisProcessor`).
   - Choose a runtime (e.g., Python 3.x).
   - Click on "Create function".

   Once the function is created, copy and paste the content of `lambda.py` into the Lambda function code editor. 

   - Click on "Deploy".

   Next, configure the Lambda function to trigger on new records in the Kinesis stream:

   - Go to the "Configuration" tab of your Lambda function.
   - Click on "Add trigger".
   - Choose "Kinesis".
   - Select the Kinesis stream you created earlier (e.g., `optiver-stream`).
   - Click on "Add".

3. **Data Format**

   Refer to `data/stream_data.json` for the data format. 


4. **Ingest Data Using the Bash Script**

   To ingest data into the Kinesis stream, use the provided bash script scripts/stream_demo.sh

   To run the script, use the following command in your terminal:

   ```bash
   bash scripts/stream_demo.sh --stream-name optiver-stream --data-tag demo_27 --data-path data/stream_data.json --batch-size 50
   ```

   This script will execute the `stream.py` script, which processes the data in batches and sends it to the Kinesis stream.

---