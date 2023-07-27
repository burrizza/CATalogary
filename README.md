# CATalog(ary)

The Python Library CATalog(ary) is based on [atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api) and will hopefully consist out of many modular APIs in the future. 
Through the CATalog universe, it should be possible to attach any kind of information to my projects in a uniform and fast way. CATalog(ary) could also be used as kind of boilerplate for API-libraries in foreign projects. 

**The repo is far away from ready state yet and main parts of the codes could be rewritten soon.**
**Please take further note: The CATalog (TM) libraries are hardly shaped to fit our personal needs and not meant to get out of alpha stage in any time. Please act respectful and always try to reduce your load on open APIs to a minimum. Thank you!**


Thanks to all developers and please let me know if I made something wrong, or you are unhappy with this development!

## Features (in development)

* api.NinaAPI: Get data from the Federal Office for Civil Protection (Bundesamt fuer Bevoelkerungsschutz):
	- KATwarn (Katastrophenschutz - civil protection warn system Germany) 
    - MoWaS (Modular Warn System)
    - BIWapp (Buerger Info und Warnapp - german citizen warn application)
    - Police through NINA-API
    - LHP (Hochwasser Portal - german flood warning system)
    - DWD (Deutscher WetterDienst - german weather service)

* api.UmweltbundesamtAPI: Get data from the Federal Environment Agency of Germany (Umweltbundesamt):
	- air data measures
	- metadata about the measures
	- air data measures stations
**more coming**


## Platforms

Implemented in Python.

## Usage

1. Installation and Usage
	1. pip install https://github.com/burrizza/CATalogary/releases/download/v1.0a0/catalogary-1.0a0-py3-none-any.whl [--force-reinstall --upgrade --no-cache-dir]
	2. import for example the NinaAPI with "from catalogary.api import NinaAPI"
    3. see tests folder for commands
2. Reusage (shortened)
	1. git clone git@github.com:burrizza/CATalogary.git
	2. implement new API
	3. test new API
	4. edit setup.py
	5. pip install wheel
	6. python .\setup.py bdist_wheel
	7. use new whl file