#! /bin/bash

#!/bin/bash

# Default values
STREAM_NAME="optiver-stream"
DATA_TAG="demo_27"
DATA_PATH="data/stream_data.json"
BATCH_SIZE=50

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --stream-name) STREAM_NAME="$2"; shift ;;
        --data-tag) DATA_TAG="$2"; shift ;;
        --data-path) DATA_PATH="$2"; shift ;;
        --batch-size) BATCH_SIZE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Execute the Python script with arguments
python3 stream.py --stream-name "$STREAM_NAME" --data-tag "$DATA_TAG" --data-path "$DATA_PATH" --batch-size "$BATCH_SIZE"
