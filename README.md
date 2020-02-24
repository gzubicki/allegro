# GitHub API simple PROXY
Provide basic information about repository

I found a lot of solutions for this exam.
I chose simplest solution without extensions, in my opinion use swagger, flask-restful or other librares is triumph of form over content.

## Nice to have 
`virtualenvwrapper` 

or installed python 3.5

all command you must run in base directory "allegro"

## Install

`pip install -r requrements.txt`

## Run tests
`python tests.py`

## Run
Firstly add your github user and token to default_settings.py

`python runp.py`

## Run in debug mode

`python run.py`
## Usage

`GET /repositories/{owner}/{repository-name}`

## Deploy
It's simple to run on uwsgi and nginx, please use socket connection.


## Siege overload raport
`
Transactions:		          20 hits
Availability:		      100.00 %
Elapsed time:		        0.47 secs
Data transferred:	        0.00 MB
Response time:		        0.34 secs
Transaction rate:	       42.55 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		       14.49
Successful transactions:          20
Failed transactions:	           0
Longest transaction:	        0.46
Shortest transaction:	        0.20
`