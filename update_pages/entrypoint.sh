#!/bin/sh

requirements="${INPUT_DOCS_FOLDER}/requirements.txt"

if [ -f $requirements ]; 
then
    pip install -r $requirements
    echo "::group::pip"
    echo "::notice::`python -m pip freeze`"
    echo "::endgroup::"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
