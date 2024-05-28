## SETTING UP REVERSE PROXY USING NGINX

Install Nginx
```bash
sudo yum install nginx
```



## FIREWALL CONFIGURATIONS TO EXPOSE PORT ON EC2 FOR APPLICATION

Step 1: Install firewalld

If firewalld is not already installed on your Amazon Linux instance, you can install it using the yum package manager:

```bash
sudo yum install firewalld
```

Step 2: Start and Enable firewalld

Once installed, you need to start the firewalld service and enable it to start at boot:

```bash
sudo systemctl start firewalld
sudo systemctl enable firewalld
```

Step 3: Managing Firewall Rules

Here are some common commands to manage your firewall settings with firewalld:

Check the status of firewalld:
```bash
sudo firewall-cmd --state
```

List all active rules:
```bash
sudo firewall-cmd --list-all
```

Allow traffic on a specific port:
- To permanently allow traffic on a specific port (e.g., port 80):
    ```bash
    sudo firewall-cmd --permanent --add-port=80/tcp
    ```
- Then reload firewalld to apply the changes:
    ```bash
    sudo firewall-cmd --reload
    ```
Remove a port from the allowed list:
```bash
sudo firewall-cmd --permanent --remove-port=80/tcp
sudo firewall-cmd --reload
```


