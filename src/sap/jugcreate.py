
class jugcreate:
    '''
    Used to construct and write the jugfile automatically from
    the provided pipeline.yaml anf application.yaml
    '''
    STANDARD_HEADER = """
from jug import TaskGenerator
from datetime import datetime
from os import environ
import subprocess
"""
    

    def __init__(self, pipeline_yaml, application_yaml, jugfilepath):
        self.pipeline_yaml = pipeline_yaml
        self.application_yaml = application_yaml
        self.jugfilepath = jugfilepath
        self.jugfilenew = False
        print("Building new workflow-manager")
        self.jugfilenew = self.__create_new_file(self.jugfilepath)

        #test
        self.__add_to_jugfile(self.jugfilepath, "hello world")

    
    def __create_new_file(self, filepath):
        '''
        Creates a new blank jugfile by overwriting the previous
        jugfile if it exists.
        '''
        try:
            with open(filepath, 'w') as jf:
                jf.write(self.STANDARD_HEADER)
            return True
        except:
            return False
    
    def __add_to_jugfile(self, filepath, addition):
        try:
            if addition[-1] != '\n':
                addition += '\n'
            with open(filepath, 'a') as jf:
                jf.write(addition)
            return True
        except:
            return False

