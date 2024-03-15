#!/bin/bash

ml purge

module use etc/modules

ml derecho_intel
ml emacs
ml cmake
ml esmf
ml fms
ml crtm
ml g2
ml g2tmplwd

ml rm python
ml conda
ml netcdf-c netcdf-fortran
