.. _`chapter: testing`:

Testing
=========


Testing Overview
------------------

[TODO]


Precision:
-------------
To build in single precision the user can use the ``-D32BIT=1`` command line argument when setting up CMake. A user might be interested in how the output of any individual suite might turn out when compiling and running in single precision versus double precision. This capacity has been added in the ``precision_analysis.py`` tool found under the ``scme/etc/scripts`` directory.


.. _`precisinoanalysis`:
precision_analysis.py
Builds single and double precision versions of the code, runs them, compares the output and ggenerateds png images of the analysis. Without any arguments the script with configure, build, run, and perform post-processing analysis.


.. code:: bash

  ./precisionanalysis.py
      [--configure|--configure32|--configure64]
      [--build|--build32|--build64]
      [--run|--run32|--run64]
      [--post]
      [-h, --help]

Optional arguments:

#. ``--configure``: Configure both single and double precision CMake builds.
#. ``--configure32``: Configure single precision CMake build.
#. ``--configure64``: Configure double precision CMake build.

#. ``--build``: Build both single and double precision CMake builds.
#. ``--build32``: Build single precision CMake build.
#. ``--build64``: Build double precision CMake build.

#. ``--run``: Run both single and double precision CMake builds.
#. ``--run32``: Run single precision CMake build.
#. ``--run64``: Run double precision CMake build.

#. ``--post``: Perform post-processing of data and produce png files of the mean squared error of variables.
