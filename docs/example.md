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
    sleep delay
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

## Pre-made example