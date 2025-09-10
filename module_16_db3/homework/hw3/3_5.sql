Select DISTINCT name FROM Battles B
JOIN Outcomes O ON B.name=O.battle
WHERE ship IN
(SELECT name FROM Ships S join Classes C ON S.class=C.class WHERE C.class='Kongo')
