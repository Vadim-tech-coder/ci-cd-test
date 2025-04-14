"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""
import sys

from flask import Flask
from datetime import datetime

app = Flask(__name__)
weekdays_tuple = ('понедельника', "вторника","среды","четверга", "пятницы", "субботы", "воскресенья") #Занимает меньше памяти
weekdays_list = ['понедельник', "вторник","среды","четверга", "пятницы", "субботы", "воскресенья"]
weekdays_dict = {0: 'понедельник', 1: "вторник", 2: "среды", 3: "четверга", 4: "пятницы", 5: "субботы", 6: "воскресенья"}

@app.route('/hello-world/<name>')
def hello_world(name):

    now_week_day = datetime.today().weekday()
    if now_week_day in (0,1,3,6):
        greeting = 'Хорошего'
    else:
        greeting = "Хорошей"
    return "Привет, {}! {} {}!".format(name, greeting,weekdays_tuple[now_week_day])


if __name__ == '__main__':
    app.run(debug=True)