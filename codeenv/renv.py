import dataiku 
import re

from ..validator.admin import AdminValidator

class REnvCreator:
    '''
    Used by the platform admin to create pre-configured python code envs. 
    :param gds_name: Admin gds credentials. 
    '''

    def __init__(self, gds_name):
        #client object for this class to use
        self.__client = dataiku.api_client()

        #Validate user is allowed to do this
        self.gds_name = AdminValidator(self.__client, gds_name)
        
    def create(self, target_devops_team):
        '''
        Create a new Python code environment. 
        :param target_devops_team: The team for which a code env needs to be created. Team lead group will automatically be added. 
        '''
        assert(target_devops_team.lower() in [x['name'].lower() for x in self.__client.list_groups()]), "Target devops team does not exist."

        payload = {
            'installCorePackages': True,
            'installJupyterSupport': True,
            'conda': False,
        }

        print('Creating a new R environment. This can take a long time...')
        new_code_env = self.__client.create_code_env(env_lang="R", 
                                                    env_name=target_devops_team + "_r",
                                                    deployment_mode="DESIGN_MANAGED", 
                                                    params=payload)
        
        #Applying settings to a code env is a post-creation task. 
        env_settings = new_code_env.get_definition()
        env_settings['usableByAll'] = False

        #Lead group
        env_settings['permissions'].append({'group': target_devops_team + '_lead',
                                            'update': True,
                                            'use': True,
                                            'manageUsers': False})
        env_settings['permissions'].append({'group': target_devops_team,
                                            'update': False,
                                            'use': True,
                                            'manageUsers': False})

        #Save
        new_code_env.set_definition(env_settings)
        print("Code env {} created.".format(target_devops_team + "_r"))



