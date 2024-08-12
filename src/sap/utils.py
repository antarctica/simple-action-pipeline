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
                                
                                # activate the python environment at the end of the env file
                                if 'pipeline' in yaml_config and 'python-env' in yaml_config['pipeline']:
                                    python_env_activate = yaml_config['pipeline']['python-env']
                                    #print(python_env_activate)
                                    file.write('source '+f'{python_env_activate}'+'\n')

                except:
                    print("!! error/undefined PIPELINE_DIRECTORY")

                
class build:
    '''
    Used to build the pipeline from YAML configurations.
    '''
    def __init__(self, configuration_yamls: list):
        self.configs = configuration_yamls
        self.app_pipeline = None
        self.pip_pipeline = None
        self.app_scripts  = None
        for a_config in self.configs:
            self.__check_config(a_config)

    def __directory_exists(self, directory_path):
        '''
        Check to see is a single directory exists.
        '''
        return os.path.isdir(directory_path)

    def __check_config(self, a_yaml):
        '''
        Check that all the scripts referenced in the config yaml exist.
        '''
        this_yaml = a_yaml
        # First check that the pipeline directories are referenced and exists.
        if 'pipeline' in this_yaml or 'application' in this_yaml:
            conf_type = list(this_yaml.keys())[0]
            if 'env' in this_yaml[conf_type] and \
                'variables' in this_yaml[conf_type]['env']:
                yaml_subset = this_yaml[conf_type]['env']['variables']
                #print("it's all there", yaml_subset)
                for a_variable in yaml_subset:
                    if 'PIPELINE_DIRECTORY' in a_variable.keys():
                        if self.__directory_exists(a_variable['PIPELINE_DIRECTORY']):
                            if conf_type == 'application':
                                self.app_pipeline = a_variable['PIPELINE_DIRECTORY']
                            if conf_type == 'pipeline':
                                self.pip_pipeline = a_variable['PIPELINE_DIRECTORY']
                    # Then check that the scripts directory is references and exists.
                    if 'SCRIPTS_DIRECTORY' in a_variable.keys():
                        if self.__directory_exists(a_variable['SCRIPTS_DIRECTORY']):
                            self.app_scripts = a_variable['SCRIPTS_DIRECTORY']
        
        print(self.app_pipeline, self.pip_pipeline, self.app_scripts)

        # Have the essential directories been successfully populated?
        if ( self.pip_pipeline == self.app_pipeline ) and \
             self.app_scripts != None:
            if 'application' in this_yaml:
                if 'sequence' in this_yaml['application']:
                    yaml_subset = this_yaml['application']['sequence']['sequence']
                    print(yaml_subset)


        else:
            print("Unable to validate application.yaml or pipeline.yaml")
            print("Pipeline/Script references may not match or exist.")
        




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
