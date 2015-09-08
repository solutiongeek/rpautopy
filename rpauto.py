#rpautopy - by Melissa Gurney
# Bookmarks an RP CG and puts it in image access mode so that it can be snapped
import requests
import json
import datetime
from datetime import datetime
# Phase 1 - Authentication (user/password/ip/CG are defaults for RP Simulator)
user="admin"
password="admin"
rpip="192.168.128.129"
congrp="ERP"
#test to check RPA state
#response=requests.get("http://%s/fapi/rest/4_0/state/rpas/all" % rpip, auth=(user,password))
#print (response)
#response=requests.post("http://%s/fapi/rest/4_0/settings/groups/actions/create_bookmarks",params=)

#find the guid of the consistency group we want
r=requests.get('https://192.168.128.129/fapi/rest/4_1/groups/settings/',auth=('admin','admin'), verify=False)

#turn the response text into json and search it for the CG we want Why did this break in 4.1???
search_r=json.loads(r.text)
count = 0
while search_r['innerSet'][count]['name'] != congrp:
  print (search_r['innerSet'][count]['name'])
  count += 1

cg_guid = 34688008     #search_r[count]['groupUID']['id']
#added clusterUID var for later when we need it for image access mode
clus_uid= search_r['innerSet'][count]['clusterUID']
copy_uid= search_r['innerSet'][count]['copyUID']
##just to be sure!
print (cg_guid, search_r[count]['name'], clus_uid, copy_uid)
#, clus_uid)

#now to create a bookmark!
bmark_stamp=str(datetime.now())
bmark_name=congrp+'_'+bmark_stamp
#I don't like spaces
bmark_name=bmark_name.replace(" ",'')

#THIS WORKS!
# -H "Content-Type: application/json" -X POST -d '{"bookmarkName":"TEST", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"2108804154"}]}
payload={"bookmarkName":"ERP3", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"34688008"}]}
header = {'content-type':'application/json'}
# This request works!
re=requests.post('https://192.168.128.129/fapi/rest/4_1/groups/bookmarks', data=json.dumps(payload), headers=header ,auth=('admin','admin'), verify=False)
print(re.text,re)

##THIS REQUEST WORKS
#first, let's find that ERP2 test bookmark I created
req=requests.get('https://192.168.128.129/fapi/rest/4_1/groups/%s/snapshots' % cg_guid, auth=('admin','admin'), verify=False)
print(req.text,req)
#test
#this command works!
payload={"snapshot":{"snapshotUID":{"id":11992},"description":"ERP3","closingTimeStamp":{"timeInMicroSeconds":1441691248316888},"sizeInBytes":4667409920,"uncompressedSizeInBytes":4667409920,"consolidationInfo":{"consolidationPolicy":"NEVER_CONSOLIDATE","consolidationType":"NO_CONSOLIDATION","savedSpaceInBytes":0}},"mode":"LOGGED_ACCESS","scenario":"NONE"}
requ=requests.put('https://192.168.128.129/fapi/rest/4_1/groups/34688008/clusters/111/copies/0/enable_image_access', data=json.dumps(payload), headers=header, auth=('admin','admin'), verify=False)
#print(req.text,req)
reque=requests.get('https://192.168.128.129/fapi/rest/4_1/groups/%s/state' % cg_guid, auth=('admin','admin'), verify=False)
##basic test assuming no other reason this cg would have a snap in logged access mode
enabled=reque.text.find("LOGGED_ACCESS")
if enabled>-1:
        print ("Access Enabled!")
