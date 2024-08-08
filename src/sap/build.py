#!/usr/bin/env python

# Version: 2024-07-02: First version
#
# Author: matsco@bas.ac.uk
#
# Script to build the pipeline from it's configuration folder

import argparse

def move(configuration_directory):
    pass


if __name__ == "__main__":

    """
    build simple action pipeline entry point
    build the simple-action-pipeline by supplying a configuration directory
    """

    parser = argparse.ArgumentParser(description='Build the simple-action-pipeline by supplying a configuration directory')
    parser.add_argument("-c", "--config_directory", help="configuration directory", action="store", dest='confdir')
    args = parser.parse_args()


    # Now kick off main
    if (not args.confdir):
        print ("ERROR. The configuration directory must be provided '-c/--config_directory'")
        exit(0)
    else:
        move(args.confdir)