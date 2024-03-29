![pic](https://i.imgur.com/silQNbk.png)

# Description
A command-line based client for the OpenWeatherMap API.

# Requirements
- Python 3.6+
- Python requests
- Python colorama

# Installation
1. Check whether you have the required Python version installed: ``python --version`` / ``python3 --version``
2. Clone the repository with ``git clone git@github.com:Xcal1bur/OpenWeatherMap-Client.git``
3. Install all required modules with ``pip install -r requirements.txt``

Alternatively you can install the requiered modules with your package manager of choice to avoid conflicts.
# Usage
```
usage: weather.py [-h] [--key KEY] [--doc]

A command-line based client for the OpenWeatherMap API

optional arguments:
  -h, --help            show this help message and exit
  --key KEY, -k KEY     API key for OpenWeatherMap or path to single line text file containing the key.
  --doc                 Show documentation

If no key is parsed the key is read from a file called key.txt. Must only contain one line!
```
***
**In order to get your own API-Key you have to create an [account at OpenWeatherMap.org](https://home.openweathermap.org/users/sign_up) and generate a key.**

# Contribution
Please feel free to report bugs, request features or add examples by submitting a pull request.

# License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

OpenWeatherMap-Client Copyright © 2019 [Xcal1bur](https://github.com/Xcal1bur)
