# *envfileparser*
___
This package is as simple as possible to get variables from .env files or files with a similar structure.

![](https://img.shields.io/pypi/v/envfileparser?style=for-the-badge)
![](https://img.shields.io/badge/covarage-97%25-green?style=for-the-badge&logo=appveyor)
![](https://img.shields.io/badge/license-GPLv3-blue?style=for-the-badge&logo=appveyor)
![](https://img.shields.io/pypi/pyversions/envfileparser?style=for-the-badge)
### Description
> The package 
> has no dependencies and works with files 
> located in the same directory as the file from 
> which the functions of this package were called. 
> 
> 1. Function ```get_env()``` takes the name of the target variable 
> as a string and an optional second parameter - 
> the path to the file. After that, the function returns the 
> value of the variable also as a string.
> 
> 2. Function ```get_envs()``` accepts a sequence of variable 
> names as a string, and also an optional 
> parameter-the path to the file. 
> This function returns a list of strings 
> that are the values of the desired variables.
> 
> 3. Function `get_env_from_file()` combines the functionality of 
> get_env and get_envs and also  if the parameter 
> with variable names is left empty, the function 
> returns a dictionary with all the variables from the file.
> 
> By default, ```.env``` is specified 
> as the path. Empty lines and lines without 
> the ```'='``` character are skipped. 
> In addition, commenting with a prefix of the ```'#'```
> character is supported.In the event that 
> the specified variable is 
> missing or the desired file cannot be found, 
> the corresponding exceptions are thrown.
## Getting started
___
Install [envfileparser](https://pypi.org/project/envfileparser/) from [PyPi](https://pypi.org/) with pip: `pip install envfileparser`
### Usage example:
The .env file:
```.env
CONST1 = 1
CONST2 = -2

VAR1 = "var1"
VAR2 = 'var2'
VAR3 = var3
```
Python code:
```python
from envfileparser import get_env, get_envs, get_env_from_file

CONST_ONE = get_env('CONST1') # CONST_ONE = '1'
CONST_TWO = get_env('CONST2', file_path='.env') # CONST_TWO = '-2'

all_variables = get_env_from_file()
# all_variables = {'CONST1: '1', 'CONST2': '-2', 'VAR1':= 'var1', 'VAR2': 'var2', 'VAR3': 'var3'}
c1 = all_variables['CONST1'] # c1 = '1'
c2 = all_variables['CONST2'] # c2 = '-2'

variables = get_envs('VAR1', 'VAR2', 'VAR3') # variables = ['var1', 'var2', 'var3']
v1, v2, v3 = variables[0], variables[1], variables[2]
```
#### One more .env file example (support for comments):
```env
# Service token.
API_TOKEN = f3u12yf36f12f418449go3294g238

PORT = 3417
IP = 127.0.0.1 # loopback

USER = 'ADMIN'
PASSWORD="12345678"
```
___
*If your value contains the "#" character, 
then be sure to put it in quotation marks - otherwise 
the parser will take all subsequent characters (including the" # " character) as a comment:*
```python
VAR1 = envfile#parser
VAR2 = "envfile#parser"
```
Python code:
```python
from envfileparser import get_envs

print(*get_envs('VAR1', 'VAR2'), sep='\n')
```
Output:
```
envfile
envfile#parser
```
___
**New version ``0.0.8``:** 
- Added new function `get_env_from_file()`.
  - Combines the functionality of `get_env()` and `get_envs()`.
  - If the parameter with variable names is left empty, the function returns a dictionary with all the variables from the file.
  - `get_env_from_file()` return empty dictionary if file is empty.
- Fixed problems with comments issue #6.
- Removing right and left side spaces in values (all values are string).
___
#### How to contact the maintainer:
![](https://img.shields.io/badge/telegram-Kirill_Lapushinskiy-blue?style=social&logo=telegram&link=https://t.me/kirilllapushinskiy)

![](https://img.shields.io/badge/VK-Kirill_Lapushinskiy-blue?style=social&logo=vk&link=https://vk.com/kirilllapushinskiy)