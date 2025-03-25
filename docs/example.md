# Example

## Basic tutorial
Lets create a pipeline from scratch using the *simple-action-pipeline* package.

### **Create a project directory for the pipeline**  
  >     mkdir hello-world-project

### **Create and link to python virtual env**  
*assuming you have python >= 3.9 available*
  >     cd hello-world-project
  >     python -m venv ./hello-venv
  >     ln -s ./hello-venv/bin/activate activate
  >     source activate
  >     python -m pip install sap@git+https://github.com/antarctica/simple-action-pipeline

### **Create a pipeline directory**  
  >     mkdir hello-pipeline

### **Create the required pipeline and application yamls**  
  >     cd hello-pipeline
  >     touch pipeline.yaml
  >     touch application.yaml

### **Create the scripts directory and scripts**  
  >     mkdir hello-world-scripts
  >     touch hello-world-scripts/hello.sh
  >     touch hello-world-scripts/world.py

### Your project should now have this structure:
```bash
hello-world-project/
│
├── hello-pipeline/
│   │
│   ├── hello-world-scripts/
│   │   │
│   │   ├── hello.sh
│   │   └── world.py
│   │
│   ├── application.yaml
│   └── pipeline.yaml
│
├── activate
│
└── hello-venv/
    │
    ├── bin/
    └── ...
```

### **Create the pipeline configuration**  
Make the pipeline.yaml file contain the following:  
```bash
---
pipeline:

    name: tutorial
    description: pipeline configuration file for the tutorial pipeline

    env:

        description: environment variables for the pipeline
        create-env-file: true
        env-filename: pipeline.env

        variables:
        - PIPELINE_DIRECTORY: "./"
        - PIPELINE_MAXWORKERS: 1
```

### **Create the application configuration**  
Make the application.yaml file contain the following:  
```bash
---
application:

    name: hello-world
    description: application configuration file for the hello-world tutorial

    env:

        description: environment variables for the application
        create-env-file: true
        env-filename: application.env

        variables:
        - PIPELINE_DIRECTORY: "./"
        - SCRIPTS_DIRECTORY: "./hello-world-scripts"
        - LETTER_DELAY_SECONDS: 2

    sequence:

        description: sequence of actions for the application

        sequence:
        - script: 
            name: hello.sh
            depends: ''
        - script:
            name: world.py
            depends: hello.sh
```

### **Create both application scripts**  
***hello.sh***  
```bash
#!/usr/bin/bash

# hello.sh

set -e

string='hello '
delay=${LETTER_DELAY_SECONDS}

for ((i=0; i<${#string}; i++)); do
    sleep ${delay}
    echo "${string:i:1}"
done

```
***world.py***  
```python
from os import environ
from time import sleep

# world.py

string = 'world'
delay = int(environ['LETTER_DELAY_SECONDS'])

for i in string:
    sleep(delay)
    print(i , end='\n')

```

### **Build the pipeline**  
- Go back to the root project directory.  
  >     cd ..
- Build the pipeline.
  >     pipeline build ./hello-pipeline
This should build without any errors.  

### **Check the pipeline status**  
  >     pipeline status ./hello-pipeline  
... or try the shorter version.  

  >     pipeline status ./hello-pipeline --short

### **Run the pipeline**
  >     pipeline execute ./hello-pipeline  
You can observe the script outputting to the terminal with 2 second gaps between each character. There will also be some output from the pipeline to show when tasks start and finish. At successful pipeline completion, a pipeline report is also output.  

```bash
(hello-venv) bash-4.2$ pipeline execute ./hello-pipeline
INFO:pipeline:Target: ~/hello-world-project/hello-pipeline/
INFO:pipeline:Pipeline Status: built
INFO:pipeline:Executing pipeline tutorial-hello-world.py ; MaxWorkers=1
(hello-venv) bash-4.2$ INFO:2025-03-25 08:44:50.224135 | started pipeline
      Failed     Waiting       Ready    Complete      Active  Task name                                                                    
------------------------------------------------------------------------------------
           0           0           1           0           0  tutorial-hello-world._00_start_pipeline                                                      
           0           1           0           0           0  tutorial-hello-world._01_hello_sh                                                            
           0           1           0           0           0  tutorial-hello-world._02_world_py                                                            
           0           1           0           0           0  tutorial-hello-world._03_finish_pipeline                                                     
....................................................................................
           0           3           1           0           0  Total                                                                 

INFO:2025-03-25 08:44:50.648218:pipeline:Task: _01_hello_sh started.
h
e
l
l
o
 
INFO:2025-03-25 08:45:02.678676:pipeline:Task: _01_hello_sh finished.
INFO:2025-03-25 08:45:02.847103:pipeline:Task: _02_world_py started.
w
o
r
l
d
INFO:2025-03-25 08:45:12.894025:pipeline:Task: _02_world_py finished.
INFO:2025-03-25 08:45:13.593772 | finished pipeline
      Failed     Waiting       Ready    Complete      Active  Task name                                                                          
------------------------------------------------------------------------------------
_00_start_pipeline                                                                  
           0           1           0           0           0  tutorial-hello-world._01_hello_sh                                                            
           0           1           0           0           0  tutorial-hello-world._02_world_py                                                             
           0           1           0           0           0  tutorial-hello-world._03_finish_pipeline                                                     
....................................................................................
           0           3           1           0           0  Total                                                                    

    Executed      Loaded  Task name                                                 
------------------------------------------------------------------------------------
           1           0  tutorial-hello-world._00_start_pipeline                   
           1           0  tutorial-hello-world._01_hello_sh                         
           1           0  tutorial-hello-world._02_world_py                        
           1           0  tutorial-hello-world._03_finish_pipeline  
....................................................................................
           4           0  Total 
```
### **Make a change to the pipeline**
For this example lets make both scripts run much slower by increasing the `LETTER_DELAY_SECONDS` environment variable to 10 seconds.  

- Change the definition in `application.yaml` and save it:
  >     LETTER_DELAY_SECONDS: 10
- Rebuild the pipeline:  
  >     pipeline build ./hello-pipeline --force-build
- Run the pipeline:
  >     pipeline execute ./hello-pipeline  
- Now the pipeline tasks are slow enough that you can use the status command to check the pipeline whilst it runs:  
  >     pipeline status ./hello-pipeline  
- You can also halt the pipeline mid run:
  >     pipeline halt ./hello-pipeline  
- Fully complete scripts will remain complete after a halt and from there you can resume the pipeline with the `execute` command:
  >     pipeline execute ./hello-pipeline
- Or you can choose to run the pipeline from the very beginning by issuing a reset command first:
  >     pipeline halt ./hello-pipeline
  >     pipeline reset ./hello-pipeline
  >     pipeline execute ./hello-pipeline

### **Now try adding an extra script to the pipeline**
The sequence section of `application.yaml` allows you to create simple-linear or complex-parallel pipelines by defining more scripts with intricate dependancies.  

Remember, if you want multiple scripts to run in parallel you will need to increase the number of `PIPELINE_MAXWORKERS` in `pipeline.yaml`.


## Pre-made example