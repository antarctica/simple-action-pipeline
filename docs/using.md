# Using the pipeline

If using a freshly installed pipeline for the first time, then the pipeline must be built from the provided pipeline and application yaml files. This also applies if changes have been made to either yaml file, i.e. the pipeline `build` command must be issued for any yaml configuration changes to take effect.

- *make sure your virtual environment is activated before issuing any of the commands below*  
  *`source <path-to-this-pipeline-directory>\activate`* 

---
## Build the pipeline `build`

To build the pipeline from the provided `pipeline.yaml` and `application.yaml`, run the command:  

```bash
pipeline build <path-to-this-pipeline-directory>
```  
--- 
## Get the pipeline status `status`

As well as checking the status, it can also be used to check that the pipeline is installed and setup correctly. This can be done by running the pipeline's `status` command:

``` bash
pipeline status <path-to-this-pipeline-directory>
# or for the short output
pipeline status <path-to-this-pipeline-directory> --short
```
A long (or short) report should be output. This `status` command can be run at any time and will give the 'live' state of the pipeline and it's tasks.

> - The status of the pipeline is stateful and persistent, even after the execution is completed, which is useful for querying long after the pipeline has completed. This holds true if the pipeline fails for any reason.  

---
## Execute the pipeline `execute`
To start the pipeline, run the command:
```bash
pipeline execute <path-to-this-pipeline-directory>
``` 
---
## Reset the pipeline `reset`
Because the statefulness of the pipeline persists even after completion, an additional step is required before the pipeline can be executed again. This is called a `reset`, and when initiated, the workflow manager erases the state of the pipeline ready for re-execution.  

A reset can be performed by running the command:
```bash
pipeline reset <path-to-this-pipeline-directory>
```

> - Resetting a running pipeline is not advised and may produce unpredictable behaviour (please refer to `halt` below).  

---
## Halt all pipeline tasks `halt`
If the pipeline needs to be halted whilst it is running, the `halt` command has been provided.  
```bash
pipeline halt <path-to-this-pipeline-directory>
```

> - This does not erase the statefulness of the pipeline, so the `status` command can be used after halting has occured. Any pipeline tasks that have already completed will remain so, although any tasks which haven't fully completed will revert to being not started.  

Following a 'halt' there are two possible choices:  

1. `execute` will resume the pipeline from where it was halted.
1. `reset` will reset the pipeline to it's un-executed state.

---
## Tips
- Using any of the pipeline commands **does not** require sourcing of the pipeline's `pipeline.env` and `application.env` files beforehand, this is automatically handled by the pipeline.  
  
- Running the pipeline command from inside a pipeline directory does not require specifying the `<path-to-pipeline-directory>` argument. When this argument is missing, the pipeline assumes the use of the current working directory. For instance, if you are inside the pipeline directory, you can simply issue the command `pipeline status` to get the current status.