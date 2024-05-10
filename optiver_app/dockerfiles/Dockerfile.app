# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY ./src .

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn" , "-w", "4" , "-k" , "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8000"]
#, "--port", "8000"]
    
#"uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]