#!/usr/bin/env python

# Version: 2024-87-06: First version
#
# Author: matsco@bas.ac.uk
#
# Main pipeline package that users interact with.

import argparse
import os
import glob
import time
import subprocess
from sap import utils
from sap.setup_logging import logger

def initial_check(provided_fullpath):
    '''
    Check the provided directory to determine if it is a pipeline.
    An unbuilt pipeline will have yaml files but no wf directory.
    '''
    try:
        # are there yaml files?
        if os.path.isfile(provided_fullpath + 'application.yaml') and \
           os.path.isfile(provided_fullpath + 'pipeline.yaml'):
            # is there a workflow-manager directory?
            if os.path.isdir(provided_fullpath + 'workflow-manager/'):
                # is there a python file in the workflow-manager?
                if len(glob.glob(provided_fullpath + 'workflow-manager/*.py')) > 0:
                    retval = 'built'
                else:
                    retval = 'unbuilt'
            else:
                retval = 'unbuilt'
        else:
            retval = 'unknown'  
    except:
        logger.error("Could not determine status of provided pipeline directory")
        exit(1)
    return retval

def perform_decision(pipeline_type, action, pipeline_fullpath, rebuild, short):
    if (pipeline_type == 'unbuilt'):
        if (action == 'build'):
            logger.info("Build process started")
            conf = utils.configuration()
            logger.info("Loading configuration files")
            yaml_pipeline = conf.yaml_ingest(pipeline_fullpath + 'pipeline.yaml')
            yaml_application = conf.yaml_ingest(pipeline_fullpath + 'application.yaml')
            logger.info("Creating .env files")
            conf.create_envfile(yaml_pipeline, pipeline_fullpath + 'pipeline.yaml')
            conf.create_envfile(yaml_application, pipeline_fullpath + 'application.yaml')
            bld_pipeline = utils.build(pipeline_fullpath, [yaml_pipeline, yaml_application])
            if bld_pipeline.build_ready == True:
                pipeline_type = 'built'
        else:
            logger.info("The pipeline does not appear to be built.")
            logger.info("Please run the pipeline build command. see pipeline --help")
            exit(1)
        
    elif (pipeline_type == 'built'):
        # here I need to use the environment files to set environment
        # variables if they dont yet exist.
        if (action == 'build'):
            if rebuild:
                logger.info("The pipeline is already built - Forcing rebuild")
                resp = 'Y'
            else:
                logger.info("Rebuild decision required.")
                resp = input('The pipeline is already built, would you like to rebuild it? ')
            if resp == 'Y' or resp == 'y':
                perform_decision('unbuilt', 'build', pipeline_fullpath, True)
        
        elif (action == 'status'):
            extra_arg = ''
            if short:
                extra_arg = '--short'
            current = os.getcwd()
            os.chdir(pipeline_fullpath + 'workflow-manager')
            if len(glob.glob('*.py')) == 1:
                subprocess.call(["jug", "status",
                                 str(glob.glob('*.py')[0]), extra_arg])
            os.chdir(current)
        
        elif (action == 'execute'):
            current = os.getcwd()
            os.chdir(pipeline_fullpath + 'workflow-manager')
            maxwork = int(os.environ['PIPELINE_MAXWORKERS'])
            if len(glob.glob('*.py')) == 1:
                check = subprocess.call(["jug", "check",
                                 str(glob.glob('*.py')[0])])
                if check == 0:  # If all tasks have already completed
                    logger.info("All Tasks complete, nothing to do")
                    logger.info("Use the [reset] command before re-executing a completed pipeline")
                #logger.info(str(os.listdir()[0]))
                else:
                    logger.info("Executing pipeline "+glob.glob('*.py')[0]+
                                " ; Workers="+str(maxwork))
                    worker_procs = [] # store which processes are launched
                    for _ in range(maxwork):
                        p = subprocess.Popen(["jug", "execute", str(glob.glob('*.py')[0])])
                        worker_procs.append(" "+str(p.pid))
                        time.sleep(0.25)
                    with open(".workers", "a") as w:
                        w.writelines(worker_procs)
            os.chdir(current)
        
        elif (action == 'reset'):
            current = os.getcwd()
            os.chdir(pipeline_fullpath + 'workflow-manager')
            logger.info("Resetting pipeline state")
            if len(glob.glob('*.py')) == 1:
                utils.reset_pipeline(pipeline_fullpath +
                            'workflow-manager/'+str(glob.glob('*.py')[0]))
                subprocess.call(["jug", "status", str(glob.glob('*.py')[0])])
                logger.info("Reset complete")
                logger.info("Ready to execute")
            os.chdir(current)
        
        elif (action == 'halt'):
            current = os.getcwd()
            os.chdir(pipeline_fullpath + 'workflow-manager')
            logger.info("Halting the pipeline")
            if len(glob.glob('*.py')) == 1:
                utils.halt_pipeline(pipeline_fullpath +
                            'workflow-manager/'+str(glob.glob('*.py')[0]))
                subprocess.call(["jug", "status", str(glob.glob('*.py')[0])])
                logger.info("Halt complete")
            os.chdir(current)


