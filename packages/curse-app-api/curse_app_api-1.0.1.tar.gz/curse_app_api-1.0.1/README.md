Project description might be outdated on [PyPI], latest version available on [Github].


# **Curseforge App API**
The package provides classes to interact with Curseforge app API.

**Note: I wrote neither API nor documentation** (btw documentation with methods and results took from [there]).



# Installation/Upgrade

1) Requires at least python 3.6

2) Install/Upgrade with $ pip install --user --upgrade curse-app-api

# Requirements
```
requests>=2.25.1
selenium>=3.141.0
selenium-requests>=1.3
webdriver-manager>=3.4.2
msedge-selenium-tools>=3.141.3
```


## Usage:
```python
# getting API class
from curse_app_api import CurseAPI, WDCurseAPI

# creating API class
api = CurseAPI()

# example method 
print(api.get_category_timestamp())

# using API with webdriver (this part works slowly because it downloads webdrivers and tries to invoke them)
wdapi = WDCurseAPI()

# it will print the same result as previous print
print(wdapi.get_category_timestamp())

# also if something goes wrong, you can get last query link
print(api.last_query_link)

# and its response
print(api.last_response)
```


# Current supported WebDrivers
For current supported web drivers you don't have to download them and install manually. 
To use Safari web driver, you need to configure it first: run once 
`safaridriver --enable` in terminal.
```textmate
ChromiumDriver
MSEdgeDriver
GeckoDriver (Firefox)
OperaChromiumDriver
Safari web driver
```

# Contributing
If you want to contribute: 

1) If you find bugs related to this project, open an issue in 
Github issues tracker.


2) If you want add a new feature, fork this repo, make changes locally and open a pull request. I'll check changes 
   myself and merge your code into main branch.

**Note:** This API implements curseforge **APP** API != Curseforge. It means that not all projects on Curseforge can be captured by API, only those, 
which seen by Curseforge Desktop. 
So don't report bugs related to this unless project can be seen by Curseforge desktop. If you report this bug, please, provide a screenshot
that your project wasn't captured by API but can be seen in Curseforge Desktop.

# TODO   
Caching webdriver for subsequent usage.

[there]: https://curseforgeapi.docs.apiary.io/
[Github]: https://github.com/CyberSteve777/CurseAppAPI/
[Pypi]: https://pypi.org/project/curse-app-api/
