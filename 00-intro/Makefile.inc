all: build
	rm -rf ../queue || echo "Nothing to clean"
	python3 -u fuzzer.py ../target

build:
	${CC} -o ../target ../target.c

start:
	# You do not need to use it. We use this container image
	# just because we use it in the second part and it
	# contains all we need also for the first part
	docker run --rm -ti -u 1000:1000 -v `pwd`/../:/AFLplusplus/workdir -w /AFLplusplus/workdir/`basename ${PWD}` aflplusplus/aflplusplus
