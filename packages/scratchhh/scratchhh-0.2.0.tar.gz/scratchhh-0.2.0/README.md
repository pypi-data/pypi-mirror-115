# scratchhh
[![img](https://shields.io/badge/view-on%20github-black?logo=github)](https://github.com/themysticsavages/scratchhh)
[![img](https://shields.io/badge/view-on%20pypi-blue?logo=pypi)](https://pypi.org/project/scratchhh)

[![scratch](https://scratch.mit.edu/images/logo_sm.png)](https://scratch.mit.edu)

scratchhh is a kinda thin wrapper for the Scratch API. It makes things easier to fetch and use.

## Installation
With pip:
```
python -m pip install scratchhh
```
Or manually:
```
python setup.py install
```

## Usage
### getUserProj
```py
# Get projects from a specific user
from scratchhh.scratchhh import Scratch
Scratch.getUserProj(user, num)
```
### getThumb
```py
# Get a project thumbnail
from scratchhh.scratchhh import Scratch
Scratch.getThumb(id, file)
```
### searchProj
```py
# Search for projects
from scratchhh.scratchhh import Scratch
Scratch.searchProj(query, num)
```
### getInfo
```py
# Get project information
from scratchhh.scratchhh import Scratch
Scratch.getInfo(id)
```
### getUserAv
```py
# Get a user avatar
from scratchhh.scratchhh import Scratch
Scratch.getUserAv(user, file)
```
### exists
```py
# Check if a user or project exists
from scratchhh.scratchhh import Scratch
Scratch.getUserAv(ini)
```
### getProjComments
```py
# Get project comments
from scratchhh.scratchhh import Scratch
Scratch.getProjComments(id, num)
```

More features will be added as project development moves!

## Examples
```py
from scratchhh.scratchhh import Scratch
import os

ids = Scratch.getUserProj('Scratchteam', 10)
print('Getting some thumbnails :P')
os.chdir('thumbs')

for i in range(0, 10):
  Scratch.getThumb(ids[i], 'thumbnail{}.png'.format(i))
```
```py
from scratchhh.scratchhh import Scratch

project = Scratch.searchProj('minecraft', 1)[0]
loves = Scratch.getInfo(project)['stats']['loves']

print('This project has {} loves. WOW!'.format(loves))
```
```py
from scratchhh.scratchhh import Scratch

users = ['Za-Chary', 'Scratchteam', 'Paddle2See']
print('Getting some user pfps...')

for i in range(0, len(users)):
  Scratch.getUserAv(users[i], '{}.png'.format(users[i]))
```