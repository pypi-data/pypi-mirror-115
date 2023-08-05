[![PyPI
version](https://badge.fury.io/py/ddg3.svg)](https://badge.fury.io/py/ddg3)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python 3.6+
supported](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

# ddg3

A Python library for querying the Duck Duck Go API.

Copyright Michael Stephens <me@mikej.st>, released under a BSD-style
license.

Updated for Python3 by Jacobi Petrucciani <jacobi@mimirhq.com>

Source: <https://github.com/jpetrucciani/python-duckduckgo>

## Installation

To install run

> `pip install ddg3`

or

> `python setup.py install`

## Usage

```python
import ddg3 
r = ddg3.query('Duck Duck Go') 
r.type                         # 'answer' 
r.results[0].text              # 'Official site' 

r.results[0].url               # '<http://duckduckgo.com/>' 
r.abstract.url                 # '<http://en.wikipedia.org/wiki/Duck_Duck_Go>' 
r.abstract.source              # 'Wikipedia'


r = ddg3.query('Python') 
r.type                         # 'disambiguation' 

r.related[6].text              # 'Python (programming language), a computer programming language' 
r.related[6].url               # '<http://duckduckgo.com/Python_(programming_language)>'

r = ddg3.query('1 + 1') 
r.type                         # 'nothing' 

r.answer.text                  # '1 + 1 = 2' 
r.answer.type                  # 'calc'
```
