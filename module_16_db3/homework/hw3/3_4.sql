Select name
from ships
where class = name
union
select ship as name
from classes,outcomes
where classes.class = outcomes.ship