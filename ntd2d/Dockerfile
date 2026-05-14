FROM ghcr.io/usnistgov/docs4nist:docker

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

RUN git config --global --add safe.directory /github/workspace

ADD entrypoint.py /entrypoint.py
ADD ntd2d.py /ntd2d.py
ADD ntd2d_action /ntd2d_action

ENTRYPOINT ["/entrypoint.py"]
