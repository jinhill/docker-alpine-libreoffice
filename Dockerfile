FROM alpine:latest
MAINTAINER jinhill
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add --no-cache \
    fontconfig \
    ttf-dejavu \
    && rm -rf /var/cache/apk/*
# 创建字体目录
RUN mkdir -p /usr/local/share/fonts
# 创建一个目录用于挂载文件
RUN mkdir -p /data

RUN apk update && apk add libreoffice \
        font-noto

EXPOSE 8000



# 设置工作目录
WORKDIR /data

# 复制启动脚本到容器中
COPY office.py office.py
RUN chmod +x office.py

# 配置容器启动flask
CMD ["./office.py"]
