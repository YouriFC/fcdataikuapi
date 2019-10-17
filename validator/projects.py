import dataiku
import dataikuapi
import re

def ProjectValidator(dataiku_client, gds_name, devops_team): 
    #User stuff
    userlist = [username['login'] for username in dataiku_client.list_users()]
    assert(gds_name.lower() in userlist), "GDS Name does not match code owner"

    userinfo = dataiku_client.get_user(gds_name).get_definition()

    #Group stuff
    grouplist = dataiku_client.list_groups()
    assert(devops_team in [x['name'] for x in grouplist]), "DevOps Team does not exist"
    if "administrators" not in userinfo['groups']:
        assert(devops_team + "_lead" in userinfo['groups'])

    return(gds_name, devops_team)
