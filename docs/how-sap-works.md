# How simple-action-pipeline works

*simple-action-pipeline (sap)* provides a generic command line tool for creating configuration based reproducible pipelines.  

Behind the scenes *sap* uses some features of the workflow manager [Jug](https://github.com/luispedro/jug) to both create and then manage the pipeline.  

Firstly, *sap* treats a single directory as a pipeline, containing all of the required configuration and code for the pipeline. This is referred to as the `<pipeline-directory>` or `<target-directory>`.  

Secondly, *sap* builds the pipeline from `pipeline.yaml`, `application.yaml` and a `scripts` subdirectory. Building the pipeline is done by invoking the **'build'** action. Once built there are a number of other actions as detailed in the [Usage](using.md) section.

## Minimum configuration
As a bare minimum the `pipeline.yaml` and `application.yaml` must contain the following as demonstrated below:

**pipeline.yaml**

    pipeline:

        name: pipeline_name
        description: pipeline configuration file

        env:

            description: environment variables for the pipeline
            create-env-file: true
            env-filename: pipeline.env

            variables:
            - PIPELINE_DIRECTORY: "./"
            - PIPELINE_MAXWORKERS: 1

**application.yaml**

    application:

        name: application_name
        description: application configuration file

        env:

            description: environment variables for the application
            create-env-file: true
            env-filename: application.env

            variables:
            - PIPELINE_DIRECTORY: "./"
            - SCRIPTS_DIRECTORY: "./scripts"

        sequence:

            description: sequence of actions for the application

            sequence:
            - script: 
                name: first_script.sh
                depends: ''

As you can see, this pipeline runs just a single script which depends on no other scripts. The maximum number of workers is set to 1 (this is how many parallel scripts can run at any one time).  

The `PIPELINE_DIRECTORY` must be defined in both yaml files as these are checked during the build process. `PIPELINE_MAXWORKERS` and `SCRIPTS_DIRECTORY` must also be defined. Also, any scripts defined under the 'sequence' section must exist in the scripts directory for the build to succeed.

## The workflow manager
The pipeline 'build' command creates or re-creates from the `application.yaml`, `pipeline.yaml` and `scripts` directory, a python script that is used by the [Jug](https://github.com/luispedro/jug) parallelisation package. Inspection of this auto-generated python script shows how all the dependancies are set up.  

*sap* invokes Jug with this python script for each `WORKER` up to `PIPELINE_MAXWORKERS`, creating one or more parallel processes that can complete multiple tasks whilst being monitored. This collection of python script, Jug and `WORKERS` is referred to as the 'workflow-manager'.  

Everything related to the workflow manager's operation is contained within the `<pipeline-directory>/workflow-manager/` directory, which is created by the 'build' command.

## Optimising `PIPELINE_MAXWORKERS`
This `pipeline.yaml` file contains the `PIPELINE_MAXWORKERS` definition. The workflow manager will attempt to allocate **up to** this many workers to the pipeline.  

It can be important to think carefully about setting the maximum number of workers as described in the example below.

> Example:  
> **| You have 10 tasks the *could* all execute in parallel.**  
> **| You are using a platform that has 6 CPU threads.**  
>   * If you set `MAXWORKERS` to `2` the workflow manager will invoke 2 workers, meaning that the 2 CPU threads can complete all 10 tasks twice as quickly as if there was only 1 worker (i.e. 1 task done at a time).  
>   * If you set `MAXWORKERS` to `10` the workflow manager will invoke 10 workers but because this is more than available CPU threads there will be a significant amount of CPU context switching to achieve the effect of 10 CPU threads running. This results in slower performance.  
>   * If you set `MAXWORKERS` to `5` the workflow manager will invoke 5 workers, meaning that the 5 CPU threads can complete all 10 tasks five times as quickly as if there was only 1 worker (i.e. 1 task done at a time). This would also avoid CPU context switch and also leave 1 CPU thread free for the underlying platform.  

## Environment variables
If your pipeline relies upon constants held within environment variables, these can be pre-defined under the `env:variables:` section of either yaml config file. *sap* will make sure these environment variables are available whenever the pipeline runs.  

## Task sequence
The sequence order and dependancies of the tasks (scripts) are defined under the `sequence:` section of the `application.yaml` config file.  

Each task (script) in the sequence has a `name:` and `depends:` field. The name is the name of the script to be found in the scripts directory. The depends can be either a single script name or a list of script names if there are multiple dependancies. If a script has no dependancy then the `depends:` field should contain an empty string `''`.  

***Currently shell scripts `.sh` and python scripts `.py` are the only supported task (script) names.*** 
 

## Further detail
For more detail on the inner workings of **Jug** or **sap**, please refer to the documentation for:  
 - [Jug](https://jug.readthedocs.io/en/latest/)  
 - [simple-action-pipeline repo](https://github.com/antarctica/simple-action-pipeline)    