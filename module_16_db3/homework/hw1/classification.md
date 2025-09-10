## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

|   Тип связи    | Таблица 1       | Таблица 2 |
|:--------------:|-----------------|-----------|
| Один ко многим | movie_direction | director  |
| Один ко многим | movie_direction | movie     |
| Один к одному  | oscar_awarded   | movie     |
| Один ко многим | movie_cast      | movie     |
| Один ко многим | movie_cast      | actors    |
