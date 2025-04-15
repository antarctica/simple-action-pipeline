# Usage

The primary method for interacting with the *simple-action-pipeline* package is via it's command-line-interface (CLI), with the command `pipeline`.

- *make sure your python virtual environment is activated before issuing any of the commands below*  
  *`source <path-to-virtual-environment>\bin\activate`* 

---
## Getting help `-h, --help`

```bash
pipeline -h
# or
pipeline --help
```
```bash
>  usage: pipeline [-h] [-d PIPEDIR] [-b] [-r] [-s] {build,status,execute,reset,halt,await} [pipeline_directory ...]
>  
>  perform action with simple-action-pipeline by supplying a pipeline directory
>  
>  positional arguments:
>    {build,status,execute,reset,halt,await}
>                                     Action for the pipeline to perform. options are 'build', 'status', 'execute', 'reset', 'halt', 'await'.
>    pipeline_directory               Pipeline directory to use
>  
>  options:
>    -h, --help                       show this help message and exit
>    -d PIPEDIR, --directory PIPEDIR  Pipeline directory
>    -b, --force-build                Force building the pipeline that is already built.
>    -r, --force-reset                Force reset if the pipeline is still active
>    -s, --short                      Output shortened information where supported 
```
> **The standard usage for the pipeline command-line tool is:**  
> **`pipeline` `[options]` `{action}` `[target_directory]`**  
---
## Build the pipeline `build`
To build the pipeline from the `pipeline.yaml` and `application.yaml` files. This command is also required if you have made configuration changes to an already built pipeline.  
```bash
pipeline build <path-to-pipeline-directory>
```
If you attempt to rebuild an already built pipeline you will be given a confirmation prompt. To suppress this the `-b, --force-build` option is provided.  
```bash
pipeline build <path-to-pipeline-directory> --force-build
```
--- 
## Get the pipeline status `status`

As well as checking the status, it can also be used to check that the pipeline is installed and setup correctly.

``` bash
pipeline status <path-to-pipeline-directory>
# or for the shorter output
pipeline status <path-to-pipeline-directory> --short
```
A long (or short) report should be output. This `status` command can be run at any time and will give the 'live' state of the pipeline and it's tasks.

> - The status of the pipeline is stateful and persistent, even after any execution is completed, which is useful for querying long after the pipeline has completed. This holds true if the pipeline fails for any reason.  

---
## Execute the pipeline `execute`
To start the pipeline.
```bash
pipeline execute <path-to-pipeline-directory>
```  
Because the pipeline state persists after completion (or failure) it must be `reset` before it can be executed again. Trying to execute a completed pipeline will result in no execution as all the work has already been done.  

```bash
pipeline execute ./example  
  
INFO:pipeline:All Tasks complete, nothing to do  
INFO:pipeline:Use the [reset] action before re-executing a completed pipeline  
```
---
## Reset the pipeline `reset`
Because the statefulness of the pipeline persists even after completion, an additional step is required before the pipeline can be executed again. This is called a `reset`, and when initiated, the workflow manager erases the state of the pipeline ready for re-execution.  

```bash
pipeline reset <path-to-pipeline-directory>
```

> - Resetting a running pipeline is not advised and may produce unpredictable behaviour (please refer to `halt` below).  

---
## Halt all pipeline tasks `halt`
If the pipeline needs to be halted whilst it is running, the `halt` command has been provided.  
```bash
pipeline halt <path-to-pipeline-directory>
```

> - This does not erase the statefulness of the pipeline, so the `status` command can be used after halting has occured. Any pipeline tasks that have already completed will remain so, although any tasks which haven't fully completed will revert to being not started.  

Following a 'halt' there are two possible choices:  

1. `execute` will resume the pipeline from where it was halted.
1. `reset` will reset the pipeline to it's un-executed state.

---
## Running the pipeline with SLURM `await`  
The action `await` is a blocking process which only returns if the pipeline completes or encounters a task failure.

```
pipeline await ./example
```
This is useful because some schedulers such as SLURM may be unaware that the pipeline is running parallel tasks in the background. By placing a pipeline `await` action at the end of a job script the job is held active until it is fully complete or fails. Please refer to the provided example script [slurm_job_example.sh](https://raw.githubusercontent.com/antarctica/simple-action-pipeline/main/example/slurm_job_example.sh).

---
## Tips
- Using any of the pipeline commands **does not** require sourcing of the pipeline's `pipeline.env` and `application.env` files beforehand, this is automatically handled by the pipeline.  
  
- Running the pipeline command from inside a pipeline directory does not require specifying the `<path-to-pipeline-directory>` argument. When this argument is missing, the pipeline assumes the use of the current working directory. For instance, if you are inside the pipeline directory, you can simply issue the command `pipeline status` to get the current status.