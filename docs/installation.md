# Installation

It is recommended to use a Python virtual environment to reduce the risk of any Python package conflicts.

### HPC Workstation or Local PC

1. **Create a Python virtual environment**  
   The Python version must be **Python 3.9** or higher.
    
    - Check the available Python with `python --version`
    - If required, install or load a compatible python version. Your system administrator will be able to help with getting a compatible Python version.
    - then `python -m venv <path-to-venv>` with a path of your choosing.

1. **Source the new newly created python venv**  
    - `source <path-to-venv>/bin/activate` (Assuming you're using Bash or similar. Use the appropriate activate script within that folder depending on your shell)

1. **Install the simple-action-pipeline (sap) package**
    - If you simply want to use the simple-action-pipeline 'as-is'.  
      `python -m pip install sap@git+https://github.com/antarctica/simple-action-pipeline`  
    - If you want to install an editable version of simple-action-pipeline.   
      `git clone https://github.com/antarctica/simple-action-pipeline ./simple-action-pipeline`  
      `cd ./simple-action-pipeline`  
      `pip install -e .`  
      Use `pip install -e ".[documentation]"` to edit/contribute to the documentation.  
