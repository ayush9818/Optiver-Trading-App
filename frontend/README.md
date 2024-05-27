## Getting Started
To run  Optiver Trading App locally, follow these steps:
#### Create a venv
```bash
python3 -m venv venv
```
#### Activate the venv
##### On Windows:
```bash
venv\Scripts\activate
```
##### On Unix or MacOS:
```bash
source venv/bin/activate
```
#### Install dependencies
```bash
pip install -r requirements.txt
```
#### Run program
```bash
streamlit run main.py
```
## Build the Docker image
```bash
docker build -f dockerfiles/Dockerfile -t optiver_app .
```
## Rebuild the Docker image
```bash
docker build --no-cache -f dockerfiles/Dockerfile -t optiver_app .
```
