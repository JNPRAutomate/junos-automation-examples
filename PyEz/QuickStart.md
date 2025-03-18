# Quick start PyEz onBox

In this guide, we provide a simple, step-by-step path, to quickly get you up and running PyEz. We'll show you how to install and configure PyEz. 

## Introduction to PyEz onBox


### What is Python on box?
Its a open-source Juniper Module, where scripts can be created and executed on Junos OS devices.
PyEz uses NETCONF.

### Script Types
1. Commit scripts
	- Junos configuration automation uses commit scripts to automate the commit process. ​
2. Operation (op) scripts
	- Junos operations automation uses op scripts to automate operational tasks and network troubleshooting. Op scripts can be executed manually in the CLI or upon user login.​
3. Event scripts
	- Junos event automation uses event policies and event scripts to instruct Junos OS to perform actions in response to system events. Event scripts are triggered automatically by defined event policies in response to a system event and can instruct Junos OS to take immediate action​
4. SNMP scripts
	- SNMP scripts are triggered automatically when the SNMP manager requests information from the SNMP agent for an object identifier (OID) that is mapped to an SNMP script for an unsupported OID. 

# Install Python and PyEz

## Overview of Python Modules on Junos Devices

Python2 and Python3 is supported on both Juniper OS ( Junos and Evolved ).
To get more informations about which version is supported with which OS release, please have a look here: https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/junos-script-automation-python-scripts-overview.html

Under the following Link, you will get a overview of supported python modules on Junos and Junos Evolved, including which python version we support: https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/junos-python-modules-on-device.html

## Get Ready with Python and PIP

You may wonder "what is PIP". Any time you want to install, delete or update modules, you use PIP ( package manager/installer program ).
Many packages can be found in the Python Package Index (PyPI). ​
This is a repository for Python ( https://pypi.python.org/pypi )
You can use pip to find packages in Python Package Index (PyPI) and to install them.

Depending on your operation system you use, you have different ways of installing Python.

### Understanding PIP
At any time, where you are not sure, what you can do with PIP, type in the following:
`pip --help`

### Python on MacOS

1. First, download an installer package from the Python website. To do that, visit https://www.python.org/downloads/ on your Mac
2. Once the download is complete, double-click the package to start installing Python. The installer will walk you through a wizard to complete the installation, and in most cases, the default settings work well, so install it like the other applications on macOS. You may also have to enter your Mac password to let it know that you agree with installing Python.
3. Let’s verify that the latest version of Python and IDLE installed correctly. To do that, double-click IDLE and type in "python --version"

### Python on Windows

1. First, download the right version of the python installer, visit https://www.python.org/downloads/windows/ on your Windows
2. Execute the python installer on your Windows
3. Make sure to include PIP in your installing process
4. Verify if Python is installed. Open Powershell or any CMD and type in "python --version"

### Python on Linux

1. First, you have to decide which Pyhton version you want to install
2. Then open your CMD
3. Now type:
	`sudo apt-get update`
	`sudo apt-get install python<version>`


## Install PyEz

After you successfully installed your python version. Its now the time to install Juniper PyEz.
For that, open any CMD. First verify, that python is working. After that type in the following:
`pip install junos-eznc`
This command will install the PyEz module.
