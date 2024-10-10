## Pipeline Example
Think of this directory `example` as containing the entire workflow of a pipeline. All the configuration/code/structure is inside this directory and pretty much self contained.  

The **simple-action-pipeline** builds the pipeline from the *YAML* config files and code within this directory.  
The **simple-action-pipeline** also executes the pipeline from this directory and creates it's own `workflow-manager` sub-directory, which it uses to monitor the state of the pipeline. 

This diagram shows the generic layout of one or more pipelines, including a summary of commands used to interact with the pipeline(s).
![layout of pipeline and commands](../assets/img/sap-layout.png)

Follow the readme on the main repository page which will guide you through the principles and operation of the pipeline and this example.
