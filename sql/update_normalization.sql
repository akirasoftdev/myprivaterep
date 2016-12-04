delete from bukken_normalization;

insert into bukken_normalization
	(bukkenId, year, occupiedArea, price, walkTime, rosenPrice)
select
	bukken.id as bukkenId,
    (year(bukken.year) - 1970 - 31.1387) / 7.914659544237533 as year,
    (bukken.occupiedArea - 6486.1952) / 2117.5691044636487 as occupiedArea,
    bukken.price as price,
    (bukken.walkTime - 10.0463) / 7.09756102948334 as walkTime,
    (rosen_price.price - 365.8280) / 399.1240927984568 as rosenPrice
from
	bukken
left join
	rosen_price
on rosen_price.townId = bukken.townId
where rosen_price.price is not null;
