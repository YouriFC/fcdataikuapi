import dataiku 

class Creator:

    def __init__(self,name):
        self.name = name

    def create(self):
        print(self.name)