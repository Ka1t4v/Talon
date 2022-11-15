# Talon

Talon is a 3rd party agent for Havoc written in C. It's very minimalistic and it's meant to show how to work with the Havoc service api.
Talon.py is the script that handles callbacks, register reqeuest and tasks by interacting with the Havoc service api. 

compile agent:
```
cd Talon
make
python build.py
```
The agent will be generated in the Agent/Bin directory

start agent handler:
```
python Talon.py
```

[+] 增加了dll和shellcode的实现

[+] 修复了下载文件和命令结果输出的编码问题



