
![simple action pipeline logo](assets/img/SAP-small.png)
## simple-action-pipeline (SAP)

A simple pipeline framework for implementing scheduled sequential and parallel actions. Designed around two simple configuration files and implementation of an uncomplicated workflow manager.  

The simple action pipeline has some standard features which wrap around any application specific configuration or code.  

![simple action pipeline features](assets/img/pipeline-features.png)

### Installation
It is recommended that the sap package is installed and used within a Python virtual environment. The Python version must be >= 3.9.x .  

To create a Python virtual environment:  
```
python -m venv path_to_new_virtual_env
```  
  
Then activate the python virtual environment:  
```
source path_to_new_virtual_env/bin/activate
```  

Once activated, install the sap package and it's dependencies into the python virtual environment:  
```
git clone https://github.com/antarctica/simple-action-pipeline ./simple-action-pipeline
cd ./simple-action-pipeline
pip install -e .
```  
### Usage
A simplified implementation of a simple-action-pipeline is given in the `example` folder. Two yaml files in the `example` folder are used to configure the pipeline and the 'application specific' scripts are in the `example/scripts` folder.
```
ls -ahl ./example
```

Check the help of the `pipeline` command-line tool:
```
pipeline --help
```

#### Running for the first time
The example pipeline (and any pipeline for that matter) must be build before it can be used.  
The standard usage for the pipeline command-line tool is:  
`pipeline` `{OPTIONS}` `[ACTION]` `[TARGET_DIRECTORY]`  

```
pipeline build ./example
```
The example pipeline should build without any errors.  

Once built you can check the status of the now built pipeline:
```
pipeline status ./example
```
