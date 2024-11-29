FROM alpine:latest
MAINTAINER jinhill
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add --no-cache \
    fontconfig \
    ttf-dejavu \
    font-noto \
    supervisor \
    py3-flask \
    && rm -rf /var/cache/apk/*
# 创建字体目录
RUN mkdir -p /usr/local/share/fonts
# 创建一个目录用于挂载文件
RUN mkdir -p /data
RUN apk update && apk add libreoffice

EXPOSE 8000

# 设置工作目录
WORKDIR /data

# 复制启动脚本到容器中
COPY office.py /usr/local/bin/office.py
RUN chmod +x /usr/local/bin/office.py
COPY supervisord.conf /etc/supervisord.conf

# 配置容器启动flask
# CMD ["./office.py"]
# 启动守护进程supervisord,自动拉起libreoffice
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
