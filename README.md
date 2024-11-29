This is Libreoffice headless based on Alpine

podman build -t libreoffice:1.0 .  

podman run -d --name office -v /path/to/data:/data -p 8100:8100 libreoffice:1.0  
