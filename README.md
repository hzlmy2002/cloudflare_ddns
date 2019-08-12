# Usage

1. You should have one domain,and add a subdomain for this script.For example,if your domain name is "helloworld.com",your subdomain name might be "ddns.helloworld.com". 
2. You should first edit the "main.py" and input your own information(email,api_key,domain name,subdomain name),they can be found at "https://dash.cloudflare.com/profile/api-tokens", Remember,the api_key is the "Global API Key".
3. Install the requirements.
```
pip3 install requests
```

4. Use cronjob to run this program automatically.
```
*/5 * * * * /usr/bin/python3 /opt/cloudflare_ddns/main.py
```

5. Now it should work, just enjoy.
