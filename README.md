Python Web Scrape API for E-registrar Burapha University
================

A Python Web Scrape API for https://reg.buu.ac.th using Flask, Beautifulsoup 4 and Request Cache 

Requirements
----------

* Python 3

Quick Start
----------

```
pip install -r requirements.txt 
python main.py
```

Route
----------

|        Routes        | HTTP METHOD |    Parameter    |     Description     |
|:--------------------:|:-----------:|:---------------:|:-------------------:|
|     `/api/campus`    |     GET     |                 |  Return all campus  |
|    `/api/building`   |     GET     |                 | Return all building |
|      `/api/room`     |     GET     | campus building |   Return all room   |
| `/api/room/schedule` |     GET     |   campus room   |  Return time table  |