# Подключение к сайту ИБД-Ф "http://ibdf02.it.mvd.ru/login.php"
# для автоматизации загрузок файлов и выгрузок в орпеделенные места

# Импортируем библиотеку для подключения к сайтам
import requests
import re
import time


def test_connect_ibdf():
    # Получаем код статуса подключения к сайту (н-р 200 - успешное, 0 - ошибка подключения)"
    try:
        response = requests.get('http://ibdf02.it.mvd.ru/login.php')
        return response.status_code
    except requests.exceptions.ConnectionError:
        print('Ошибка подключения к сети. Проверьте настройки подключения. Попытка переподключения через 1 минуту...')
        return 0
    except:
        print('Ошибка подключения к сайту. Возможно сервис ИБД-Ф в настоящее время не доступен')
        return 0


def get_user_login_and_pass():
    # Истребует ввод логина и пароля от пользователя СУДИС
    # Возвращает логин и пароль пользователя
    user_login = input('Ведите логин пользователя СУДИС: ')
    user_password = input('Ведите пароль пользователя СУДИС: ')
    return user_login, user_password


def get_headers_site(arg1, arg2):
    # Принимает arg1 - имя пользователя, arg2 - пароль пользователя
    # Функция возвращает cookie сайта http://ibdf02.it.mvd.ru/login.php (uid и ssh)
    # Сохраняем заголовки ответа браузера к сайту http://ibdf02.it.mvd.ru/login.php
    user_login = arg1
    user_password = arg2
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Length': '53',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'SID=0; SSH=0',
        'Host': 'ibdf02.it.mvd.ru',
        'Origin': 'http://ibdf02.it.mvd.ru',
        'Referer': 'http://ibdf02.it.mvd.ru/login.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }
    # Подключаемся с нашими заголовками и данными к сайту
    response = requests.post('http://ibdf02.it.mvd.ru/login.php',
                             headers=headers,
                             data=[("login", user_login),
                                   ("parol", user_password),
                                   ("uin", ""),
                                   ("step", "2")])

    # Получаем ключ заголовка ответа (UID и SSH) нашего сайта и обрезаем его до SSH
    return response


# Если скрипт запущен как основной, то выполнится следующее:
if __name__ == '__main__':
    try:
        if test_connect_ibdf() == 200:
            print("Сайт доступен")
            # Авторизация на сайте
            user_login, user_password = get_user_login_and_pass()
            cookie_site = get_headers_site(user_login, user_password).headers['Set-Cookie']
            print(f"Cookie сайта: {cookie_site}")
            print(f"Дата сайта: {get_headers_site(user_login, user_password).headers['Date']}")
            # Если авторизация прошла успешно - c помощью "re" будет найден SSH в строке, если нет - ошибка авторизации
            if re.findall(".*SSH", cookie_site):
                print('Авторизация прошла успешно')
            else:
                print('Ошибка авторизации')
        else:
            # Если ответ от сайта не 200 - будет печататься текущий статус
            print(f'Статус подключения: {test_connect_ibdf()}')
    except:
        print('Ошибка подключения (сработал общий EXCEPT)')