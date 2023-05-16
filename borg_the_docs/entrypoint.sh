#!/bin/bash

requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

if [ -f $requirements ]; 
then
    pip install -r $requirements
fi

echo `pwd` >> $GITHUB_OUTPUT
echo `ls` >> $GITHUB_OUTPUT

python entrypoint.py >> $GITHUB_OUTPUT
