import dataiku
import re

def ProjectValidator(dataiku_client, gds_name, devops_team): 
    #User stuff
    userinfo = dataiku_client.get_auth_info()
    assert(gds_name.lower() == userinfo['authIdentifier'].lower()), "GDS Name does not match code owner"

    #Group stuff
    grouplist = dataiku_client.list_groups()
    assert(devops_team in [x['name'] for x in grouplist]), "DevOps Team does not exist"
    if "administrators" not in userinfo['groups']:
        assert(devops_team + "_lead" in userinfo['groups'])

    return(gds_name, devops_team)
