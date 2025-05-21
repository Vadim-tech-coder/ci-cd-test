Ответы на вопросы:
=
1. Вопрос: 
    > Телефоны какого цвета чаще всего покупают?

    Для решения использовал следующий запрос, в котором сначала все продажи телефонов группируются по ид. телефона, считается количество сгруппированных записей, записи сортируются по убыванию и берется ид. первой записи для выборки из таблицы с описанием телефонов.

    ```sql        
    SELECT tp.*
    FROM table_phones tp
    WHERE tp.id = (
      SELECT phone_id
      FROM (
        SELECT COUNT(*) AS cnt, phone_id
        FROM TABLE_CHECKOUT
        GROUP BY phone_id
        ORDER BY cnt DESC
        LIMIT 1
      ) AS max_phone
    );
    ```
Ответ по вопросу 1:

![Ответ: задача №2](./Задача%20№2.png)

2. Вопрос: 
    > Какие телефоны чаще покупают: красные или синие?

    Для решения использовал следующие запросы, в которых считаем количество продаж для ид. телефонов, которые соответствуют нужному условию(цвет: синий или красный). 
    
   ```sql        
   SELECT COUNT(*) 
   from table_checkout tc 
   WHERE tc.phone_id  IN 
   (SELECT id 
   from table_phones tp 
   where colour = 'синий')
   ```
   и 
   ```sql
   SELECT COUNT(*) 
   from table_checkout tc 
   WHERE tc.phone_id IN 
   (SELECT id 
   from table_phones tp 
   where colour = 'красный')
   ```

Ответ по вопросу 2: 
Количество проданных синих телефонов - 500, красных - 429, т.е. синих продано больше. 

3. Вопрос: 
    > Какой самый непопулярный цвет телефона?

    Для решения использовал следующий запрос, в котором считаем количество продаж для всех ид. телефонов,группируем по ид. телефона, сортируем по возрастанию и выбираем ид. первой записи, которую изспользуем для выборки из таблицы с описанием телефона.     
 
   ```sql        
   SELECT * FROM table_phones tp 
   WHERE ID = (SELECT phone FROM 
   (SELECT COUNT(*) AS COUNT, phone_id AS phone 
   from table_checkout tc 
   GROUP BY phone_id 
   ORDER BY COUNT ASC 
   LIMIT 1))
   ```
Ответ на 3 вопрос: 

![Ответ: задача №3](./Задание%20№3.png)

