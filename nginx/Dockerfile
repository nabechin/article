FROM nginx:1.19.1

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./html /etc/nginx/html
COPY ../app/static /usr/src/article/app/static

EXPOSE 80