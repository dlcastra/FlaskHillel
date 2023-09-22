import csv
import sqlite3

import requests
from faker import Faker
from flask import Flask, send_file, render_template

from setups import setup_customers, setup_tracks


app = Flask(__name__)

""" -- Головна сторінка і генератори -- """


@app.route('/')
def main_page():
    return (
        "<p>Як користуватися:\n"
        "<p>Напишіть у пошуковий рядок /requrements/, щоб побачити зміст файлу requrements.txt"
        "<p>Напишіть у пошуковий рядок /users/generate/'Ваша цифра'"
        ", щоб згенерувати певну кількість людей та їх email-и, за замовчуванням це буде 100"
        "<p>Напишіть у пошуковий рядок /mean/, щоб побачити середній зріст та вагу з файлу hw.csw"
        "<p>Напишіть у пошуковий рядок /space/, щоб побачити кількість космонафтів"
        "<p>Напишіть у пошуковий рядок /setup/, щоб згенерувати дані для бази даних"
        "<p>Напишіть у пошуковий рядок /first_name/, щоб побачити кількість імен і самі імена в базі даних"
        "<p>Напишіть у пошуковий рядок /tracks/, щоб побачити кількість треків в базі даних"
        "<p>Напишіть у пошуковий рядок /tracks-sec/, щоб побачити інформацію о треках"

    )


@app.route('/setup/')
def setups():
    setup_customers()
    setup_tracks()

    return "Ви згенерували дані для таблиці customers і tracks в біза даних flask"


""" -- Перша домашка по flask -- """


@app.route('/requrements/', methods=['GET'])
def requrements():
    # Висилаємо файл так, щоб його не пропонувало завантажити
    return send_file('tables_and_txt/requrements.txt', as_attachment=False)


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
    for person in response_in_json.get('people'):
        # Беремо всі імена космонафтів, щоб потім перевірити їх кількість ще раз
        names.append(person['name'])

    return f"Вказана кількість космонавтів {numbers_cosmonaut}, кількість після перевірки {len(names)}"


""" -- Друга домашка flask + SQLite"""


@app.route('/first_name/', methods=['GET'])
def get_customer_name():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute(""" SELECT first_name FROM customers """)
        customers = cur.fetchall()
        names_counter = len(customers)

        return render_template('customers.html', names_counter=names_counter, customers=customers)


@app.route('/tracks/', methods=['GET'])
def get_count_records_tracks():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute(""" SELECT id FROM tracks """)
        tracks = cur.fetchall()
        tracks_counter = len(tracks)

        return render_template('count_traks.html', tracks_counter=tracks_counter, tracks=tracks)


@app.route('/tracks-sec/', methods=['GET'])
def get_tracks_information():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute(""" SELECT id, singer, track_name, track_length, release_date FROM tracks """)
        tracks = cur.fetchall()

        return render_template('tracks_information.html',tracks=tracks)


""" --  Чатина для помилок -- """


@app.errorhandler(404)
def error_404(error):
    return '<h1 style="text-align:center; font-size:24px;">Ви робите щось не так((</h1>'


if __name__ == "__main__":
    app.run(debug=True)
