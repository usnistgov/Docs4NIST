FROM continuumio/miniconda3

LABEL maintainer="Jonathan Guyer <guyer@nist.gov>"

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
 && apt-get install --no-install-recommends --yes \
      graphviz \
      imagemagick \
      make \
      \
      latexmk \
      lmodern \
      fonts-freefont-otf \
      texlive-latex-recommended \
      texlive-latex-extra \
      texlive-fonts-recommended \
      texlive-fonts-extra \
      texlive-lang-cjk \
      texlive-lang-chinese \
      texlive-lang-japanese \
      texlive-luatex \
      texlive-xetex \
      xindy \
      tex-gyre \
      \
      ghostscript \
      gsfonts \
      texlive-science \
      texlive-extra-utils \
      librsvg2-bin \
      \
      git
 && apt-get autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ADD environment.yml /environment.yml

RUN conda config --set solver libmamba
RUN conda update -n base -c defaults conda
RUN conda env update --name base --file /environment.yml
