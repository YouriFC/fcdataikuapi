import dataiku 
import re

from ..validator.projects import ProjectValidator

class ProjectCreator:
    '''
    ProjectCreator is used by team leads to create pre-configured projects. 
    :param gds_name: Your gds credentials. Used for verification & config mapping. 
    :param team: The team for which you'd like to create this projects. You must be team lead. For formatting, refer to DS DevOps teams in OneNote. 
    '''

    def __init__(self, gds_name, devops_team):
        #client object for this class to use
        self.__client = dataiku.api_client()
   

        #Validate user is allowed to do this
        self.gds_name, self.devops_team = ProjectValidator(self.__client, gds_name, devops_team)
        

    def create(self, project_key, project_name):
        '''
        Create a new DataIKU project. 
        :param project_key: The project key is used to reference datasets between projects. It cannot be changed once the project is created.
        :param project_name: The display name of your dataiku project.
        '''
        new_project = self.__client.create_project(project_key, project_name, owner=self.gds_name)

        #Ensure correct group access to project
        #Intentionally hardcoded
        project_permissions = new_project.get_permissions()
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
        new_project.set_permissions(project_permissions)                                    


        ##TODO 


        #Fix project code env in settings
        #Fix selecting correct container
        

