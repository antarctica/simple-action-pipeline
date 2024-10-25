# Creates a new jugfile from the provided pipeline and application YAML
# files. This will overwrite any pre-existing  jugfile in the
# ./workflow_manager/ directory of the same name.

from pathlib import Path
from sap.setup_logging import logger

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
import time
"""
    STANDARD_PSTART = """
@TaskGenerator
def _00_start_pipeline():
    time.sleep(0.5)
    print("INFO:"+str(datetime.now()), "| started pipeline")
    subprocess.call('jug status ' + '/workflow-manager/', shell=True) 
    return datetime.now()
"""

    STANDARD_PFINISH = """
@TaskGenerator
def _00_finish_pipeline(finish_times: list):
    time.sleep(0.5)
    print("INFO:"+str(datetime.now()), "| finished pipeline")
    subprocess.call('jug status ' + '/workflow-manager/', shell=True)  
    return datetime.now()
"""   

    def __init__(self, pipeline_yaml, application_yaml, jugfilepath):
        self.pipeline_yaml = pipeline_yaml
        self.application_yaml = application_yaml
        self.jugfilepath = jugfilepath
        self.jugfilenew = False
        self.tasknumber = 0
        logger.info("Building new workflow-manager")
        self.jugfilenew = self.__create_new_file(self.jugfilepath)
        logger.info("Writing JUGfile %s ", Path(jugfilepath).name)
        self.__task_start_finish(self.tasknumber, self.jugfilepath)
        self.jugtasks = self.__task_extract(self.application_yaml)
        self.__task_write(self.jugfilepath, self.jugtasks)
        self.__task_start_finish(self.tasknumber, self.jugfilepath)
        self.__start_exec(self.jugfilepath)
        self.__task_exec(self.jugfilepath, self.jugtasks)
        logger.info("Exiting build process.")

    
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
        '''
        Adds one or more lines to the current jugfile being written.
        '''
        try:
            if addition[-1] != '\n':
                addition += '\n'
            with open(filepath, 'a') as jf:
                jf.write(addition)
            return True
        except:
            return False
        
    def __task_start_finish(self, tasknum, jugfilepath):
        '''
        Populates additional start and end tasks into the
        workflow-manager jugfile.
        '''
        if tasknum == 0:
            wrt_data = self.STANDARD_PSTART
        else:
            wrt_data = self.STANDARD_PFINISH.replace( \
                        '_00_', '_'+f"{tasknum+1:02d}"+'_')
            wrt_data = wrt_data + '\n'
        
        wrt_data = wrt_data.replace("'/workflow-manager/'",
                "pipeline_directory + '/workflow-manager/" + Path(jugfilepath).name + "'")
        self.__add_to_jugfile(jugfilepath, wrt_data)

    def __start_exec(self, jugfilepath):
        self.__add_to_jugfile(jugfilepath, "pipeline_directory = environ['PIPELINE_DIRECTORY']\n")
        self.__add_to_jugfile(jugfilepath, "scripts_directory = environ['SCRIPTS_DIRECTORY']\n\n")
        self.__add_to_jugfile(jugfilepath, "start_output = _00_start_pipeline()")
        self.__add_to_jugfile(jugfilepath, "\nif start_output:\n")
    
    def __task_exec(self, jugfilepath, jugtasks):
        # make the first real task depend on the start pipeline task
        newtasks = []
        for task in jugtasks:
            if len(task) < 3:
                subtask = task + ['start_output']
            else:
                subtask = task
            newtasks.append(subtask)
        # write each task execution to the jugfile
        for next, task in enumerate(newtasks):
            dependencies = ''
            for dep in task[2:]:
                dependencies += str(dep + ', ')
            wrt_data  = "    " + task[0].replace('.','_') + "_output = "
            wrt_data += task[1] + "([" + dependencies + "])\n\n"
            self.__add_to_jugfile(jugfilepath, wrt_data)
            # construct the if statements
            if next <= len(newtasks) - 2:
                nextif = newtasks[next + 1][2:]
                if len(nextif) == 1:
                    self.__add_to_jugfile(jugfilepath, "if " + nextif[0] + ":\n")
                else:
                    multideps = ''
                    for dependency_single in nextif:
                        multideps += str(dependency_single + ' and ')
                    multideps = multideps[:-5]
                    self.__add_to_jugfile(jugfilepath, "if " + multideps + ":\n")

        # after the real tasks, add the finish task
        all_scripts = [task[0].replace('.','_')+'_output' for task in newtasks] # list all script names
        all_dependencies = [dep for row in newtasks for dep in row[2:]] # list all dependencies
        final_dependencies = [orphan for orphan in all_scripts if orphan not in all_dependencies]
        finaldeps = ''
        if len(final_dependencies) == 1:
                    self.__add_to_jugfile(jugfilepath, "if " + final_dependencies[0] + ":\n")
                    finaldeps += str(final_dependencies[0] + ', ')
        else:
            multideps = ''
            for dependency_single in final_dependencies:
                multideps += str(dependency_single + ' and ')
                finaldeps += str(dependency_single + ', ')
            multideps = multideps[:-5]
            self.__add_to_jugfile(jugfilepath, "if " + multideps + ":\n")
        self.__add_to_jugfile(jugfilepath, "    _" + f"{self.tasknumber+1:02d}" +
                              "_finish_pipeline([" + finaldeps + "])\n")


    def __task_extract(self, yaml) -> list:
        '''
        Extracts the information needed to create individual jug
        tasks. Including, script name, reference and dependencies.
        '''
        try:
            seq = yaml['application']['sequence']['sequence']
            seq_out = []
            for n, script in enumerate(seq):
                self.tasknumber = n + 1
                tmp_list = []
                tmp_list.append(script['script']['name'])
                tmp_list.append('_'+f"{n+1:02d}"+'_'+script['script']['name'].replace('.', '_'))
                d = script['script']['depends']
                if type(d) == type(''):
                    d = [d,]
                for dep in d:
                    if dep != '':
                        tmp_list.append(dep.replace('.', '_')+'_output')
                seq_out.append(tmp_list)
        except:
            seq_out = []
        return seq_out
    
    def __task_write(self, filepath, tasklist):
        try:
            for a_task in tasklist:
                if a_task[0].endswith('.sh'):
                    exe_type = 'bash'
                elif a_task[0].endswith('.py'):
                    exe_type = 'python'
                else:
                    exe_type = 'bash'
                self.__add_to_jugfile(filepath, 
                  '\n@TaskGenerator\ndef '+a_task[1]+'(finish_times: list):\n')
                self.__add_to_jugfile(filepath,
                  '    print("INFO:"+str(datetime.now())+":pipeline:Task: '+a_task[1]+' started.")')
                self.__add_to_jugfile(filepath,
                  "    returncode = subprocess.call('"+exe_type+" ' + scripts_directory + " +
                  "'/"+a_task[0]+"', shell=True)\n")
                self.__add_to_jugfile(filepath,
                  '    if returncode != 0: raise RuntimeError("Task: '+a_task[1]+' failed")\n')
                self.__add_to_jugfile(filepath,
                  '    print("INFO:"+str(datetime.now())+":pipeline:Task: '+a_task[1]+' finished.")')
                self.__add_to_jugfile(filepath, 
                  '    return datetime.now()\n')

        except:
            pass

