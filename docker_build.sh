#!/bin/bash

# find . -type f -name "*.pyc" -type f -delete
# find . -type d -name "__pycache__" -exec rm -rf {} +

docker build -t xh-sanic-image .

docker tag xh-sanic-image lamborghini1993/xh-sanic:1.0.1

docker push lamborghini1993/xh-sanic:1.0.1
