import yaml
import os
import glob
import shutil
import psutil
import subprocess
from pathlib import Path
from time import sleep
from signal import SIGKILL
from sap.jugcreate import jugcreate
from sap.setup_logging import logger

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
                    logger.info("Loaded configuration: %s", filepath_in)
                    retval = data_yaml
            else:
                logger.error("Path %s is not a file.")
                exit(1)
        else:
            logger.error("Path %s does not exist.")
        return retval
    
    def create_envfile(self, yaml_config, yaml_fullpath):
        '''
        Generates env files for a given YAML input config. The env file gets
        deposited in the PIPELINE_DIRECTORY and for this reason the 
        PIPELINE_DIRECTORY must be defined in the 'env' section of the YAML.
        '''
        # test for current directory in case of relative path.
        p = Path(yaml_fullpath)

        if 'pipeline' in yaml_config and 'env' in yaml_config['pipeline']:
            yaml_subset = yaml_config['pipeline']['env']
        elif 'application' in yaml_config and 'env' in yaml_config['application']:
            yaml_subset = yaml_config['application']['env']
        
        if yaml_subset:
            if 'create-env-file' in yaml_subset and \
                     'variables' in yaml_subset and \
                     yaml_subset['create-env-file'] == True:
                try:
                    prev_cwd = Path().resolve()
                    os.chdir(p.parents[0])
                    for entry in yaml_subset['variables']:
                        if 'PIPELINE_DIRECTORY' in entry:
                            outfilename = entry['PIPELINE_DIRECTORY'] \
                                  + '/' + yaml_subset['env-filename']
                            with open(outfilename, 'w') as file:
                                for line in yaml_subset['variables']:
                                    for key, val in line.items():
                                        #print(f'{key}'+'="'+f'{val}'+'"')
                                        if key == 'PIPELINE_DIRECTORY' or key == 'SCRIPTS_DIRECTORY':
                                            this_p = Path(f'{val}').resolve()
                                            file.write(f'{key}'+'="'+f'{this_p}'+'"\n')
                                        else:
                                            file.write(f'{key}'+'="'+f'{val}'+'"\n')
                                        file.write('export '+f'{key}'+'\n')
                                
                                # # activate the python environment at the end of the env file
                                # if 'pipeline' in yaml_config and 'python-env' in yaml_config['pipeline']:
                                #     python_env_activate = yaml_config['pipeline']['python-env']
                                #     #print(python_env_activate)
                                #     file.write('source '+f'{python_env_activate}'+'\n')
                except:
                    logger.error("!! error/undefined PIPELINE_DIRECTORY")
                finally:
                    os.chdir(prev_cwd)

                
