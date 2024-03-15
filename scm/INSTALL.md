# Instruction for Building on Derecho
v4.0.0 has been updated to build and run on Derecho

## Setup Environment and Modules

### Setup Python with Conda
Install Conda Environment. This will take awhile but only needs to be done once. In the future skip to using `conda activate`.

```
$ ml conda
$ conda env create -f ../environment.yml
```

Load conda environment
```
$ conda activate scm_py38
```

### Load modules
```
$ source intel-env.sh
```
 or
```
$ . intel-env.sh
```

## Configure CMake
```
$ cmake -B build src/
```

## Build CMake
```
$ make -C build -j 4
```
