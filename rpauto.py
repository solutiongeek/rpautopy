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
congrp="Test"
target_site="Tgt"
''' this is for later
def iterateJSON(json_obj):
    object=json.loads(json_obj)
    for key,value in object.iterateitems():
        print (key,value)
#        ret_value[key:value]=value

#return group IDs available
group_ids=requests.get('https://%s/fapi/rest/4_1/groups/' % rpip, auth=(user,password), verify=False)
iterateJSON(group_ids)
'''
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

cg_guid = str(search_r['innerSet'][count]['groupUID']['id'])
#it's a real pain to find the right clusterUID in all of this JSON
#start at the target site
ts_index=r.text.find(target_site)
#find clusterUID under Target site
cuid_index=r.text.find('clusterUID',ts_index-100)
cp_index=r.text.find('copyUID',cuid_index)
cp_end=r.text.find('}',cp_index)
id_index=r.text.find('id',cuid_index)
end_index=r.text.find('}',id_index)
clus_uid= r.text[id_index+4:end_index]
copy_uid= r.text[cp_index+9:cp_end]
##just to be sure!
print (search_r['innerSet'][count]['name'],cg_guid, clus_uid, copy_uid)

#now to create a unique bookmark!
bmark_stamp=str(datetime.now())
bmark_name=congrp+'_'+bmark_stamp
#I don't like spaces
bmark_name=bmark_name.replace(" ",'')

#THIS WORKS!
# -H "Content-Type: application/json" -X POST -d '{"bookmarkName":"TEST", "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id":"2108804154"}]}
payload={"bookmarkName": bmark_name, "consistencyType":"CONSISTENCY_UNKNOWN", "consolidationPolicy":"NEVER_CONSOLIDATE", "groups":[{"id": cg_guid }]}
header = {'content-type':'application/json'}
# This request works!
re=requests.post('https://'+ rpip +'/fapi/rest/4_1/groups/bookmarks', data=json.dumps(payload), headers=header ,auth=(user, password), verify=False)
print(re.text,re)

##THIS REQUEST WORKS
#first, let's find that ERP2 test bookmark I created
req=requests.get('https://' + rpip +'/fapi/rest/4_1/groups/' + cg_guid +'/snapshots', auth=(user,password), verify=False)
print(req.text,req)
req=json.loads(req.text)
count=0
while req['copiesSnapshots'][0]['snapshots'][0]['description'] != bmark_name:
    print (req['copiesSnapshots'][0]['snapshots'][count]['description'])
    count += 1

ss_uid=req['copiesSnapshots'][0]['snapshots'][count]['snapshotUID']
ss_desc=req['copiesSnapshots'][0]['snapshots'][count]['description']
ss_cts=req['copiesSnapshots'][0]['snapshots'][count]['closingTimeStamp']
ss_sib=req['copiesSnapshots'][0]['snapshots'][count]['sizeInBytes']
ss_usib=req['copiesSnapshots'][0]['snapshots'][count]['uncompressedSizeInBytes']
ss_cifo=req['copiesSnapshots'][0]['snapshots'][count]['consolidationInfo']

'''
payload={"snapshot":{"snapshotUID":{"id":11992},"description":"ERP3","closingTimeStamp":{"timeInMicroSeconds":1441691248316888},"sizeInBytes":4667409920,
"uncompressedSizeInBytes":4667409920,"consolidationInfo":{"consolidationPolicy":"NEVER_CONSOLIDATE","consolidationType":"NO_CONSOLIDATION","savedSpaceInBytes":0}}
,"mode":"LOGGED_ACCESS","scenario":"NONE"}

'''
payload={"snapshot":{"snapshotUID":ss_uid,"description":ss_desc,"closingTimeStamp":ss_cts,"sizeInBytes":ss_sib,"uncompressedSizeInBytes":ss_usib,"consolidationInfo":ss_cifo},"mode":"LOGGED_ACCESS","scenario":"NONE"}
requ=requests.put('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/clusters/'+clus_uid+'/copies/'+copy_uid+'/enable_image_access', data=json.dumps(payload), headers=header, auth=(user,password), verify=False)
#print(req.text,req)
reque=requests.get('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/state', auth=(user,password), verify=False)
##basic test assuming no other reason this cg would have a snap in logged access mode
enabled=reque.text.find("LOGGED_ACCESS")
if enabled>-1:
        print ("Access Enabled!")

#command to disable image access mode
#command works, commented out for demo
#reques=requests.put('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/clusters/'+clus_uid+'/copies/'+copy_uid+'/disable_image_access', auth=(user,password), verify=False)
#the command above also pauses replication between sites. Need to resume.
#resume=requests.put('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/start_transfer/', auth=(user,password), verify=False)
