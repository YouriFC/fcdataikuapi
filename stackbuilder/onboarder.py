import dataiku 
import re

from ..validator.admin import AdminValidator
from ..groups.ldapgroups import GroupCreator
from ..codeenv.pythonenv import EnvCreator
from ..connections.s3 import S3Creator
from ..connections.redshift import RedshiftCreator


class StackCreator:
    '''
    Used by the platform admin to create a pre-configured all-in-one setup. 
    N.B.: Greenlight the LDAP group in global settings first, or none of this will work! 
    :param gds_name: Admin gds credentials. 
    :param base_ad_group: The AD group that acts as basis for this stack. 
    '''

    def __init__(self, gds_name, base_ad_group):
        #client object for this class to use
        self.__client = dataiku.api_client()

        #Validate user is allowed to do this
        self.gds_name = AdminValidator(self.__client, gds_name)

        assert(base_ad_group in self.__client.get_general_settings().settings['ldapSettings']['authorizedGroups']), 'Whitelist the AD group first / check for ad group typos.'
        self.base_ad_group = base_ad_group
        self.devops_team = base_ad_group.replace('GEN-ZZ-APP-GG-ai-', '').replace('-', '_')

    def create(self, service_account_user, service_account_pw):
        '''
        Creates the whole stack for a specified AD team in one go. 
        N.B.: Greenlight the LDAP group in global settings first, or none of this will work! 
        :param gds_name: Admin gds credentials. 
        :param service_account_user: The username of the Redshift service account
        :param service_account_pw: The password of the Redshift service account. Provided by Terra Alto.      
        '''

        #Groups first
        group_creator = GroupCreator(self.gds_name)
        group_creator.create(self.base_ad_group)

        #Code Env next
        codeenv_creator = EnvCreator(self.gds_name)
        codeenv_creator.create(self.devops_team)

        #S3
        s3_creator = S3Creator(self.gds_name)
        s3_creator.create(self.devops_team)

        #RS
        redshift_creator = RedshiftCreator(self.gds_name)
        redshift_creator.create(self.devops_team, service_account_user, service_account_pw)

        #Proj
        #add this one later, especially since the projectvalidator might be an issue here. 
        



