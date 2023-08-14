FROM continuumio:miniconda3

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

ADD environment.yml /environment.yml

RUN conda env update --name base --file /environment.yml

ADD borg_the_docs.py /borg_the_docs.py
ADD entrypoint.py /entrypoint.py
ADD borg_the_docs_action /borg_the_docs_action

ENTRYPOINT ["/entrypoint.py"]
