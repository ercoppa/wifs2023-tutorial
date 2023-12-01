all: build
	rm -rf ../queue || echo "Nothing to clean"
	python3 -u fuzzer.py ../target

build:
	${CC} -o ../target ../target.c