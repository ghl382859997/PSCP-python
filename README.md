# PSCP-python

该脚本实现了类似于scp的功能
包含了获取远程文件(本来有获取整个远程文件夹的功能,但是我自己没什么需求，就懒得写了--)

可通过vscode编译源文件，pyinstaller生成exe


脚本执行命令   pscp.exe <目标主机用户名> <目标主机密码> <目标主机IP> <本地文件> <远程路径> <操作类型>
当需要把本地文件发送给远程主机的时候，会自动查看本地文件路径是文件还是文件夹，然后执行当对应的操作
