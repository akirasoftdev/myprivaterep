use fudosan
SELECT
    (price.price / bukken.occupiedArea),
    Year(bukken.year) - 1970,
    bukken.occupiedArea,
    access.walkTime,
    posted_price.price,
    rosen_price.price,
    bukken.url
FROM
    (bukken
    INNER JOIN rosen_price ON rosen_price.townId = bukken.townId)
WHERE price.price < 40000
AND   bukken.occupiedArea < 200
AND   access.walkTime < 30
AND   access.walkTime >= 0
INTO outfile '/var/lib/mysql-files/mansion.csv' FIELDS TERMINATED BY ',';
