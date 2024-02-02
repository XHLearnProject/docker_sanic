#!/bin/bash

cd `dirname $0`

fuser -k -n tcp 16471

python3 main.py

# mongo 10.215.33.133:30000/xh_sanic -ug83db -pg83entitydb
