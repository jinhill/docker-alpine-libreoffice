#!/bin/sh

# 启动 LibreOffice 服务
libreoffice --nologo --norestore --invisible --headless --accept='socket,host=0,port=8100,tcpNoDelay=1;urp;'

# 保持容器运行，等待宿主机执行命令
while :; do sleep 2073600; done
