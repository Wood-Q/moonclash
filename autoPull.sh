#!/bin/bash
cd /home/doeca/documents/projects/clashBack/
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
cd ./store/
git pull
cd ../
python3 collectmap.py
python3 handle.py