def perform(pipeline_directory, action, rebuild, short):
    if type(pipeline_directory) != type(list):
        pipeline_directory = [pipeline_directory]
    # The first element of pipeline_directory should always be the
    # directory path, everything after that is additional arguments

    # First handle relative and absolute paths sensibly
    try:
        if ''.join(pipeline_directory[0])[0] == '.':
            pipeline_fullpath = (os.getcwd()+''.join(pipeline_directory[0]).replace('.',''))
        elif ''.join(pipeline_directory[0])[0] == '/':
            pipeline_fullpath = (''.join(pipeline_directory[0]))
        elif ''.join(pipeline_directory[0]) == '.':
            pipeline_fullpath = (os.getcwd()+'/')
        else:
            pipeline_fullpath = (os.getcwd()+'/'+''.join(pipeline_directory[0]).replace('.',''))
        if pipeline_fullpath[-1] != '/':
            pipeline_fullpath += '/'
        logger.info("Target: %s", pipeline_fullpath)
    except:
        logger.error("Unrecognised pipeline directory path")
        exit(1)

    pipeline_type = initial_check(pipeline_fullpath)
    logger.info("Pipeline Status: %s", pipeline_type)
    perform_decision(pipeline_type, action, pipeline_fullpath, rebuild, short)
    #logger.info(action+": Finished")
 
def main():
    """
    pipeline entry point
    this entry point relies on being pointed to a pipeline directory
    """
    
    parser = argparse.ArgumentParser(description='perform action with simple-action-pipeline by supplying a pipeline directory')
    parser.add_argument("action", help="Action for the pipeline to perform. \
                        options are 'build', 'status', 'execute', 'reset', 'halt'.", \
                            type=str, choices=['build', 'status', 'execute', 'reset', 'halt'])
    parser.add_argument("pipeline_directory", help="Pipeline directory to use", nargs="*", default="./")
    parser.add_argument("-d", "--directory", help="Pipeline directory", action="store", dest='pipedir')
    parser.add_argument("-f", "--force-rebuild", help="Force building the pipeline that is already built.", action="store_true", dest='rebuild', default=False)
    parser.add_argument("-s", "--short", help="Output shortened information where supported", action="store_true", dest='short', default=False)
    args = parser.parse_args()


    # Now kick off main

    # What to do if no pipeline directory was supplied
    if (not args.pipedir) and (not args.pipeline_directory):
        logger.warning("No pipeline directory provided. Attempting to use current directory as pipeline.")

    # Keyword switch takes priority over positional switch
    if (args.pipedir):
        args.pipeline_directory = args.pipedir
    
    perform(args.pipeline_directory, args.action, args.rebuild, args.short)


if __name__ == "__main__":
    main()
