import dataiku

def ProjectValidator(dataiku_client, gds_name): 
    userlist = dataiku_client.list_users()
    for entry in userlist:
        if entry['login'].lower() == gds_name.lower():
        return entry['login']
    raise ValueError('Listed user is not a valid team lead user and can not perform this operation.')