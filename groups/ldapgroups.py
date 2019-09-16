import dataiku 
import re

from ..validator.admin import AdminValidator

class GroupCreator:
    '''
    Used by the platform admin to create pre-configured LDAP groups and permissions. 
    N.B.: Greenlight the LDAP group in global settings first! 
    :param gds_name: Admin gds credentials. 
    '''

    def __init__(self, gds_name):
        #client object for this class to use
        self.__client = dataiku.api_client()

        #Validate user is allowed to do this
        self.gds_name = AdminValidator(self.__client, gds_name)

    def _create_base_group(self, ad_group):
        '''
        Creates the base, non-lead group. 
        :param ad_group: The AD group for which a DataIKU base group needs to be created. 
        '''

        #Basic stuff; we extract everything from our base string. 
        groupname = ad_group.replace('GEN-ZZ-APP-GG-ai-', '').replace('-', '_')
        groupdesc = "User group for project {} for department {}.".format(groupname.split('_')[1], groupname.split('_')[0].upper())

        my_base_group = self.__client.create_group(name=groupname, 
                                                description=groupdesc, 
                                                source_type='LDAP')

        #Now that we have a handle, grab and edit settings
        base_group_settings = my_base_group.get_definition()        

        #Amateur hour but the API doesn't support another way
        base_group_settings['ldapGroupNames'] = ad_group
        base_group_settings['admin'] = False
        base_group_settings['mayManageUDM']= False
        base_group_settings['mayCreateProjects']= False
        base_group_settings['mayWriteUnsafeCode']= True
        base_group_settings['mayWriteSafeCode']= True
        base_group_settings['mayCreateAuthenticatedConnections']= False
        base_group_settings['mayCreateCodeEnvs']= False
        base_group_settings['mayCreateClusters']= False
        base_group_settings['mayDevelopPlugins']= False
        base_group_settings['mayEditLibFolders']= False
        base_group_settings['mayManageCodeEnvs']= False
        base_group_settings['mayManageClusters']= False
        base_group_settings['mayViewIndexedHiveConnections']= False
        base_group_settings['mayCreatePublishedAPIServices']= False

        my_base_group.set_definition(base_group_settings)

        print('Base group created.')

    def _create_lead_group(self, ad_group):
        '''
        Creates the lead group with elevated permissions.
        :param base_ad_group: The AD group for which a DataIKU lead group needs to be created. 
        '''        
        
        #Basic stuff; we extract everything from our base string. 
        groupname = ad_group.replace('GEN-ZZ-APP-GG-ai-', '').replace('-', '_')
        groupdesc = "Lead group for project {} for department {}.".format(groupname.split('_')[1], groupname.split('_')[0].upper())

        my_lead_group = self.__client.create_group(name=groupname, 
                                                description=groupdesc, 
                                                source_type='LDAP')
        #Now that we have a handle, grab and edit settings
        lead_group_settings = my_lead_group.get_definition()        

        #Amateur hour but the API doesn't support another way
        lead_group_settings['ldapGroupNames'] = ad_group
        lead_group_settings['admin'] = False
        lead_group_settings['mayManageUDM']= True
        lead_group_settings['mayCreateProjects']= False
        lead_group_settings['mayWriteUnsafeCode']= True
        lead_group_settings['mayWriteSafeCode']= True
        lead_group_settings['mayCreateAuthenticatedConnections']= False
        lead_group_settings['mayCreateCodeEnvs']= True
        lead_group_settings['mayCreateClusters']= False
        lead_group_settings['mayDevelopPlugins']= True
        lead_group_settings['mayEditLibFolders']= True
        lead_group_settings['mayManageCodeEnvs']= False
        lead_group_settings['mayManageClusters']= False
        lead_group_settings['mayViewIndexedHiveConnections']= False
        lead_group_settings['mayCreatePublishedAPIServices']= False

        my_lead_group.set_definition(lead_group_settings)

        print('Lead group created.')
    
    def create(self, base_ad_group):
        '''
        Create a new duo of groups: lead and normal. 
        :param base_ad_group: The AD group for which a DataIKU group setup needs to be created. 
        '''

        self._create_base_group(base_ad_group)

        self._create_lead_group(base_ad_group + '-lead')

