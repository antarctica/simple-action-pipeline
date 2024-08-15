
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
    STANDARD_PSTART = """
@TaskGenerator
def _00_start_pipeline():
    print(datetime.now(), "| started pipeline")
    subprocess.call('jug status ' + '/workflow-manager/', shell=True) 
    return datetime.now()
"""

    STANDARD_PFINISH = """
@TaskGenerator
def _00_finish_pipeline():
    print(datetime.now(), "| finished pipeline")
    subprocess.call('jug status ' + '/workflow-manager/', shell=True)  
    return datetime.now()
"""   

    def __init__(self, pipeline_yaml, application_yaml, jugfilepath):
        self.pipeline_yaml = pipeline_yaml
        self.application_yaml = application_yaml
        self.jugfilepath = jugfilepath
        self.jugfilenew = False
        self.tasknumber = 0
        print("Building new workflow-manager")
        self.jugfilenew = self.__create_new_file(self.jugfilepath)
        self.__task_start_finish(self.tasknumber, self.jugfilepath)
        self.jugtasks = self.__task_extract(self.application_yaml)
        self.__task_write(self.jugfilepath, self.jugtasks)
        self.__task_start_finish(self.tasknumber, self.jugfilepath)
        self.__start_exec(self.jugfilepath)
        self.__task_exec(self.jugfilepath, self.jugtasks)

    
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
            wrt_data = wrt_data + '\n\n'
        
        wrt_data = wrt_data.replace('/workflow-manager/',
                                            jugfilepath)
        self.__add_to_jugfile(jugfilepath, wrt_data)

    def __start_exec(self, jugfilepath):
        self.__add_to_jugfile(jugfilepath, "pipeline_directory = environ['PIPELINE_DIRECTORY']")
        self.__add_to_jugfile(jugfilepath, "start_output = _00_start_pipeline()")
        self.__add_to_jugfile(jugfilepath, "\nif start_output:\n")
    
    def __task_exec(self, jugfilepath, jugtasks):
        '''
        if results:
            downcomplete = _03check_downloads_complete([results, ])
        '''
        newtasks = []
        for task in jugtasks:
            print(len(task))
            if len(task) < 3:
                subtask = task + ['start_output']
            else:
                subtask = task
            print(subtask)
            newtasks.append(subtask)
        
        for task in newtasks:
            wrt_data  = "    " + task[0].replace('.','_') + "_output = "
            wrt_data += task[1] + "([])\n"
            self.__add_to_jugfile(jugfilepath, wrt_data)
        
        print(newtasks)


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
                self.__add_to_jugfile(filepath, 
                  '\n@TaskGenerator\ndef '+a_task[1]+'(finish_times: list):\n')
                self.__add_to_jugfile(filepath,
                  '    print(datetime.now(), "| started '+a_task[1]+'")\n')
                self.__add_to_jugfile(filepath,
                  "    subprocess.call('bash ' + pipeline_directory + " +
                  "'/scripts/"+a_task[0]+"', shell=True)\n")
                self.__add_to_jugfile(filepath,
                  '    print(datetime.now(), "| finished '+a_task[1]+'")\n')
                self.__add_to_jugfile(filepath, 
                  '    return datetime.now()\n')

        except:
            pass

