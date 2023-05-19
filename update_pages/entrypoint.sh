#!/bin/sh

# These ridiculous machinations are necessary because GitHub Actions docs
# [illustrate](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs)
# using hyphens in input names, and then document that names like
# `octocat-eye-color` are converted to environment variables like
# `INPUT_OCTOCAT-EYE-COLOR`, but these environment variable names
# are [not POSIX compliant](https://stackoverflow.com/a/36992531/2019542)
# and can't be accessed in many shells.
# This has been [reported](actions/toolkit#629) and the following is
# the only offered "solution".
input_docs_var="INPUT_DOCS-FOLDER"
input_docs_folder=(
    printenv
    | grep ${input_docs_var}
    | sed "s/${input_docs_var}=//"
)

requirements="${input_docs_folder}/requirements.txt"

if [ -f $requirements ]; 
then
    pip install -r $requirements
    echo "::group::pip"
    echo "::notice::`python -m pip freeze`"
    echo "::endgroup::"
fi

python /entrypoint.py >> $GITHUB_OUTPUT
