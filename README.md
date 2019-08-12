#Usage
1. You should first edit the "main.py" and input your own information(email,api_key,domain name,subdomain name).
2. Install the requirements.
```pip3 install requests
```

3. Use cronjob to run this program automatically.
```
*/5 * * * * /usr/bin/python3 /opt/cloudflare_ddns/main.py
```

4. Now it should work, just enjoy.
