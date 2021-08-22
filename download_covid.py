# http://ibdf02.it.mvd.ru/vigr/index.php
# http://ibdf02.it.mvd.ru/vigr/vigr_covid.php
# Иностранцы: http://ibdf02.it.mvd.ru/vigr/vigr_covid_ino.php

import requests
import conn_site
import re
import os


def get_table_ino(arg1, arg2):
    # Функция принимает 2 аргумента:
    #   1) arg1 - cookie сайта (sid & ssh),
    #   2) arg2 - текущая дата сайта
    # Функция возвращает текст, куда ГИАЦ выкладывает новые файлы по иностранным гражданам
    sid = arg1[:5]
    ssh = arg1[7:]
    #     # переформатируем куки из sid=?, ssh=? в sid?; ssh=?
    cookie = (sid + '; ' + ssh)
    date = arg2
    print(f'ТЕСТ функции get_table_ino\nПолучаем данные для подключения к http://ibdf02.it.mvd.ru/vigr/vigr_covid_ino.php'
          f'\nПолные cookie сайта: {arg1}\nОтформатированные cookie: {cookie}'
          f'\nДата сайта: {date}')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'ibdf02.it.mvd.ru',
        'If-Modified-Since': date,
        'Referer': 'http://ibdf02.it.mvd.ru/vigr/vigr_covid.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }

    # Подключаемся с нашими заголовками и данными к сайту
    response = requests.get('http://ibdf02.it.mvd.ru/vigr/vigr_covid_ino.php', headers=headers)
    return response.text


def search_string_ino(arg1):
    # Функция получает в arg1 - html содержимое со списком файлов для скачивания из функции get_table_ino()
    # Функция возвращает:
    # - две новых ссылки на скачивание файлов иностранцы въезд и выезд
    # - два новых имени файлов по этим ссылкам
    text = arg1
    #print(text)
    # Выполняем поиск по полученному тексту и находим все сслыки в виде списка
    # Поиск выполняется: ищем dld.php + любые символы до символа ' .Знак "?" - минимальное количество совпадений
    # Получеам список совпадений и сохраняем его в links
    links = re.findall("dld\.php.*?'", text)
    # получаем первую ссылку и обрезаем символ '
    ino = links[0][:-1]
    # получаем вторую ссылку и обрезаем символ '
    ino_out = links[1][:-1]
    print(f'ТЕСТ функции search_string_ino\nСсылка на файл ino_*: \t\t{ino} \nСсылка на файл ino_out_*: \t{ino_out}')
    # Получаем имена файлов, которыми будут называться скачанные файлы с сайта
    names_files = re.findall("ino_.*?.csv",text)
    # Получаем имена файлов
    ino_name = names_files[0]
    ino_out_name = names_files[1]
    print(f'Имя файла ino: \t{ino_name}\nИмя файла ino_out: {ino_out_name}')
    return ino, ino_out, ino_name, ino_out_name


def check_exist_file(arg1, arg2):
    # Проверка существования файлов в корне проекта. Если файлы есть - возвращает True, иначе False
    path_ino_name = arg1
    path_ino_out_name = arg2
    if not (os.path.exists(path_ino_name) and os.path.exists(path_ino_out_name)):
        #print('Файлов не существует!')
        return False
    else:
        #print('Файлы существуют!')
        return True


def download_ino(arg1, arg2, arg3, arg4, arg5):
    # Функция принимает аргументы:
    # arg1 - cookie сайта, которые разбиваем его на sid и ssh
    # arg2 - ссылку на скачивание файла ino_(н-р: dld.php?tip=1&id=17708292)
    # arg3 - ссылку на скачивание файла ino_out_ (н-р: dld.php?tip=2&id=17708292)
    # arg4 - имя файла ino_, котрый мы скачаем (н-р: ino_20210618.csv)
    # arg5 - имя файла ino_out_, котрый мы скачаем (н-р: ino_out_20210618.csv)
    sid = arg1[:5]
    print(f'ТЕСТ функции download_ino\nИмя заголовка sid: {sid}')
    ssh = arg1[7:]
    print(f'\nИмя заголовка ssh: {ssh}')
    # переформатируем куки из sid=?, ssh=? в sid?; ssh=?)
    cookie = (sid + '; ' + ssh)
    # ino присваивается ссылка на файл ino_*
    ino = arg2
    # ino_out присваивается ссылка на файл ino_out_*
    ino_out = arg3
    print(f'\nСсылка на файл ino_*: {ino}\nСсылка на файл ino_out_*: {ino_out}'
          f'\n----------------------------------------------------'
          f'\nНачалось скачиваение файлов, ожидайте завершения...'
          f'\n----------------------------------------------------')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'ibdf02.it.mvd.ru',
        'Referer': 'http://ibdf02.it.mvd.ru/vigr/vigr_covid_ino.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }
    # Переходим по ссылке для скачивания файла ino_*
    response = requests.get(f'http://ibdf02.it.mvd.ru/vigr/{ino}', headers=headers)
    #print(response.text)
    ino_file_name = arg4
    # Создаем файл № 1
    file = open(ino_file_name, "w")
    file.write(response.text)
    file.close()
    # Переходим по ссылке для скачивания файла ino_out_*
    response = requests.get(f'http://ibdf02.it.mvd.ru/vigr/{ino_out}', headers=headers)
    ino_out_file_name = arg5
    # Создаем файл № 2
    file = open(ino_out_file_name, "w")
    file.write(response.text)
    file.close()
    print('Скачивание файлов завершено')


# Если скрипт запущен как основной, то выполнится следующее:
if __name__ == '__main__':
    user_login, user_password = conn_site.get_user_login_and_pass()
    headers_site = conn_site.get_headers_site(user_login, user_password)
    cookie_site = headers_site.headers['Set-Cookie']
    date_site = headers_site.headers['Date']
    text = get_table_ino(arg1=cookie_site, arg2=date_site)
    ino_link, ino_out_link, ino_name, ino_out_name = search_string_ino(text)
    if check_exist_file(ino_name, ino_out_name):
        download_ino(arg1=cookie_site, arg2=ino_link, arg3=ino_out_link, arg4=ino_name, arg5=ino_out_name)