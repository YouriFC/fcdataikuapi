import dataiku 
import re

from ..validator.admin import AdminValidator

class S3Creator:
    '''
    S3 is used by the platform admin to create pre-configured s3 connectors. 
    :param gds_name: Admin gds credentials. 
    '''

    def __init__(self, gds_name):
        #client object for this class to use
        self.__client = dataiku.api_client()

        #Validate user is allowed to do this
        self.gds_name = AdminValidator(self.__client, gds_name)
        
    
    def create(self, target_devops_team):
        '''
        Create a new S3 connector. 
        :param target_devops_team: The team for which a new S3 connection needs to be set up.
        '''

        #Quick Check
        assert(target_devops_team.lower() in [x['name'].lower() for x in self.__client.list_groups()]), "Target devops team does not exist."

        #Define standard parameter paylaod
        payload = {'useDefaultCredentials': True,
                'defaultManagedPath': '/dataiku',
                'regionOrEndpoint': 'eu-west-1',
                'hdfsInterface': 'S3A',
                'encryptionMode': 'SSE_S3',
                'chbucket': 'fcdatascience',
                'chroot': target_devops_team,
                'switchToRegionFromBucket': True,
                'customAWSCredentialsProviderParams': [],
                'namingRule': {}}
        #Good to go

        self.__client.create_connection(name='s3_' + target_devops_team,
                                        type='EC2',
                                        params=payload,
                                        usable_by='ALLOWED',
                                        allowed_groups=[target_devops_team, target_devops_team + '_lead']) 

        #And now for the read-only share: 
        payload_shares = {'useDefaultCredentials': True,
                'defaultManagedPath': '/dataiku',
                'regionOrEndpoint': 'eu-west-1',
                'hdfsInterface': 'S3A',
                'encryptionMode': 'SSE_S3',
                'chbucket': 'fcdatascience',
                'chroot': 'shares/' + target_devops_team,
                'switchToRegionFromBucket': True,
                'customAWSCredentialsProviderParams': [],
                'namingRule': {},} #fix this allowWrite isn't enough... also fix the name
        #Good to go

        new_shares_conn = self.__client.create_connection(name='s3_' + target_devops_team + '_shares',
                                        type='EC2',
                                        params=payload_shares,
                                        usable_by='ALLOWED',
                                        allowed_groups=[target_devops_team, target_devops_team + '_lead']) 

        #For now we allow write, too - let's see how it goes
        #env_settings = new_shares_conn.get_definition()
        #env_settings['allowWrite'] = False
        #env_settings['allowManagedDatasets'] = False
        #env_settings['allowManagedFolders'] = False
        #new_shares_conn.set_definition(env_settings)


        print('S3 connections successfully created.')
       