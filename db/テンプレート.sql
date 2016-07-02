use fudosan;

#SELECT * FROM city_name where cityId = 992;
#select * from city_name where name like '八潮市';

#select * from town_name where name like '%鶴ヶ丘';
#select * from town_name where townId = 13306;
#select * from town where id = 16675;

#select * from city_name
#	left join town on town.cityId = city_name.cityId
#	left join town_name on town.id = town_name.townId and town_name.name like '%中島';

#select * from town_name
#    join town on town.id = town_name.townId and town.cityId = 1006;
    
#select * from town_name
#	join town on cityId = 1144;

#select * from town where id = 14435;

#insert into city_name (name, cityId) values ('毛呂山町', 999);
#insert into town_name (name, townId) values ('大字二丁目', 12762);

#select * from town_name
#	right join town on town_name.town_id = town.id;

#UPDATE `fudosan`.`town_name`
#SET
#`name` = '瀬戸上灰毛',
#`townId` = 18394
#WHERE name  = ' 瀬戸上灰毛';

#INSERT INTO town_name (name, townId) VALUES ('沖ノ上', 18396);
#INSERT INTO town (cityId) VALUES (949);

#select * from town order by id desc limit 1
#select * from town_name where name = '道佛';
#delete from town_name where name like '道佛' limit 1;

#select * from bukken limit 10;
