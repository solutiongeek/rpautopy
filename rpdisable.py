#rpdisablepy - by Melissa Gurney
# removes image access mode on a specific consistency group
import requests
import json
import datetime
from datetime import datetime
import argparse
#import XtremIOsnaps
#from XtremIOsnaps import *
# Phase 1 - Authentication (user/password/ip/CG are defaults for RP Simulator)
user=""
password=""
rpip=""
congrp="Test"
target_site="Tgt"
#
req=requests.get('https://%s/fapi/rest/4_1/groups/settings/' % rpip, auth=(user,password), verify=False)

#turn the response text into json and search it for the CG we want Why did this break in 4.1???
search_r=json.loads(req.text)
count = 0
while search_r['innerSet'][count]['name'] != congrp:
    print (search_r['innerSet'][count]['name'])
    count += 1

cg_guid = str(search_r['innerSet'][count]['groupUID']['id'])
#it's a real pain to find the right clusterUID in all of this JSON
#start at the target site
ts_index=req.text.find(target_site)
#find clusterUID under Target site
cuid_index=req.text.find('clusterUID',ts_index-100)
cp_index=req.text.find('copyUID',cuid_index)
cp_end=req.text.find('}',cp_index)
id_index=req.text.find('id',cuid_index)
end_index=req.text.find('}',id_index)
clus_uid= req.text[id_index+4:end_index]
copy_uid= req.text[cp_index+9:cp_end]
##just to be sure!
print (search_r['innerSet'][count]['name'],cg_guid, clus_uid, copy_uid)

#command to disable image access mode
#command works, commented out for demo
reques=requests.put('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/clusters/'+clus_uid+'/copies/'+copy_uid+'/disable_image_access', auth=(user,password), verify=False)
#the command above also pauses replication between sites. Need to resume.
resume=requests.put('https://'+rpip+'/fapi/rest/4_1/groups/'+cg_guid+'/start_transfer/', auth=(user,password), verify=False)
