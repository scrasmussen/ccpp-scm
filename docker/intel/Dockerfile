FROM intel/oneapi-hpckit
# FROM intel/fortran-essentials
ARG PR_NUMBER

#Compiler environment variables
ENV CC=mpiicx
ENV FC=mpiifx
ENV CXX=mpiicx
ENV F77=mpiifx
ENV F90=mpiifx
ENV LD_LIBRARY_PATH=/usr/local/lib/:/usr/lib/gcc/x86_64-linux-gnu/13:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# Set up base OS environment
RUN apt-get -y update

# Get "essential" tools and libraries
RUN apt-get update -qq && apt-get install -qq -y --no-install-recommends \
    build-essential \
    cmake \
    cmake-curses-gui \
    curl \
    emacs-nox \
    file \
    git \
    ksh \
    less \
    libcurl4-openssl-dev \
    libssl-dev \
    m4 \
    pipx \
    python3 \
    python3-pip \
    python3-venv \
    python3-netcdf4 \
    tcsh \
    time \
    vim \
    wget \
    zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# Set up python needed packages, preferred Docker method is apt-get but
# f90nml can't be installed for debian that way
RUN pipx install f90nml \
    && pipx ensurepath

WORKDIR /home/src
# Install HDF5
ENV hdf5_version=1.14.6
RUN wget -q https://github.com/HDFGroup/hdf5/archive/refs/tags/hdf5-${hdf5_version}.tar.gz \
    && tar zxf hdf5-${hdf5_version}.tar.gz \
    && cd hdf5-hdf5-${hdf5_version} \
    && ./configure --prefix=/usr/local/ \
    && make -j \
    && make install \
    && cd .. \
    && rm -rf hdf5-hdf5-${hdf5_version} hdf5-${hdf5_version}.tar.gz
    # && LD_LIBRARY_PATH=$HDF5_ROOT/lib:$LD_LIBRARY_PATH \
    # && PATH=$HDF5_ROOT/bin:$PATH

# ENV ompi_major_version=4.1 \
#     ompi_version=4.1.8
# RUN wget -q https://download.open-mpi.org/release/open-mpi/v${ompi_major_version}/openmpi-${ompi_version}.tar.gz \
#     && tar zxf openmpi-${ompi_version}.tar.gz \
#     && cd openmpi-${ompi_version}
#     && CFLAGS=-fPIC CXXFLAGS=-fPIC FCFLAGS=-fPIC ./configure \
#     && make -j \
#     && make install \
#     && cd .. \
#     && rm -rf openmpi-${ompi_version} openmpi-${ompi_version}.tar.gz

ENV netcdf_version=4.9.3 \
    netcdff_version=4.6.2
RUN echo "here"
RUN wget -q https://github.com/Unidata/netcdf-c/archive/refs/tags/v${netcdf_version}.tar.gz \
    && tar -xzf v${netcdf_version}.tar.gz \
    && cd netcdf-c-${netcdf_version} \
    && CXXFLAGS="-I/usr/include/c++/13 -I/usr/include/x86_64-linux-gnu/c++/13" \
       CFLAGS="-L/usr/lib/gcc/x86_64-linux-gnu/13 -L/usr/lib/x86_64-linux-gnu" \
       ./configure --disable-libxml2 \
    && make -j \
    && make install \
    && cd .. && rm -rf netcdf-c-${netcdf_version} v${netcdf_version}.tar.gz
RUN wget -q https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v${netcdff_version}.tar.gz \
    && tar -xzf v${netcdff_version}.tar.gz
RUN which $FC
RUN cd netcdf-fortran-${netcdff_version} \
    && export FFLAGS="-fPIC" FCFLAGS="-fPIC" \
    && ./configure
RUN cd netcdf-fortran-${netcdff_version} \
    make -j \
    && make install \
    && cd .. && rm -rf netcdf-fortran-${netcdff_version} v${netcdff_version}.tar.gz

# # install NCELLIBS
ENV bacio_version=2.6.0
RUN git clone --branch v${bacio_version} https://github.com/NOAA-EMC/NCEPLIBS-bacio.git bacio \
    && cd bacio && mkdir build && cd build \
    && cmake .. \
    && make -j \
    && make install \
    && cd ../../ \
    && rm -rf bacio
    # && echo "bacio_DIR=/home/runner/bacio/lib/cmake/bacio" >> $GITHUB_ENV \

# todo: update to ip
ENV sp_version=2.5.0
RUN git clone --branch v${sp_version} https://github.com/NOAA-EMC/NCEPLIBS-sp.git \
    && cd NCEPLIBS-sp && mkdir build && cd build \
    && cmake .. \
    && make -j \
    && make install \
    && cd ../../ \
    && rm -rf NCEPLIBS-sp
    # && echo "sp_DIR=/home/runner/NCEPLIBS-sp/lib/cmake/sp" >> $GITHUB_ENV \

ENV w3_version=2.12.0
RUN git clone --branch v${w3_version} https://github.com/NOAA-EMC/NCEPLIBS-w3emc.git \
      && cd NCEPLIBS-w3emc && mkdir build && cd build \
      && cmake ../ \
      && make -j \
      && make install \
      && cd ../../ \
      && rm -rf NCEPLIBS-w3emc
        # echo "w3emc_DIR=/home/runner/myw3emc/lib/cmake/w3emc" >> $GITHUB_ENV


# Set up unprivileged user using /home/src as home directory
RUN groupadd -g 9999 comusers && \
    useradd -u 9999 -g comusers -M -s /bin/bash -c "Unprivileged user account" -d /home/src comuser && \
    install -d -m 2755 -o comuser -g comusers /home/src

# Switch to the unprivileged user
USER comuser

# Obtain CCPP SCM source code, build code, and download static data
RUN if [ -z "$PR_NUMBER" ]; then \
        git clone --recursive -b enhancement/bacio-library-bump https://github.com/scrasmussen/ccpp-scm; \
    else \
        git clone https://github.com/NCAR/ccpp-scm \
        && cd ccpp-scm \
        && git fetch origin pull/${PR_NUMBER}/head:test_pr \
        && git checkout test_pr \
        && git submodule update --init --recursive --depth 1; \
    fi

RUN mkdir /home/src/ccpp-scm/scm/bin \
  && cd /home/src/ccpp-scm/scm/bin \
  && cmake ../src \
  && make -j


# # The analysis scripts have options for using LaTeX when making figure labels.
# # If you would like to install LaTeK, uncomment the section below.
# # Note: This will increase the image size by 1 GB.
# # USER root
# # RUN apt-get update && \
# #     apt-get install -y --no-install-recommends \
# #     texlive-full && \
# #     rm -rf /var/lib/apt/lists/*
# # USER comuser


# Set working directory
WORKDIR /home/src/ccpp-scm/
ENV SCM_WORK=/home
ENV SCM_ROOT=/home/src/ccpp-scm/

# For interactive use, vim mouse settings are infuriating
RUN echo "set mouse=" > ~/.vimrc

# only download test data when PR is being tested
# ENTRYPOINT ["sh", "-c", "\
# if [ -n \"$PR_NUMBER\" ]; then \
#   ./contrib/get_aerosol_climo.sh && \
#   ./contrib/get_all_static_data.sh && \
#   ./contrib/get_thompson_tables.sh; \
# fi && \
# cd /home/src/ccpp-scm/scm/bin"]
