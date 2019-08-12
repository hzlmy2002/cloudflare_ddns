#!/usr/bin/python3
#coding:utf-8
"""
get_current_ip => load => get_zone_id => get_record_id => update_record
"""
import requests
import os
import re
import json
"""
Copyright: Copyright (c) 2019
Created on 2019-08-12  
Author:Minyi_Lei
Version 1.0
Project Address:https://github.com/hzlmy2002/cloudflare_ddns

The following information can be found at https://dash.cloudflare.com/profile/api-tokens
Remember,the api_key is the "Global API Key" 
"""
email=""
api_key=""
domain_name=""
subdomain_name=""
class Cloudflare_Api():
	def __init__(self,email,api_key,domain_name,subdomain_name):
		self.email=email
		self.api_key=api_key
		self.domain_name=domain_name
		self.subdomain_name=subdomain_name
		self.should_update=False
		self.is_first_time=False
	def get_zone_id(self):
		url="https://api.cloudflare.com/client/v4/zones"
		payload={"name":self.domain_name}
		data={
			"X-Auth-Email":email,
			"X-Auth-Key":api_key,
			"Content-Type":"application/json"
		}
		response=requests.get(url,params=payload,headers=data).json()
		self.zone_id=response["result"][0]["id"]
	def get_record_id(self):
		url="https://api.cloudflare.com/client/v4/zones/"+self.zone_id+"/dns_records"
		payload={"name":subdomain_name}
		data={
			"X-Auth-Email":email,
			"X-Auth-Key":api_key,
			"Content-Type":"application/json"
		}
		response=requests.get(url,params=payload,headers=data).json()
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
	def get_current_ip(self,server):
		url=server                                        #"http://45.32.164.128/ip.php"
		response=requests.get(url)
		pattern=re.compile(r"(\d{1,3}\.){3}\d{1,3}")
		text=response.text
		current_ip=pattern.search(text).group()
		self.current_ip=current_ip
	def update_record(self):
		url="https://api.cloudflare.com/client/v4/zones/"+self.zone_id+"/dns_records/"+self.record_id
		header_data={
			"X-Auth-Email":email,
			"X-Auth-Key":api_key,
			"Content-Type":"application/json"
		}
		data={
			"type":"A",
			"name":self.subdomain_name,
			"content":self.current_ip
		}
		data=json.dumps(data)
		response=requests.put(url,data=data,headers=header_data).json()
		self.feedback=response
		self.is_update_successfully=response["success"]
	def start(self):
		self.get_current_ip("http://45.32.164.128/ip.php") #You can change this as long as the server's response contains your ip address
		self.load()
		if self.should_update or self.is_first_time:
			self.get_zone_id()
			self.get_record_id()
			self.update_record()
			if self.is_update_successfully:
				print("Update the record successfully!")
			else:
				print("Update failed")
				print(self.feedback)
		else:
			print("ip does not change")
cf=Cloudflare_Api(email,api_key,domain_name,subdomain_name)
cf.start()
