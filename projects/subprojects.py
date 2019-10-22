import dataiku 
import dataikuapi
import re

from ..validator.projects import ProjectValidator

class SubProject:
    '''
    SubProject is used by team leads to create pre-configured projects. 
    :param gds_name: Your gds credentials. Used for verification & config mapping. 
    :param devops_team: The team for which you'd like to create this projects. You must be team lead. For formatting, refer to DS DevOps teams in OneNote. 
    :param api_key: The API key that has been provided to team leads. 
    '''

    def __init__(self, gds_name, devops_team, apikey):
        #client object for this class to use
        self.__secondary_key = 'ouMfCYAS2Nbgq4BUUXOt3ICL3Q78wIlZ'



        assert(isinstance(apikey, str)), "Ensure your API key is formatted as string."
        self.__client = dataikuapi.DSSClient(host='http://10.189.40.171:8443', api_key=apikey)
   

        #Validate user is allowed to do this
        self.__verification_client = dataikuapi.DSSClient(host='http://10.189.40.171:8443', api_key=self.__secondary_key)
        self.gds_name, self.devops_team = ProjectValidator(self.__verification_client, gds_name, devops_team)
        

    def create(self, project_key, project_name):
        '''
        Create a new DataIKU project. 
        :param project_key: The project key is used to reference datasets between projects. It cannot be changed once the project is created.
        :param project_name: The display name of your dataiku project.
        '''
        new_project = self.__client.create_project(project_key, project_name, owner=self.gds_name)

        #Ensure correct group access to project
        #Intentionally hardcoded
        project_handler = self.__verification_client.get_project(project_key)
        project_permissions = project_handler.get_permissions()
        project_permissions['permissions'].append({
                                                'group': self.devops_team,
                                                'admin': False,
                                                'exportDatasetsData': True,
                                                'manageAdditionalDashboardUsers': False,
                                                'manageDashboardAuthorizations': False,
                                                'manageExposedElements': False,
                                                'moderateDashboards': True,
                                                'readDashboards': True,
                                                'readProjectContent': True,
                                                'runScenarios': True,
                                                'writeDashboards': True,
                                                'writeProjectContent': True
                                            })
        project_permissions['permissions'].append({
                                                'group': self.devops_team + '_lead',
                                                'admin': True,
                                                'exportDatasetsData': True,
                                                'manageAdditionalDashboardUsers': True,
                                                'manageDashboardAuthorizations': True,
                                                'manageExposedElements': True,
                                                'moderateDashboards': True,
                                                'readDashboards': True,
                                                'readProjectContent': True,
                                                'runScenarios': True,
                                                'writeDashboards': True,
                                                'writeProjectContent': True
                                            })
        project_handler.set_permissions(project_permissions)                                    

        #Ensure correct code env & lock
        #Also select correct container before saving changes
        project_settings = project_handler.get_settings()

        #Code Env
        project_settings.settings['settings']['codeEnvs']['python']['useBuiltinEnv'] = False
        project_settings.settings['settings']['codeEnvs']['python']['envName'] = self.devops_team
        project_settings.settings['settings']['codeEnvs']['python']['preventOverride'] = True

        #R Env
        project_settings.settings['settings']['codeEnvs']['r']['useBuiltinEnv'] = False
        project_settings.settings['settings']['codeEnvs']['r']['envName'] = self.devops_team + "_r"
        project_settings.settings['settings']['codeEnvs']['r']['preventOverride'] = True

        #Container
        project_settings.settings['settings']['container']['containerMode'] = 'EXPLICIT_CONTAINER'
        project_settings.settings['settings']['container']['containerConf']= self.devops_team

        #Done
        project_settings.save()

        print("Project creation successful.")

        

