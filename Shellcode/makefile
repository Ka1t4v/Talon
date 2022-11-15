MAKEFLAGS += -s

CCX64	= x86_64-w64-mingw32-gcc
CCX86	= i686-w64-mingw32-gcc

CFLAGS	=  -Os -fno-asynchronous-unwind-tables -nostdlib
CFLAGS 	+= -fno-ident -fpack-struct=8 -falign-functions=1
CFLAGS  += -s -ffunction-sections -falign-jumps=1 -w
CFLAGS	+= -falign-labels=1 -fPIC -Wl,-TScripts/Linker.ld
CFLAGS	+= -Wl,-s,--no-seh,--enable-stdcall-fixup

EXECUTABLE_X64 = Bin/Shellcode.x64.exe

all: x64

x64:
	printf "\033[0;36m[*]\033[0m Compile x64 executable...\n"
	nasm -f win64 Source/Asm/x64/Asm.s -o Bin/Asm.x64.o
	$(CCX64) Source/*.c Bin/Asm.x64.o -o $(EXECUTABLE_X64) $(CFLAGS) -I Include -masm=intel
	printf "\033[0;36m[*]\033[0m Finished Compile...\n"



