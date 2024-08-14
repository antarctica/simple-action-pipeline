#!/usr/bin/env python

# Version: 2024-87-06: First version
#
# Author: matsco@bas.ac.uk
#
# Main pipeline package that users interact with.

import argparse, os, glob, utils

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
        print("Could not determine status of provided pipeline directory")
        exit(1)
    return retval

def perform_decision(pipeline_type, action, pipeline_fullpath):
    if (pipeline_type == 'unbuilt'):
        if (action == 'build'):
            print('here we build the pipeline')
            conf = utils.configuration()
            yaml_pipeline = conf.yaml_ingest(pipeline_fullpath + 'pipeline.yaml')
            yaml_application = conf.yaml_ingest(pipeline_fullpath + 'application.yaml')
            conf.create_envfile(yaml_pipeline)
            conf.create_envfile(yaml_application)
            bld_pipeline = utils.build([yaml_pipeline, yaml_application])
            #TODO create workflow-manager directory
            #TODO populate workflow-manager directory
        else:
            print('The pipeline does not appear to be built.')
            print('Please run the pipeline build command.')
            exit(1)
    if (pipeline_type == 'built'):
        if (action == 'build'):
            resp = input('The pipeline is already built, would you like to rebuild it? ')
            if resp == 'Y' or resp == 'y':
                perform_decision('unbuilt', 'build', pipeline_fullpath)

def perform(pipeline_directory, action):
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
        print(pipeline_fullpath)
    except:
        print("Problem opening pipeline directory")
        exit(1)

    pipeline_type = initial_check(pipeline_fullpath)
    perform_decision(pipeline_type, action, pipeline_fullpath)
    print(pipeline_type)
 
        
    #currentwd = os.getcwd()
    #print(currentwd)
    #cwlisting = os.listdir(currentwd)
    #print(cwlisting)

if __name__ == "__main__":

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
    args = parser.parse_args()


    # Now kick off main

    # What to do if no pipeline directory was supplied
    if (not args.pipedir) and (not args.pipeline_directory):
        print ("WARN. No pipeline directory provided.\n \
                Attempting to use current directory as pipeline.")

    # Keyword switch takes priority over positional switch
    if (args.pipedir):
        args.pipeline_directory = args.pipedir
    
    perform(args.pipeline_directory, args.action)