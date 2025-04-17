## Найденные ошибки:
- метод *set_name* было: <code>self.name = self.name</code> стало: <code>self.name = name</code>
- метод *get_name* было: <code>now: datetime.datetime = datetime.datetime.now()</code> стало: <code>now: datetime = datetime.now()</code>, и добавлен импорт datetime
- метод *get_name* было: <code>return self.yob - now.year</code> стало: <code>return now.year - self.yob</code>
- метод *set_address* было: <code>self.address == address</code> стало: <code>self.address = address</code>
- метод *is_homeless* было: <code>return address is None</code> стало: <code>return self.address is None</code>


