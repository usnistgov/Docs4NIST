FROM python:3-slim

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

RUN pip install GitPython
RUN pip install packaging
RUN pip install github-action-utils
RUN git config --global --add safe.directory /github/workspace

ADD borg_the_docs.py /borg_the_docs.py
ADD entrypoint.py /entrypoint.py
ADD ntd2d_action /ntd2d_action

ENTRYPOINT ["/entrypoint.py"]
