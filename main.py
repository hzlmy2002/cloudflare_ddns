#!/usr/bin/python3
#coding:utf-8
import requests,os,re,json,sys
"""
Copyright: Copyright (c) 2019 hzlmy2002
Created on 2019-12-02
Author:Minyi_Lei
Version 1.1
Project Address:https://github.com/hzlmy2002/cloudflare_ddns

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


The following information can be found at https://dash.cloudflare.com/profile/api-tokens
Remember,the api_key is the "Global API Key" 

"""
class Cloudflare_Api():
	def __init__(self,email,api_key,domain_name,subdomain_name):
		self.domain_name=domain_name
		self.subdomain_name=subdomain_name
		self.should_update=False
		self.is_first_time=False
		self.auth_header={
			"X-Auth-Email":email,
			"X-Auth-Key":api_key,
			"Content-Type":"application/json"
		}
	def get_zone_id(self):
		url="https://api.cloudflare.com/client/v4/zones"
		payload={"name":self.domain_name}
		response=requests.get(url,params=payload,headers=self.auth_header).json()
		self.zone_id=response["result"][0]["id"]
	def get_record_id(self):
		url="https://api.cloudflare.com/client/v4/zones/"+self.zone_id+"/dns_records"
		payload={"name":subdomain_name}
		response=requests.get(url,params=payload,headers=self.auth_header).json()
		self.record_id=response["result"][0]["id"]
	def load(self):
		filename=self.subdomain_name+"_ip.txt"
		if os.path.exists(filename):
			self.is_first_time=False
			with open(filename,"r") as file:
				ip=file.read()
			if ip == self.current_ip:
				self.should_update=False
			else:
				self.should_update=True
		else:
			with open(filename,"w") as file:
				file.write(self.current_ip)
			self.is_first_time=True
	def get_current_ip(self,server="http://ipv4.lookup.test-ipv6.com/ip/?callback=_jqjsp&asn=1&testdomain=test-ipv6.com&testname=test_asn4"):
		url=server
		response=requests.get(url)
		pattern=re.compile(r"(\d{1,3}\.){3}\d{1,3}")
		text=response.text
		current_ip=pattern.search(text).group()
		self.current_ip=current_ip
	def update_record(self):
		url="https://api.cloudflare.com/client/v4/zones/"+self.zone_id+"/dns_records/"+self.record_id
		data={
			"type":"A",
			"name":self.subdomain_name,
			"content":self.current_ip
		}
		data=json.dumps(data)
		response=requests.put(url,data=data,headers=self.auth_header).json()
		self.feedback=response
		self.is_update_successfully=response["success"]
	def start(self):
		self.get_current_ip("http://ipv4.lookup.test-ipv6.com/ip/?callback=_jqjsp&asn=1&testdomain=test-ipv6.com&testname=test_asn4") #You can change this as long as the server's response contains your ip address
		self.load()
		if self.should_update or self.is_first_time:
			self.get_zone_id()
			self.get_record_id()
			self.update_record()
			if self.is_update_successfully:
				filename=self.subdomain_name+"_ip.txt"
				with open(filename,"w") as file:
					file.write(self.current_ip)
				print("Update the record successfully!")
			else:
				sys.stderr.write("Update failed! \n")
				sys.stderr.write(self.feedback)
		else:
			print("IP does not change")
if __name__ =="__main__":
	env_dict=os.environ
	try:
		email=env_dict["CF_Email"]
		api_key=env_dict["CF_Key"]
		domain_name=env_dict["CF_Domain"]
		if len(env_dict["CF_Host"]) == 0 :
			subdomain_name=domain_name
		else:
			subdomain_name=env_dict["CF_Host"]+"."+domain_name
	except Exception:
		sys.stderr.write("Please check your env (CF_Email,CF_Key,CF_Domain,CF_Host) and try again.\n")
		exit()
	cf=Cloudflare_Api(email,api_key,domain_name,subdomain_name)
	cf.start()