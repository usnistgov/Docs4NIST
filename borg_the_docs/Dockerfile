FROM python:3-slim

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

RUN pip install GitPython

ADD entrypoint.py /entrypoint.py
ADD ntd2d_action /ntd2d_action

ENTRYPOINT ["/entrypoint.py"]