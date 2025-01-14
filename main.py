import time
from datetime import datetime, timezone
from requests_html import AsyncHTMLSession
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# URL страницы для парсинга
url = 'https://www.profinance.ru/currency_usd.asp?ref=tjournal.ru'

# Создаем асинхронную сессию
session = AsyncHTMLSession()


# Функция для получения данных валют
async def get_currency_data():
    try:
        response = await session.get(url, timeout=10)  # Устанавливаем таймаут на 10 секунд
        await response.html.arender(sleep=10)  # Рендерим JavaScript с увеличенным временем ожидания

        data = {}

        # Извлекаем данные
        data['USDRUB'] = response.html.find('#lp_29', first=True).text.strip()
        data['USDRUB_F'] = response.html.find('#lp_USDRUB_F', first=True).text.strip()
        data['USDRUB_FUT'] = response.html.find('#lp_RUB_FUT', first=True).text.strip()

        data['EURRUB'] = response.html.find('#lp_30', first=True).text.strip()
        data['EURRUB_F'] = response.html.find('#lp_EURRUB_F', first=True).text.strip()
        data['EURRUB_FUT'] = response.html.find('#lp_ERUB_FUT', first=True).text.strip()

        data['CNYRUB'] = response.html.find('#lp_CNY_RUB', first=True).text.strip()
        data['CNYRUB_F'] = response.html.find('#lp_CNYRUB_F', first=True).text.strip()
        data['CNYRUB_FUT'] = response.html.find('#lp_CNYRUB_FUT', first=True).text.strip()

        logging.info("Данные успешно получены.")
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return None

    return data


# Функция для записи данных в файл для конкретного актива
def write_to_file(filename, currency_type, data):
    try:
        with open(filename, 'a') as f:
            utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            f.write(
                f"{utc_time}, {currency_type}: {data[currency_type]}, "
                f"{currency_type}_F: {data[currency_type + '_F']}, "
                f"{currency_type}_FUT: {data[currency_type + '_FUT']}\n")
    except Exception as e:
        logging.error(f"Ошибка при записи данных: {e}")


# Основной цикл для получения данных каждые 15 минут
async def main():
    while True:
        try:
            currency_data = await get_currency_data()

            if currency_data:  # Проверяем, что данные успешно получены перед записью в файл
                write_to_file('usd_data.txt', 'USDRUB', currency_data)
                write_to_file('eur_data.txt', 'EURRUB', currency_data)
                write_to_file('cny_data.txt', 'CNYRUB', currency_data)
            else:
                logging.warning("Не удалось получить данные.")

            await asyncio.sleep(900)  # Ждем 15 минут перед следующим запросом

        except Exception as e:
            logging.error(f"Произошла ошибка в основном цикле: {e}. Перезапуск через 5 секунд...")
            await asyncio.sleep(5)  # Ждем перед перезапуском в случае ошибки


if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # Получаем текущий цикл событий
    loop.run_until_complete(main())  # Запускаем основную функцию
