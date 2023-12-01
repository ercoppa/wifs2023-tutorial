CFLAGS ?= -g -w

all: run

run: build
	afl-fuzz -i seeds/ -o out ./target

clean:
	@rm -f target

build: target.c
	AFL_USE_ASAN=1 afl-clang-fast ${CFLAGS} target.c -o target

