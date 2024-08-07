#!/usr/bin/env python

# Version: 2024-87-06: First version
#
# Author: matsco@bas.ac.uk
#
# Main pipeline package that users interact with.

import argparse, os

def perform(pipeline_directory):
    if type(pipeline_directory) != type(list):
        pipeline_directory = [pipeline_directory]
    
    try:
        print(''.join(pipeline_directory[0]))
    except:
        print("Problem opening pipeline directory")
        exit(1)

    #TODO
    # The very first thing to do is to deduce if the provided directory
    # is built or not (an unbuilt pipeline directory is no use to anyone).
    
    # First handle relative and absolute paths sensibly
    try:
        if ''.join(pipeline_directory[0])[0] == '.':
            print(os.getcwd()+''.join(pipeline_directory[0]).replace('./','/'))
        elif ''.join(pipeline_directory[0])[0] == '/':
            print(''.join(pipeline_directory[0]))
        elif ''.join(pipeline_directory[0]) == '.':
            print(os.getcwd()+'/')
        else:
            print(os.getcwd()+'/'+''.join(pipeline_directory[0]).replace('.',''))

        
        currentwd = os.getcwd()
        print(currentwd)
        cwlisting = os.listdir(currentwd)
        print(cwlisting)
    except:
        print("Problem opening pipeline directory")
        exit(1)

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
    
    perform(args.pipeline_directory)