#rpautopy - by Melissa Gurney
# Bookmarks an RP CG and puts it in image access mode so that it can be snapped
import requests
import json
# Phase 1 - Authentication (user/password/ip/CG are defaults for RP Simulator)
user="admin"
password="admin"
rpip="192.168.128.128"
congrp="ERP"
#test to check RPA state
#response=requests.get("http://%s/fapi/rest/4_0/state/rpas/all" % rpip, auth=(user,password))
#print (response)
#response=requests.post("http://%s/fapi/rest/4_0/settings/groups/actions/create_bookmarks",params=)

#find the guid of the consistency group we want
r=requests.get('https://192.168.128.128/fapi/rest/4_0/settings/groups/all',auth=('admin','admin'), verify=False)
#turn the response text into json and search it for the CG we want
search_r=json.loads(r.text)
count = 0
while search_r[count]['name'] != congrp:
  print (search_r[count]['name'])
  count += 1

cg_guid = search_r[count]['groupUID']['id']
##just to be sure!
print (cg_guid, search_r[count]['name'])