select avg(occupiedArea), std(occupiedArea) from bukken;
select avg(year(year) - 1970), std(year(year) - 1970) from bukken;
select avg(walkTime), std(walkTime) from bukken;
select avg(rosen_price.price), std(rosen_price.price) from bukken
	left join  rosen_price on bukken.townId = rosen_price.townId;