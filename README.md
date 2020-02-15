# Usage

1. You should have one domain,and add a subdomain for this script.For example,if your domain name is "helloworld.com",your subdomain name might be "ddns.helloworld.com". 
2. The most important thing is to get your cloudflare api key,it can be found at "https://dash.cloudflare.com/profile/api-tokens". The api_key is the "Global API Key".
3. Install the requirements.
```
pip3 install requests
```

4. Edit "main.py" and input your own information then using cronjob to run this program automatically.Please be reminded that your should first setup the environment variables(CF_Email,CF_Key,CF_Domain,CF_Host) so that the script can run properly.
```
#note:This sample only takes effect if you are using vixie-cron(Debian,Ubuntu).If you are using cronie(Arch,Redhat),please use "export xxx" instead.

CF_Email="xxx@gmail.com"
CF_Key="adiauyicas4d5a465a46"
CF_Domain="example.com"
CF_Hosts="hostname1,hostname2"
*/5 * * * * /usr/bin/python3 /opt/cloudflare_ddns/main.py
```

5. Now it should work, just enjoy.
