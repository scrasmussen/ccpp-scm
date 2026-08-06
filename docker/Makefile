DOCKER ?= docker
CONTEXT ?= ..
NETCDF_FORTRAN_VERSION ?= 4.6.2
FINAL_IMAGE ?= scm-gnu:latest

.PHONY: all build minimal netcdf nceplibs python finalize run clean

all: build

build: finalize

minimal:
	$(DOCKER) build \
		-f Dockerfile-gnu-minimal \
		-t minimal-toolchain:gnu \
		$(CONTEXT)

netcdf: minimal
	$(DOCKER) build \
		-f Dockerfile-add-netcdf \
		--build-arg TOOLCHAIN=gnu \
		--build-arg NFVERSION=$(NETCDF_FORTRAN_VERSION) \
		-t add-netcdf:gnu \
		$(CONTEXT)

nceplibs: netcdf
	$(DOCKER) build \
		-f Dockerfile-add-nceplibs \
		--build-arg TOOLCHAIN=gnu \
		-t add-nceplibs:gnu \
		$(CONTEXT)

python: nceplibs
	$(DOCKER) build \
		-f Dockerfile-add-python \
		--build-arg TOOLCHAIN=gnu \
		-t add-python:gnu \
		$(CONTEXT)

finalize: python
	$(DOCKER) build \
		-f Dockerfile-finalize \
		--build-arg TOOLCHAIN=gnu \
		-t $(FINAL_IMAGE) \
		$(CONTEXT)

run:
	@echo "From the top directory run"
	@echo "$$ docker run --rm -it --user "$$(id -u):$$(id -g)" --env HOME=/tmp -v "$${PWD}/../:/src" -w /src scm-gnu:latest"

clean:
	$(DOCKER) image rm \
		$(FINAL_IMAGE) \
		add-python:gnu \
		add-nceplibs:gnu \
		add-netcdf:gnu \
		minimal-toolchain:gnu
