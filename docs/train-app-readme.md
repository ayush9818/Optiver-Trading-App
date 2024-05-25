To Build Train APPP
```bash
docker build -f dockerfiles/Dockerfile.train -t optiver-train-app .
```

To run the Optiver DB APP 
```bash
docker run -d --env-file $(pwd)/.env -p 81:8001 --name train-app optiver-train-app
```

## FIREWALL CONFIGURATIONS TO EXPOSE PORT ON EC2 FOR APPLICATION

Allow traffic on a specific port:
- To permanently allow traffic on a specific port (e.g., port 81):
    ```bash
    sudo firewall-cmd --permanent --add-port=81/tcp
    ```
- Then reload firewalld to apply the changes:
    ```bash
    sudo firewall-cmd --reload
    ```


