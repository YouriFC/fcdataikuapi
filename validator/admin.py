import dataiku
import re

#Definitely fix this function when we know what the admin account actually is supposed to look like 
def AdminValidator(dataiku_client, gds_name): 
    #User stuff
    userinfo = dataiku_client.get_auth_info()
    assert(gds_name.lower() == userinfo['authIdentifier'].lower()), "GDS Name does not match code owner"

    #Group stuff
    grouplist = dataiku_client.list_groups()
    assert("administrators" in userinfo['groups'])

    return(gds_name)
