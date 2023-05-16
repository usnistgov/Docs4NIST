#!/bin/bash

echo "::warning::INPUT_ACTION=${INPUT_ACTION}"
echo "::error::GITHUB_SHA=${GITHUB_SHA}"
requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

echo "::notice::requirements=${requirements}"
if [ -f $requirements ]; 
then
    echo "::notice::installing"
    pip install -r $requirements
    echo "::notice::`python -m pip freeze`"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
