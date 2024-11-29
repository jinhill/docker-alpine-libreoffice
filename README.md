This is Libreoffice headless based on Alpine  
podman build -t libreoffice:1.0 .  
#podman run -d --name office -v /path/to/data:/data -p 8100:8000 libreoffice:1.0  
从挂载目录
podman run -d --name office -v /path/to/data:/data -v /path/to/font:/usr/local/share/fonts -p 8100:8100 libreoffice:1.0  
#更新字体  
podman exec -it office sh -c "fc-cache -f -v"  
#使用
time podman exec -it office soffice --headless --convert-to pdf /data/document.docx --outdir /data  
time curl http://localhost:8100/converter?file=/data/test.docx  
time curl -X POST -F "file=@/data/test3.doc" http://localhost:8100/converter -o test.pdf  
