import dataiku 
import operator

class ProjectCreator:
    '''
    ProjectCreator is used by team leads to create pre-configured projects. 
    :param gds_name: team lead's gds credentials. Used for verification & config mapping. 
    :type gds_name: str
    '''

    def __init__(self,gds_name):
        self.client = dataiku.api_client()
        self.gds_name = gds_name

        gds_name = property(operator.attrgetter('_gds_name'))

        @gds_name.setter
        def gds_name(self, gdn):
            userlist = self.client.list_users()
            assert(gdn.lower() in [x['login'].lower() for x in userlist])
            self._gds_name = gdn

    def create(self):
        print(self.gds_name)