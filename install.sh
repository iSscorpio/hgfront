#!/bin/bash

#./manage.py syncdb
curl -i http://127.0.0.1:8001/r/q/createqueue/ -d name=repoclone
curl -i http://127.0.0.1:8001/r/q/createqueue/ -d name=repocreate