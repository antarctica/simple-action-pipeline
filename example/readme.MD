## Pipeline Example
Think of this directory `example` as containing the entire workflow of a pipeline. All the configuration/code/structure is inside this directory and pretty much self contained.  

The **simple-action-pipeline** builds the pipeline from the *YAML* config files and code within this directory.  
The **simple-action-pipeline** also executes the pipeline from this directory and creates it's own `workflow_manager` directory, which it uses to monitor the state of the pipeline.  

