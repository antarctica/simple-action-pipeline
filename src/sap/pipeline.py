#!/usr/bin/env python

# Version: 2024-87-06: First version
#
# Author: matsco@bas.ac.uk
#
# Main pipeline package that users interact with.

import argparse
import os
import glob
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

def perform_decision(pipeline_type, action, pipeline_fullpath, rebuild):
    if (pipeline_type == 'unbuilt'):
        if (action == 'build'):
            logger.info("Build process started")
            conf = utils.configuration()
            logger.info("Loading configuration files")
            yaml_pipeline = conf.yaml_ingest(pipeline_fullpath + 'pipeline.yaml')
            yaml_application = conf.yaml_ingest(pipeline_fullpath + 'application.yaml')
            logger.info("Creating .env files")
            conf.create_envfile(yaml_pipeline)
            conf.create_envfile(yaml_application)
            bld_pipeline = utils.build([yaml_pipeline, yaml_application])
        else:
            logger.info("The pipeline does not appear to be built.")
            logger.info("Please run the pipeline build command. see pipeline --help")
            exit(1)
        
    if (pipeline_type == 'built'):
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
            current = os.getcwd()
            os.system("source %s/pipeline.env" % pipeline_fullpath)
            os.system("source %s/application.env" % pipeline_fullpath)
            os.chdir(pipeline_fullpath + '/workflow-manager')
            if len(glob.glob('*.py')) == 1:
                logger.info(str(os.listdir()[0]))
                subprocess.call(["jug", "status", str(os.listdir()[0])])
            os.chdir(current)

def perform(pipeline_directory, action, rebuild):
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
    perform_decision(pipeline_type, action, pipeline_fullpath, rebuild)
    logger.info("Pipeline Status: %s", pipeline_type)
    logger.info("Finished")
 
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
    args = parser.parse_args()


    # Now kick off main

    # What to do if no pipeline directory was supplied
    if (not args.pipedir) and (not args.pipeline_directory):
        logger.warning("No pipeline directory provided. Attempting to use current directory as pipeline.")

    # Keyword switch takes priority over positional switch
    if (args.pipedir):
        args.pipeline_directory = args.pipedir
    
    perform(args.pipeline_directory, args.action, args.rebuild)


    #currentwd = os.getcwd()
    #print(currentwd)
    #cwlisting = os.listdir(currentwd)
    #print(cwlisting)

if __name__ == "__main__":
    main()
