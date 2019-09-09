import dataiku
import re

def ProjectValidator(dataiku_client, gds_name): 
    userinfo = dataiku_client.get_auth_info()
    assert(gds_name.lower() == userinfo['authIdentifier'].lower()), "GDS Name does not match code owner"
    
    checklist = []
    for entry in userinfo['groups']:
        if re.search(r"(lead|admin)",entry, re.IGNORECASE):
            checklist.append(True)
    assert(True in checklist), "This user does not have the required priviliges to perform this action."
    
    return
