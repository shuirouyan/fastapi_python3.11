#!/bin/bash
echo $PWD
/root/code/venv_fastapi/bin/python /root/code/fastapi_python3.11/project01/main.py > /dev/null 2>&1 &
echo $(ps -ef | grep python | grep -v grep)
