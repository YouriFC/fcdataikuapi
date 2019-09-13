import dataiku
import re

#Definitely fix this function when we know what the admin account actually is supposed to look like 
def AdminValidator(dataiku_client, gds_name, devops_team): 
    #User stuff
    userinfo = dataiku_client.get_auth_info()
    assert(gds_name.lower() == userinfo['authIdentifier'].lower()), "GDS Name does not match code owner"

    #Group stuff
    grouplist = dataiku_client.list_groups()
    assert(devops_team in [x['name'] for x in grouplist]), "DevOps Team does not exist"
    assert("administrators" in userinfo['groups'])

    return(gds_name)
