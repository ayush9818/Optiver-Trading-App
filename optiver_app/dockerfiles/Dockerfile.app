# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src/app

# Copy the current directory contents into the container at /app
COPY ./app .

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

WORKDIR /src

EXPOSE 8000

CMD ["gunicorn" , "-w", "4" , "-k" , "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]