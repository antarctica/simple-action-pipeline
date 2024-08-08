import yaml
import os

class configuration:
    '''
    Used to load and manipulate both the pipeline, and the application configurations.
    '''
    def __init__(self):
        pass

    def yaml_ingest(self, filepath_in):
        '''
        Ingests YAML data from a valid input filepath.
        '''
        retval = None
        if os.path.exists(filepath_in):
            if os.path.isfile(filepath_in):
                with open(filepath_in) as yamlfile:
                    data_yaml = yaml.safe_load(yamlfile)
                    #print(data_yaml)
                    retval = data_yaml
            else:
                print("!! not a file")
        else:
            print("!! no file")
        
        return retval
    
    def create_envfile(self, yaml_config):
        '''
        Generates env files for a given YAML input config. The env file gets
        deposited in the PIPELINE_DIRECTORY and for this reason the 
        PIPELINE_DIRECTORY must be defined in the 'env' section of the YAML.
        '''
        if 'pipeline' in yaml_config and 'env' in yaml_config['pipeline']:
            yaml_subset = yaml_config['pipeline']['env']
        elif 'application' in yaml_config and 'env' in yaml_config['application']:
            yaml_subset = yaml_config['application']['env']
        
        if yaml_subset:
            if 'create-env-file' in yaml_subset and \
                     'variables' in yaml_subset and \
                     yaml_subset['create-env-file'] == True:
                try:
                    for entry in yaml_subset['variables']:
                        if 'PIPELINE_DIRECTORY' in entry:
                            outfilename = entry['PIPELINE_DIRECTORY'] \
                                  + '/' + yaml_subset['env-filename']
                            with open(outfilename, 'w') as file:
                                for line in yaml_subset['variables']:
                                    for key, val in line.items():
                                        #print(f'{key}'+'="'+f'{val}'+'"')
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
