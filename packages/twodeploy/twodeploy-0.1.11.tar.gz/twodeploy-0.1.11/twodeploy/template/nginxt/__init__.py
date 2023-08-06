Dockerfile = '''
FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY REMOTE_HOSTNAME_HERE.key /etc/nginx/conf.d/REMOTE_HOSTNAME_HERE.key
COPY REMOTE_HOSTNAME_HERE.crt /etc/nginx/conf.d/REMOTE_HOSTNAME_HERE.crt
'''

conf = '''
upstream loadbalancer {
# server 172.17.0.1:7281;
# server 172.17.0.1:7282;
SERVER_URLS_HERE
}

# # 80
# server {
# listen 80;
# server_name HOSTNAME_HERE;  
# return 302 https://$server_name$request_uri;
# }

# # 443
# server {
# listen 443 ssl;
# server_name HOSTNAME_HERE;
# ssl_certificate /etc/nginx/conf.d/HOSTNAME_HERE.crt;
# ssl_certificate_key /etc/nginx/conf.d/HOSTNAME_HERE.key;
# location / {
# proxy_set_header Host $host;
# proxy_pass http://loadbalancer;
# }}

server {
# server_name HOSTNAME_HERE;
location / {
proxy_set_header Host $host;
proxy_pass http://loadbalancer;
}}
'''

sh = '''
# Building
docker build -t NGINX_IMAGE_NAME_HERE NGINX_BASE_HERE -f DOCKER_PATH_HERE

# Detached Deploying
# ExternalPort:InternalPort
docker run --restart=on-failure -d -p EXTERNAL_PORT_HERE:80 NGINX_IMAGE_NAME_HERE
# docker run --restart=on-failure -d -p EXTERNAL_PORT_HERE:443 NGINX_IMAGE_NAME_HERE
'''

def read(arg):
    if(arg == 'sh'):
        return sh
    if(arg == 'conf'):
        return conf
    if(arg == 'Dockerfile'):
        return Dockerfile     
    return ''