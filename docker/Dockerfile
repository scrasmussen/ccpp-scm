FROM debian:12-slim
LABEL maintainer="Michael Kavulich <kavulich@ucar.edu>"

# arguments that can be passed in
ARG PR_NUMBER
# build variables
ARG GNU_VERSION=12
ARG VERBOSE=0


# Set up base OS environment
RUN apt-get -y update

# Get "essential" tools and libraries
RUN apt-get update -qq && apt-get install -qq -y --no-install-recommends \
    build-essential \
    cmake \
    cmake-curses-gui \
    curl \
    git \
    file \
    gfortran-$GNU_VERSION \
    ksh \
    m4 \
    tcsh \
    time \
    wget \
    vim \
    emacs-nox \
    python3 \
    python3-pip \
    python3.11-venv \
    python3-netcdf4 \
    libnetcdf-pnetcdf-19 \
    libnetcdff7 \
    libnetcdf-dev \
    libnetcdff-dev \
    libxml2 \
    openmpi-bin \
    libopenmpi-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/gfortran-$GNU_VERSION /usr/bin/gfortran

# Set up python needed packages, preferred Docker method is apt-get but
# f90nml can't be installed for debian that way
RUN pip install f90nml --break-system-packages

#Compiler environment variables
ENV CC=gcc
ENV FC=gfortran
ENV CXX=g++
ENV F77=gfortran
ENV F90=gfortran

# Other necessary environment variables
ENV LD_LIBRARY_PATH=/usr/lib/

# Set up unpriviledged user account, set up user home space and make sure user has permissions on all stuff in /comsoftware
RUN groupadd comusers -g 9999 \
 && useradd -u 9999 -g comusers -M -s /bin/bash -c "Unpriviledged user account" -d /home comuser \
 && mkdir /comsoftware \
 && chown -R comuser:comusers /home \
 && chmod 6755 /home \
 && chown -R comuser:comusers /comsoftware \
 && chmod -R 6755 /comsoftware

# all root steps completed above, now continue below as regular userID comuser
USER comuser
WORKDIR /home

# Build NCEP libraries we need for SCM

ENV NCEPLIBS_DIR=/comsoftware/nceplibs

RUN mkdir -p $NCEPLIBS_DIR/src && cd $NCEPLIBS_DIR/src \
   && git clone -b v2.4.1 --depth 1 --recursive https://github.com/NOAA-EMC/NCEPLIBS-bacio \
   && mkdir NCEPLIBS-bacio/build && cd NCEPLIBS-bacio/build \
   && cmake -DCMAKE_INSTALL_PREFIX=$NCEPLIBS_DIR .. \
   && make VERBOSE=$VERBOSE -j \
   && make install

RUN cd $NCEPLIBS_DIR/src \
  && git clone -b v2.3.3 --depth 1 --recursive https://github.com/NOAA-EMC/NCEPLIBS-sp \
  && mkdir NCEPLIBS-sp/build && cd NCEPLIBS-sp/build \
  && cmake -DCMAKE_INSTALL_PREFIX=$NCEPLIBS_DIR .. \
  && make VERBOSE=$VERBOSE -j \
  && make install

RUN cd $NCEPLIBS_DIR/src \
  && git clone -b v2.11.0 --depth 1 --recursive https://github.com/NOAA-EMC/NCEPLIBS-w3emc \
  && mkdir NCEPLIBS-w3emc/build && cd NCEPLIBS-w3emc/build \
  && cmake -DCMAKE_INSTALL_PREFIX=$NCEPLIBS_DIR .. \
  && make VERBOSE=$VERBOSE -j \
  && make install

ENV bacio_ROOT=/comsoftware/nceplibs
ENV sp_ROOT=/comsoftware/nceplibs
ENV w3emc_ROOT=/comsoftware/nceplibs

# Obtain CCPP SCM source code, build code, and download static data
RUN if [ -z "$PR_NUMBER" ]; then \
        cd /comsoftware \
        && git clone --recursive -b release/public-v7 https://github.com/NCAR/ccpp-scm; \
    else \
        cd /comsoftware \
        && git clone https://github.com/NCAR/ccpp-scm \
        && cd ccpp-scm \
        && git fetch origin pull/${PR_NUMBER}/head:test_pr \
        && git checkout test_pr \
        && git submodule update --init --recursive --depth 1; \
    fi

RUN mkdir /comsoftware/ccpp-scm/scm/bin \
  && cd /comsoftware/ccpp-scm/scm/bin \
  && cmake ../src \
  && make -j


# The analysis scripts have options for using LaTeX when making figure labels.
# If you would like to install LaTeK, uncomment the section below.
# Note: This will increase the image size by 1 GB.
#USER root
#RUN yum -y update \
#  && yum -y install texlive-*
#USER comuser

# Set working directory
WORKDIR /comsoftware/ccpp-scm/
ENV SCM_WORK=/comsoftware
ENV SCM_ROOT=/comsoftware/ccpp-scm/

# For interactive use, vim mouse settings are infuriating
RUN echo "set mouse=" > ~/.vimrc

# only download test data when PR is being tested
ENTRYPOINT ["sh", "-c", "\
if [ -n \"$PR_NUMBER\" ]; then \
  ./contrib/get_aerosol_climo.sh && \
  ./contrib/get_all_static_data.sh && \
  ./contrib/get_thompson_tables.sh; \
fi && \
cd /comsoftware/ccpp-scm/scm/bin && \
exec sh"]
