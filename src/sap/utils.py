import yaml
import os
import jugcreate

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
        self.pipeline_yaml = None
        self.application_yaml = None
        self.wfman = 'workflow-manager'
        self.app_pipeline = None
        self.pip_pipeline = None
        self.app_scripts  = None
        self.build_ready  = False

        for a_config in self.configs:
            self.__check_config(a_config)
        if self.__pre_build_check():
            self.build_ready = self.__build_workflow_manager()

    def __configure_jug(self):
        '''
        The Jug package is automatically configured for
        consistent behaviour across pipelines.
        '''
        try:
            #re-write the user's jugrc config file
            os.system("mkdir -p $HOME/.config")
            os.system("echo $'[main]\njugdir=recent.%(jugfile)s\nwill_cite=True\n' > $HOME/.config/jugrc")
            retval = True
        except:
            print("Unable to configure underlying workflow manager")
            retval = False
        return retval

    def __construct_jugfile(self):
        '''
        Using the provided pipeline.yaml and application.yaml, construct
        and write the jugfile
        '''
        for single_config in self.configs:
            if 'pipeline' in single_config.keys():
                self.pipeline_yaml = single_config
            elif 'application' in single_config.keys():
                self.application_yaml = single_config
            else:
                pass
        
        pipeyaml = self.pipeline_yaml; appyaml = self.application_yaml

        if self.pipeline_yaml != None and self.application_yaml != None:
            jugfile_name = pipeyaml['pipeline']['name'] + '-' + \
            appyaml['application']['name'] + '.py'
            print(self.pip_pipeline + '/' + self.wfman + '/' + jugfile_name)
            test = jugcreate.jugcreate(self.configs, (self.pip_pipeline + '/' + self.wfman + '/' + jugfile_name) )
        return True

    def __build_workflow_manager(self):
        '''
        Build the workflow-manager directory from scratch.
        '''
        try: 
            if self.__directory_exists(self.pip_pipeline + '/' + self.wfman):
                print("Erasing previous workflow-manager")
                command = 'rm -rf ' + self.pip_pipeline + '/' + self.wfman
                os.system(command)
            
            os.mkdir(self.pip_pipeline + '/' + self.wfman)
            # Standardise the configuration of JUG.
            if ( self.__configure_jug() != True ):
                retval = False
            else:
                # construct and write the jugfile
                retval = self.__construct_jugfile()

        except:
            retval = False
        
        return retval

    def __pre_build_check(self):
        '''
        Once the config(s) have been loaded, we check that everything
        is ready for the build process.
        '''
        if ( self.app_pipeline == self.pip_pipeline ):
            retval = False
            if ( self.app_scripts != None ):
                print("Ready to build workflow-manager")
                retval = True
        return retval

    def __directory_exists(self, directory_path):
        '''
        Check to see is a single directory exists.
        '''
        return os.path.isdir(directory_path)

    def __file_exists(self, file_path):
        '''
        Check to see is a single file exists.
        '''
        return os.path.isfile(file_path)

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
        
        #print(self.app_pipeline, self.pip_pipeline, self.app_scripts)

        # Have the essential directories been successfully populated?
        if ( self.pip_pipeline == self.app_pipeline ) and \
             self.app_scripts != None:
            if 'application' in this_yaml:
                if 'sequence' in this_yaml['application']:
                    yaml_subset = this_yaml['application']['sequence']['sequence']
                    #print(yaml_subset)
                    # Make a list of all the scripts
                    script_list = []
                    for a_script in yaml_subset:
                        if 'script' in a_script:
                            sub_script = a_script['script']
                            if 'name' in sub_script:
                                if sub_script['name'] not in script_list:
                                    script_list.append(sub_script['name'])
                            if 'depends' in sub_script:
                                if type(sub_script['depends']) != type(list()):
                                    if sub_script['depends'] not in script_list \
                                         and sub_script['depends'] != '' :
                                        script_list.append(sub_script['depends'])
                                else:
                                    for depend in sub_script['depends']:
                                        if depend not in script_list and depend != '':
                                            script_list.append(depend)
                    # Now check existence for each script file
                    all_scripts = [ self.__file_exists(self.app_scripts+'/'+a_file) for a_file in script_list ]
                    #print(all_scripts)
                    if False in all_scripts:
                        self.app_scripts = None
                        print("Unable to validate application.yaml")
                        print("One or more script references unresolved")
                    else:
                        # Everything checks out so far so lets build the workflow manager.
                        print('Configuration Checks Complete')

        




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
