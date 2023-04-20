FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=rootpassword \
    MYSQL_DATABASE=job_data \
    MYSQL_USER=jobuser \
    MYSQL_PASSWORD=jobpassword

COPY ./init /docker-entrypoint-initdb.d/

EXPOSE 3306

# Thiết lập lệnh để chạy dịch vụ db
CMD ["mysqld", "--default-authentication-plugin=mysql_native_password"]
