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
response=requests.get("http://%s/fapi/rest/4_0/state/rpas/all" % rpip, auth=(user,password))
print (response)
