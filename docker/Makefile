all: build

build: build-gnu
build-gnu:
	docker build -t dtcenter/ccpp-scm:gnu gnu
	docker tag dtcenter/ccpp-scm:gnu dtcenter/ccpp-scm:latest
build-nvhpc:
	docker build -t dtcenter/ccpp-scm:nvhpc nvidia
build-intel:
	docker build -t dtcenter/ccpp-scm:intel intel

run: run-gnu
run-gnu:
	docker run -it --name ccpp-scm-gnu dtcenter/ccpp-scm:gnu
run-intel:
	docker run -it --name ccpp-scm-intel dtcenter/ccpp-scm:intel
run-nvhpc:
	docker run -it --name ccpp-scm-nvhpc dtcenter/ccpp-scm:nvhpc

pull:
	docker pull dtcenter/ccpp-scm
