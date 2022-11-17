#!/bin/bash

PWD=`pwd`
# python3.10 -m pip install virtualenv
python3.10 -m virtualenv -p `which python3.10` venv

active(){
        source $PWD/venv/bin/activate
        # apt-get install python3.10-pip
	python3.10 -m pip install --upgrade pip
	python3.10 -m pip install -r requirements.txt
        python3.10 manage.py makemigrations
        python3.10 manage.py migrate
}
active
