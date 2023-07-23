FROM python:3-slim

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

# Install git if not installed
# Lifted from https://github.com/David-Lor/Docker-Python-Git-App
# Apache License 2.0
RUN which git \
  || ( \
    ( \
      apt-get -yq update \
      && apt-get -yq install git \
      && rm -rf /var/lib/apt/lists/* \
    ) \
    || ( \
      apk update --no-cache \
      && apk add --no-cache git \
    ) \
  )

RUN pip install GitPython
RUN pip install packaging
RUN pip install github-action-utils
RUN git config --global --add safe.directory /github/workspace

ADD entrypoint.py /entrypoint.py
ADD update_pages_action /update_pages_action

ENTRYPOINT ["/entrypoint.py"]
