rm ~/work/mysql/mysql_data/mysql-files/mansion.csv
mysql -h 127.0.0.1 -P 3306 -u root --password=secret < export.sql
cp ~/work/mysql/mysql_data/mysql-files/mansion.csv .