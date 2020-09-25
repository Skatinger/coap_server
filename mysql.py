
/run/mysqld/mysqld.sock

docker run --name mysql -p 3306 -e MYSQL_ROOT_PASSWORD=my-1234 -d mysql:latest