# pip install mimesis - библиотека для генерации данных
from random import choice
from mimesis import Person
from mimesis import Finance
from mimesis.enums import Gender
from database import write_csv, write_json

def get_employee(id): # генерация строчки в базу данных
    person = Person('ru')
    finance = Finance('ru')
    gender = choice([Gender.MALE,Gender.FEMALE]) 
    mask = ["id", "last_name", "first_name", "position", "phone_number", "salary"]
    result = [int(id), person.last_name(gender=gender), person.first_name(gender=gender), 
                person.occupation().lower(), person.telephone(mask='+7-9##-###-####'), 
                float(finance.price())]
    return dict(zip(mask, result))


def generate(n):
    # n = 10 # строк в бд
    data = [get_employee(x) for x in range(1,n+1)]
    write_csv(data)
    write_json(data)

