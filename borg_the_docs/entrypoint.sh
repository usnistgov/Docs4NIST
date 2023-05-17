#!/bin/sh

echo "::error::`env`"
echo "::warning::INPUT_ACTION=${INPUT_ACTION}"
echo "::warning::GITHUB_SHA=${GITHUB_SHA}"
echo "::warning::INPUT_DOCS-FOLDER=${INPUT_DOCS-FOLDER}"
echo "::warning::INPUT_DEFAULT-BRANCH=${INPUT_DEFAULT-BRANCH}"
echo "::warning::INPUT_PAGES-BRANCH=${INPUT_PAGES-BRANCH}"
echo "::warning::INPUT_PAGES-URL=${INPUT_PAGES-URL}"

requirements="${INPUT_DOCS-FOLDER}/requirements.txt"

echo "::error::requirements=${requirements}"
if [ -f $requirements ]; 
then
    echo "::notice::installing"
    pip install -r $requirements
    echo "::notice::`python -m pip freeze`"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
