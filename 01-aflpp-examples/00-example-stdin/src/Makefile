CFLAGS ?= -g -w

all: 
	echo "Run AFL++ in QEMU or LLVM mode using targets: run-llvm, run-qemu"

run-llvm: build-llvm
	afl-fuzz -i seeds/ -o out -t 1000 -- ./target

run-qemu: build-qemu
	afl-fuzz -Q -i seeds/ -o out -t 1000 -- ./target

clean:
	@rm -f target

build-llvm: target.c
	AFL_USE_ASAN=1 afl-clang-fast ${CFLAGS} target.c -o target

build-qemu: target.c
	${CC} ${CFLAGS} target.c -o target

