#!/bin/bash

pipenv install -r requirements.txt
pipenv run flask db init
pipenv run flask db upgrade