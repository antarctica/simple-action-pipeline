import json
import os

class configuration:
    '''
    Used to load and manipulate both the pipeline, and the application configurations.
    '''
    def __init__(self):
        pass

    def json_ingest(self, filepath_in):
        '''
        Ingests JSON data from a valid input filepath.
        '''
        retval = None
        if os.path.exists(filepath_in):
            if os.path.isfile(filepath_in):
                with open(filepath_in) as jsonfile:
                    data_json = json.load(jsonfile)
                    print(data_json)
                    retval = data_json
            else:
                print("!! not a file")
        else:
            print("!! no file")
        
        return retval
    
    def create_envfile(self, json_config):
        '''
        Generates env files for a given json input config. The env file gets
        deposited in the PIPELINE_DIRECTORY and for this reason the 
        PIPELINE_DIRECTORY must be defined in the 'env' section of the json.
        '''
        if 'pipeline' in json_config and 'env' in json_config['pipeline']:
            json_subset = json_config['pipeline']['env']
        elif 'application' in json_config and 'env' in json_config['application']:
            json_subset = json_config['application']['env']
        
        if json_subset:
            if 'create-env-file' in json_subset and \
                     'variables' in json_subset and \
                     json_subset['create-env-file'] == True:
                try:
                    for entry in json_subset['variables']:
                        if 'PIPELINE_DIRECTORY' in entry:
                            outfilename = entry['PIPELINE_DIRECTORY'] \
                                  + '/' + json_subset['env-filename']
                            with open(outfilename, 'w') as file:
                                for line in json_subset['variables']:
                                    for key, val in line.items():
                                        print(f'{key}'+'="'+f'{val}'+'"')
                                        file.write(f'{key}'+'="'+f'{val}'+'"\n')
                                        file.write('export '+f'{key}'+'\n')

                except:
                    print("!! error/undefined PIPELINE_DIRECTORY")



# BASIC guide
# import utils
# c = utils.configuration()
# vals = c.json_ingest("/data/hpcdata/users/matsco/simple-action-pipeline/example/pipeline.json")
# c.create_envfile(vals)  # <- for pipeline.env
# vals = c.json_ingest("/data/hpcdata/users/matsco/simple-action-pipeline/example/application.json")
# c.create_envfile(vals)  # <- for application.env

def add(a, b):
    return a+b

def subtract(a, b):
    return a-b

def mutiply(a, b):
    return a*b

def divide(a, b):
    return a/b
