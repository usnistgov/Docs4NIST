FROM continuumio/miniconda3

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

ADD environment.yml /environment.yml

RUN conda config --set solver libmamba
RUN conda update -n base -c defaults conda
RUN conda env update --name base --file /environment.yml

RUN git config --global --add safe.directory /github/workspace

ADD entrypoint.py /entrypoint.py
ADD ntd2d.py /ntd2d.py
ADD ntd2d_action /ntd2d_action

ENTRYPOINT ["/entrypoint.py"]
