MAKEFLAGS += -s

all:
	rm -rf Agent/Bin/*
	rm -rf Shellcode/Bin/*
	make -C Agent
	make -C Shellcode