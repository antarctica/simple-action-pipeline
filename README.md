
![simple action pipeline logo](assets/img/SAP-small.png)
## simple-action-pipeline (SAP)

A simple pipeline framework for implementing scheduled sequential and parallel actions. Designed around two simple configuration files and implementation of an uncomplicated workflow manager.  

The simple action pipeline has some standard features which wrap around any application specific configuration or code.  

![simple action pipeline features](assets/img/pipeline-features.png)

### Installation
It is recommended that the sap package is installed and used within a python virtual environment. To create a python virtual environment:  
```
python3 -m venv path_to_new_virtual_env
```  
  
Then activate the python virtual environment:  
```
source path_to_new_virtual_env/bin/activate
```  

Once activated, install the sap package into the python virtual environment:  
```
git clone https://github.com/antarctica/simple-action-pipeline ./sap
pip install -e ./sap
```  