class build:
    '''
    Used to build the pipeline from YAML configurations.
    '''
    def __init__(self, directory, configuration_yamls: list):
        self.root_fullpath = directory
        self.configs = configuration_yamls
        self.pipeline_yaml = None
        self.application_yaml = None
        self.wfman = 'workflow-manager'
        self.app_pipeline = None
        self.pip_pipeline = None
        self.app_scripts  = None
        self.build_ready  = False

        for a_config in self.configs:
            self.__check_config(a_config, self.root_fullpath)
        if self.__pre_build_check():
            self.build_ready = self.__build_workflow_manager()
        # if self.build_ready:
        #     self.__create_graph()

    def __create_graph(self):
        current = os.getcwd()
        os.chdir(self.pip_pipeline + "/" + self.wfman)
        if len(glob.glob('*.py')) == 1:
            subprocess.call(["jug", "graph",
                            str(glob.glob('*.py')[0])])
            sleep(0.5)
        os.remove(str(glob.glob('*.dot')[0]))
        os.chdir(current)

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
            logger.error("Unable to configure JUG workflow manager")
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
            jugcreate(self.pipeline_yaml, self.application_yaml, \
                (self.pip_pipeline + '/' + self.wfman + '/' + jugfile_name) )
        return True

    def __build_workflow_manager(self):
        '''
        Build the workflow-manager directory from scratch.
        '''
        try: 
            if self.__directory_exists(self.pip_pipeline + '/' + self.wfman):
                logger.info("Erasing any previous workflow-manager")
                shutil.rmtree(self.pip_pipeline + '/' + self.wfman)
            
            os.mkdir(self.pip_pipeline + '/' + self.wfman)
            # Standardise the configuration of JUG.
            logger.info("Configuring JUG workflow manager for standard behaviour.")

            if ( self.__configure_jug() != True ):
                logger.warning("Unable to configure JUG with ~/.config/jugrc file.")
                retval = False

            else:
                # construct and write the jugfile
                logger.info("Building workflow manager from configuration files.")
                retval = self.__construct_jugfile()

        except:
            logger.error("Failed to successfully build the workflow manager")
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
                logger.info("Preparing to build workflow-manager")
                retval = True
            else:
                logger.error("No application scripts defined. Aborting build.")
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

    def __check_config(self, a_yaml, rootdir):
        '''
        Check that all the scripts referenced in the config yaml exist.
        '''
        this_dir = Path(rootdir)
        prev_dir = Path().resolve()
        os.chdir(this_dir)
        this_yaml = a_yaml
        logger.info("Checking %s configuration file.", tuple(this_yaml.keys())[0])
        # First check that the pipeline directories are referenced and exists.
        if 'pipeline' in this_yaml or 'application' in this_yaml:
            conf_type = list(this_yaml.keys())[0]
            if 'env' in this_yaml[conf_type] and \
                'variables' in this_yaml[conf_type]['env']:
                yaml_subset = this_yaml[conf_type]['env']['variables']
                #print("it's all there", yaml_subset)
                for a_variable in yaml_subset:
                    if 'PIPELINE_DIRECTORY' in a_variable.keys():
                        if self.__directory_exists(Path(a_variable['PIPELINE_DIRECTORY']).resolve()):
                            if conf_type == 'application':
                                self.app_pipeline = str(Path(a_variable['PIPELINE_DIRECTORY']).resolve())
                            if conf_type == 'pipeline':
                                self.pip_pipeline = str(Path(a_variable['PIPELINE_DIRECTORY']).resolve())
                    # Then check that the scripts directory is references and exists.
                    if 'SCRIPTS_DIRECTORY' in a_variable.keys():
                        if self.__directory_exists(Path(a_variable['SCRIPTS_DIRECTORY']).resolve()):
                            self.app_scripts = str(Path(a_variable['SCRIPTS_DIRECTORY']).resolve())

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

                    if False in all_scripts:
                        self.app_scripts = None
                        logger.error("Unable to validate application configuration file")
                        logger.error("One or more script references unresolved")
                        exit(1)
                    else:
                        # Everything checks out so far so lets build the workflow manager.
                        logger.info("Configuration Checks Complete")
        # exit without changing path
        os.chdir(prev_dir)

def reset_pipeline(jugfilepath):
    name = Path('recent.'+str(Path(jugfilepath).stem))
    directory = Path(jugfilepath).parent
    try:
        if os.path.isdir(Path.joinpath(directory, name)):
            shutil.rmtree(Path.joinpath(directory, name))
            os.remove(Path.joinpath(directory, ".workers"))
    except:
        logger.error("Unable to reset pipeline - cannot modify workflow-manager")

def check_max_workers(max_workers, jugfilepath):
    '''
    With the max_workers provided, deduce how many workers are currently working
    on the pipeline and thus how many more workers to create to stay below the
    max_workers limit.
    '''
    # Load the workers file
    directory = Path(jugfilepath).parent
    with open(Path.joinpath(directory, ".workers")) as w:
        workers = w.readlines()
    workers = ''.join([pid for line in workers for pid in line])
    workers = workers.split(" ")
    print(workers)
    running_workers = []
    # Count how many workers are still working
    for worker in workers:
        if psutil.exists(worker):
            running_workers.append(worker)
    print(len(running_workers))
    # Subtract any running workers from the maximum allowed
    workers_to_create = max_workers - len(running_workers)
    return workers_to_create

def halt_pipeline(jugfilepath):
    directory = Path(jugfilepath).parent
    try:
        if os.path.isfile(Path.joinpath(directory, ".workers")):
            with open(Path.joinpath(directory, ".workers")) as w:
                workers = w.readlines()
            workers = ''.join([pid for line in workers for pid in line])
            workers = workers.split(" ")
            print(workers)
            for pid in workers:
                if pid != '':
                    try:
                        subprocess.call(["kill", pid])
                    except Exception as e:
                        logger.error(e)
                        logger.warning("Worker %s no longer running", pid)
            os.remove(Path.joinpath(directory, ".workers"))
    except:
        logger.error("Unable to halt pipeline - cannot release workers")

def populate_env_variables(environment_file):
    '''
    Clears any pre-existing environment variables of the same
    name, then populates them from the env file into the environment.
    '''
    try:
        with open(environment_file) as envfile:
            filelines = envfile.readlines()
        filelines = [variable.strip('\n') for variable in filelines if 'export' not in variable]
        for envvar in filelines:
            (name, value) = envvar.split('=')
            try:
                _ = os.environ[str(name)]
                os.environ.pop(name)
                os.environ[str(name)] = str(value).strip('"')
            except KeyError:
                os.environ[str(name)] = str(value).strip('"')
    except Exception as e:
        logger.error(e)
