#!/bin/bash

echo "::warning::INPUT_ACTION=${INPUT_ACTION}"
echo "::warning::GITHUB_SHA=${GITHUB_SHA}"
echo "::warning::GITHUB_SHA=INPUT_DOCS-FOLDER=${INPUT_DOCS-FOLDER}"

requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

echo "::error::requirements=${requirements}"
if [ -f $requirements ]; 
then
    echo "::notice::installing"
    pip install -r $requirements
    echo "::notice::`python -m pip freeze`"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
