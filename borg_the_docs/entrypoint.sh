#!/bin/sh

echo "::error::`env`"
echo "::warning::INPUT_ACTION=${INPUT_ACTION}"
echo "::warning::GITHUB_SHA=${GITHUB_SHA}"
echo "::warning::INPUT_DOCS_FOLDER=${INPUT_DOCS_FOLDER}"
echo "::warning::INPUT_DEFAULT_BRANCH=${INPUT_DEFAULT_BRANCH}"
echo "::warning::INPUT_PAGES_BRANCH=${INPUT_PAGES_BRANCH}"
echo "::warning::INPUT_PAGES_URL=${INPUT_PAGES_URL}"

requirements="${INPUT_DOCS_FOLDER}/requirements.txt"

echo "::error::requirements=${requirements}"
if [ -f $requirements ]; 
then
    echo "::notice::installing"
    pip install -r $requirements
    echo "::notice::`python -m pip freeze`"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
