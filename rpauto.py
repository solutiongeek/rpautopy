#rpautopy - by Melissa Gurney
# Bookmarks an RP CG and puts it in image access mode so that it can be snapped
import requests
import json
import datetime
from datetime import datetime
import argparse
# Phase 1 - Authentication (user/password/ip/CG are defaults for RP Simulator)
user="admin"
password="admin"
rpip="192.168.128.129"
congrp="ELP"
target_site="NY Copy"

#


#test to check RPA state
#response=requests.get("http://%s/fapi/rest/4_0/state/rpas/all" % rpip, auth=(user,password))
#print (response)
#response=requests.post("http://%s/fapi/rest/4_0/settings/groups/actions/create_bookmarks",params=)

#find the guid of the consistency group we want
r=requests.get('https://%s/fapi/rest/4_1/groups/settings/' % rpip, auth=(user,password), verify=False)

#turn the response text into json and search it for the CG we want Why did this break in 4.1???
search_r=json.loads(r.text)
count = 0
while search_r['innerSet'][count]['name'] != congrp:
    print (search_r['innerSet'][count]['name'])
    count += 1
cg_guid = search_r['innerSet'][count]['groupUID']['id']
#it's a real pain to find the right clusterUID in all of this JSON
#start at the target site
ts_index=r.text.find(target_site)
#find clusterUID under Target site
cuid_index=r.text.find('clusterUID',ts_index)
id_index=r.text.find('id',cuid_index)
end_index=r.text.find('}',id_index)
clus_uid= r.text[id_index:end_index]

#this does not work
#copy_uid= search_r['innerSet'][count]['copyUID']
##just to be sure!
#print (search_r['innerSet'][count]['name'],cg_guid, clus_uid, copy_uid)

#now to create a unique bookmark!
bmark_stamp=str(datetime.now())
bmark_name=congrp+'_'+bmark_stamp
#I don't like spaces
bmark_name=bmark_name.replace(" ",'')

#THIS WORKS!
# -H "Content-Type: application/json" -X POST -d '{"bookmarkName":"TEST", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"2108804154"}]}
payload={"bookmarkName":"%s", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"%s"}] % congrp, cg_guid}
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
