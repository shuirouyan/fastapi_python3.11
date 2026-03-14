#!/bin/sh
echo "pengpai news shell"
cd /root/code/frida_repository
echo $PWD
echo $(/root/code/venv_fastapi/bin/python py/pengpai.py)
