#!/bin/bash

requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

if [ -f $requirements ]; 
then
    pip install -r $requirements
fi

echo "::notice::`pwd`"
echo "::notice::`ls`"

python entrypoint.py >> $GITHUB_OUTPUT
