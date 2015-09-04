#rpautopy - by Melissa Gurney
# Bookmarks an RP CG and puts it in image access mode so that it can be snapped
import requests
import json
import datetime
from datetime import datetime
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
#added clusterUID var for later when we need it for image access mode
#clus_uid= search_r[count]['clusterUID']
##just to be sure!
print (cg_guid, search_r[count]['name'])
#, clus_uid)

#now to create a bookmark!
bmark_stamp=str(datetime.now())
bmark_name=congrp+'_'+bmark_stamp
#I don't like spaces
bmark_name=bmark_name.replace(" ",'')

# -H "Content-Type: application/json" -X POST -d '{"bookmarkName":"TEST", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"2108804154"}]}
payload={"bookmarkName":"ERP2", "consistencyType":"ConsistencyUnknown", "consolidationPolicy":"NoConsolidation", "groups":[{"id":"1859504091"}]}
header = {'content-type':'application/json'}
# This request works!
re=requests.post('https://192.168.128.128/fapi/rest/4_0/settings/groups/actions/create_bookmark', data=json.dumps(payload), headers=header ,auth=('admin','admin'), verify=False)
print(re.text,re)

#first, let's find that ERP2 test bookmark I created
req=requests.get('https://192.168.128.128/fapi/rest/4_0/settings/groups/%s/snapshots' % cg_guid, auth=('admin','admin'), verify=False)
search_req=json.loads(req.text)

print(req.text,req)
