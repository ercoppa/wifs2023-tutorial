CFLAGS ?= -g -w

all: run

run: build
	afl-fuzz -i seeds/ -o out -c ./target.cmplog -t 1000 -- ./target

clean:
	@rm -f target

build: target.c
	AFL_USE_ASAN=1 afl-clang-fast ${CFLAGS} target.c -o target
	AFL_USE_ASAN=1 AFL_LLVM_CMPLOG=1 afl-clang-fast ${CFLAGS} target.c -o target.cmplog