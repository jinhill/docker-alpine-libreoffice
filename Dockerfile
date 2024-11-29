FROM alpine:latest
MAINTAINER jinhill
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add libreoffice \
        font-noto

EXPOSE 8100

# 创建一个目录用于挂载文件
RUN mkdir -p /data

# 设置工作目录
WORKDIR /data

# 复制启动脚本到容器中
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 配置容器启动时不自动运行 LibreOffice
CMD ["/bin/sh", "/start.sh"]
