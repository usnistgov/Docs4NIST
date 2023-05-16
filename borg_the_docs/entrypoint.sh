#!/bin/bash

requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

if [ -f $requirements ]; 
then
    pip install -r $requirements
fi

python /entrypoint.py >> $GITHUB_OUTPUT
