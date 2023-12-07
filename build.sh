#!/bin/bash

pipenv install -r requirements.txt
flask db init
flask db update