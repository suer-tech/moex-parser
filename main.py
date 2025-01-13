import time
from datetime import datetime, timezone
from requests_html import HTMLSession

# URL страницы для парсинга
url = 'https://www.profinance.ru/currency_usd.asp?ref=tjournal.ru'

# Создаем сессию
session = HTMLSession()


# Функция для получения данных валют
def get_currency_data():
    response = session.get(url)
    response.html.render(sleep=3)  # Рендерим JavaScript

    data = {}

    # Извлекаем данные
    try:
        data['USDRUB'] = response.html.find('#lp_29', first=True).text.strip()
        data['USDRUB_F'] = response.html.find('#lp_USDRUB_F', first=True).text.strip()
        data['USDRUB_FUT'] = response.html.find('#lp_RUB_FUT', first=True).text.strip()

        data['EURRUB'] = response.html.find('#lp_30', first=True).text.strip()
        data['EURRUB_F'] = response.html.find('#lp_EURRUB_F', first=True).text.strip()
        data['EURRUB_FUT'] = response.html.find('#lp_ERUB_FUT', first=True).text.strip()

        data['CNYRUB'] = response.html.find('#lp_CNY_RUB', first=True).text.strip()
        data['CNYRUB_F'] = response.html.find('#lp_CNYRUB_F', first=True).text.strip()
        data['CNYRUB_FUT'] = response.html.find('#lp_CNYRUB_FUT', first=True).text.strip()

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

    return data

# Запуск функции для тестирования
currency_data = get_currency_data()
print(currency_data)


# Функция для записи данных в файл для конкретного актива
def write_to_file(filename, currency_type, data):
    try:
        with open(filename, 'a') as f:
            utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            f.write(
                f"{utc_time}, {currency_type}: {data[currency_type]}, {currency_type}_F: {data[currency_type + '_F']}, {currency_type}_FUT: {data[currency_type + '_FUT']}\n")
    except Exception as e:
        print(f"Ошибка при записи данных: {e}")


# Основной цикл для получения данных каждые 15 минут
while True:
    currency_data = get_currency_data()

    if currency_data:  # Проверяем, что данные успешно получены перед записью в файл
        write_to_file('usd_data.txt', 'USDRUB', currency_data)
        write_to_file('eur_data.txt', 'EURRUB', currency_data)
        write_to_file('cny_data.txt', 'CNYRUB', currency_data)
    else:
        print("Не удалось получить данные.")

    time.sleep(900)  # Ждем 15 минут перед следующим запросом
