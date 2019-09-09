import dataiku 

from validator.projects import ProjectValidator

class ProjectCreator:
    '''
    ProjectCreator is used by team leads to create pre-configured projects. 
    :param gds_name: team lead's gds credentials. Used for verification & config mapping. 
    :type gds_name: str
    '''

    def __init__(self,gds_name):
        self.client = dataiku.api_client()
        self.gds_name = ProjectValidator(self.client, gds_name)
        
    def create(self):
        print(self.gds_name)