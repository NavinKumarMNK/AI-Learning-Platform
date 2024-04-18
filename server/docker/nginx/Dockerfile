FROM nginx:latest

COPY ./nginx.conf.template /etc/nginx/conf.d/nginx.conf.template

CMD ["/bin/bash" , "-c" , "envsubst < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"]
