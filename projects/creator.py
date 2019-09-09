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
        '''
        new_project = self.__client.create_project(project_key, project_name, owner=self.gds_name)