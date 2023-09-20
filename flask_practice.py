from flask import Flask, send_file
from faker import Faker
from setups import setup_customers, setup_tracks
import csv
import requests


app = Flask(__name__)


@app.route('/')
def main_page():
    return (
        "<p>Як користуватися:\n"
        "<p>Напишіть у пошуковий рядок /requrements/, щоб побачити зміст файлу requrements.txt"
        "<p>Напишіть у пошуковий рядок /users/generate/'Ваша цифра'"
        ", щоб згенерувати певну кількість людей та їх email-и, за замовчуванням це буде 100"
        "<p>Напишіть у пошуковий рядок /mean/, щоб побачити середній зріст та вагу з файлу hw.csw"
        "<p>Напишіть у пошуковий рядок /space/, щоб побачити кількість космонафтів"
    )


@app.route('/requrements/', methods=['GET'])
def requrements():
    return send_file('tables_and_txt/requrements.txt', as_attachment=False)  # Висилаємо файл так, щоб його не пропонувало завантажити


@app.route('/users/generate/<int:generate>', methods=['GET'])
def user_generation(generate: int):
    fake = Faker()
    user_digit = generate

    default_quantity = [[fake.name(), fake.company_email()] for _ in range(100)]  # Кількість за замовчуванням
    user_quantity = [[fake.name(), fake.company_email()] for _ in range(user_digit)]  # Кількість користувача

    if user_digit > 0:
        return user_quantity

    return default_quantity


@app.route('/mean/', methods=['GET'])
def mean():
    get_file = 'tables_and_txt/hw.csv'
    heights = []
    weights = []

    with open(get_file, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:  # Вибераємо дані по індексах "Index"row[0], "Height"row[1], "Weight"row[2]
            try:
                heights.append(float(row[1]))
                weights.append(float(row[2]))

            except (ValueError, IndexError):  # Пропускаємо некоректні дані
                continue

    mean_height = sum(heights) / len(heights) * 2.54
    mean_weight = sum(weights) / len(weights) * 0.453592

    return (f"<p>Середній зріст: {mean_height} см"
            f"<p>Середня вага: {mean_weight} кг")


@app.route('/space/', methods=['GET'])
def cosmonaut_count():
    get_response = requests.get('http://api.open-notify.org/astros.json')
    response_in_json = get_response.json()
    numbers_cosmonaut = response_in_json.get('number')  # Беремо кількість космонафтів з json файлу

    names = []
    for person in response_in_json.get('people'):  # Беремо всі імена космонафтів, щоб потім перевірити їх кількість ще раз
        names.append(person['name'])

    return f"Вказана кількість космонавтів {numbers_cosmonaut}, кількість після перевірки {len(names)}"


@app.errorhandler(404)
def error_404(error):
    return '<h1 style="text-align:center; font-size:24px;">Ви робите щось не так((</h1>'


if __name__ == "__main__":
    setup_customers()
    setup_tracks()
    app.run(debug=True)
