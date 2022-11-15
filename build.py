#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pefile
import argparse
import os

if __name__ in '__main__':
    os.system('')
    try:
        parser = argparse.ArgumentParser( description = 'Extracts shellcode from a PE.' );
        parser.add_argument( '-f', help = 'Path to the source executable', type = str ,default='Shellcode/Bin/Shellcode.x64.exe');
        parser.add_argument( '-o', help = 'Path to store the output raw binary', type = str ,default='Shellcode/Bin/Shellcode.x64.bin');
        option = parser.parse_args();

        PeExe = pefile.PE( option.f );
        PeSec = PeExe.sections[0].get_data();

        if PeSec.find( b'ENDOFCODE' ) != None:
            ScRaw = PeSec[ : PeSec.find( b'ENDOFCODE' ) ];
            f = open( option.o, 'wb+' );
            f.write( ScRaw );
            f.close();
        else:
            print('[!] error: no ending tag');
    except Exception as e:
        print( '[!] error: {}'.format( e ) );

    loader = open('Shellcode/Bin/Shellcode.x64.bin','rb').read()

    with open('Agent/Bin/Talon.dll','rb') as f2:
        shellcode = loader+f2.read()
        with open('Agent/Bin/Talon.bin','wb') as f3:
            f3.write(shellcode)
      


