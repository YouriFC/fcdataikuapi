import dataiku 
import re

from ..validator.admin import AdminValidator

class RedshiftCreator:
    '''
    Used by the platform admin to create pre-configured redshift connectors. Note that this will create connectors for all 4 schemas in one go. 
    :param gds_name: Admin gds credentials. 
    :param devops_team: Just for checking purposes. 
    '''

    def __init__(self, gds_name, devops_team):
        #client object for this class to use
        self.__client = dataiku.api_client()

        #Validate user is allowed to do this
        self.gds_name = AdminValidator(self.__client, gds_name, devops_team)

    #Private
    def _single_connection(self, target_devops_team, layer, service_account_user, service_account_pw):
        '''
        Create a single redshift connector in the dev cluster. 
        :param target_devops_team: The team for which Redshift access needs to be set up.
        :param layer: The data warehousing layer for which the connector should be set up. 
        :param service_account_user: The username of the Redshift service account
        :param service_account_pw: The password of the Redshift service account. Provided by Terra Alto.        
        '''

        #Define standard parameter paylaod
        payload = {'port': 5439,
                'iamRole': 'arn:aws:iam::641610760574:role/redshiftbidtanew',
                'host': 'redshiftbidta-redshiftclusterdev-o2vfdr3s4abv.cqzcwvudafse.eu-west-1.redshift.amazonaws.com',
                'user': service_account_user,
                'password': service_account_pw,
                'db': 'dwh',
                'useURL': False,
                'namingRule': {'tableNameDatasetNamePrefix': '${projectKey}_',
                'schemaName': 'ds_' + target_devops_team + '_' + layer,
                'canOverrideSchemaInManagedDatasetCreation': False},
                'schemaSearchPath': 'ds_' + target_devops_team + '_' + layer,
                'useTruncate': False,
                'autocommitMode': False,
                'properties': [{'name': 'ssl', 'value': 'true', 'secret': False}]}     

        self.__client.create_connection(name='rs_' + target_devops_team + '_' + layer,
                                        type='Redshift',
                                        params=payload,
                                        usable_by='ALLOWED',
                                        allowed_groups=[target_devops_team, target_devops_team + '_lead']) 

        print("Created connection at layer {}.".format(layer))

    def create(self, target_devops_team, service_account_user, service_account_pw):
        '''
        Create a new suite of Redshift connectors. 
        :param target_devops_team: The team for which Redshift access needs to be set up.
        :param service_account_user: The username of the Redshift service account
        :param service_account_pw: The password of the Redshift service account. Provided by Terra Alto.
        '''

        #Quick Check
        assert(target_devops_team.lower() in [x['name'].lower() for x in self.__client.list_groups()]), "Target devops team does not exist."

        for current_layer in ['sa', 'dl', 'ds', 'dm']:
            self._single_connection(target_devops_team, current_layer, service_account_user, service_account_pw)

