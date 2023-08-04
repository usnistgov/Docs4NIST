FROM python:3-slim

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

RUN pip install GitPython
RUN pip install packaging
RUN pip install github-action-utils

ADD borg_the_docs.py /borg_the_docs.py
ADD entrypoint.py /entrypoint.py
ADD borg_the_docs_action /borg_the_docs_action

ENTRYPOINT ["/entrypoint.py"]
