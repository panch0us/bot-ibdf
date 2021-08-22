import conn_site
import download_covid
import conn_ftp
import re
import sys
import datetime
import time


print('----------------------------------------------------\n'
      'Проверьте актуальность текущей даты и времени на ПК!\n'
      '----------------------------------------------------')


def connect(arg1, arg2):
    # Подключение к сайту
    user_login = arg1
    user_password = arg2
    try:
        # Получаем куки сайта ИБД-Ф
        headers_site = conn_site.get_headers_site(user_login, user_password)
        # Из кук сайта сохраняем Сет-куки и дату
        cookie_site = headers_site.headers['Set-Cookie']
        date_site = headers_site.headers['Date']
        # В полученных куках ищем слово SSH. Если оно есть - значит авторизация прошла успешно
        if re.findall(".*SSH", cookie_site):
            print('Авторизация прошла успешно')
            return cookie_site, date_site
        else:
            print('Ошибка авторизации, возможно вы указали неверный логин или пароль')
            # завершаем выполнение скрипта
            sys.exit()
    except SystemExit:
        # ловим исключение от sys.exit() и повторяем выход из скрипта (возможно нужно заменить на os._exit(1)
        print('Исключение SystemExit - выход из скрипта (sys.exit())')
        sys.exit()


def download(arg1, arg2):
    # Скачивание файлов
    cookie_site = arg1
    date_site = arg2
    # Получаем html текст из таблицы на странице размещения файлов для скачивания иностранных граждан
    text_site = download_covid.get_table_ino(arg1=cookie_site, arg2=date_site)
    # Получаем две новых ссылки для скачивания иностранцев въезд и выезд
    # Получаем два правильных имени файлов иностранцев въезд и выезд для дальнейшего сохранения этих файлов
    ino_link, ino_out_link, ino_name, ino_out_name = download_covid.search_string_ino(text_site)
    # Получаем текущую дату из которой вычитаем 1 день
    current_date_minus_one_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    # Проверяем дату выложенных файлов. Дата должна быть на 1 день меньше текущей даты.
    # Дата выложенных файлов и текущей даты минус один день (20210811)
    if (ino_name[4:-4] and ino_out_name[8:-4]) == current_date_minus_one_day:
        print('Файлы для скачивания за вчерашний день!')
        # Проверяем скачаны уже файлы или нет. Если нет (False) - скачиваем.
        if download_covid.check_exist_file(arg1=ino_name, arg2=ino_out_name) == False:
            # Скачиваем файлы иностранцев
            download_covid.download_ino(arg1=cookie_site, arg2=ino_link, arg3=ino_out_link, arg4=ino_name, arg5=ino_out_name)
            # Сохраняем в список файлов названия скачанных файлов
            list_path_on_ftp = ['Obmen_IC_UVM/Граница/COVID-19 иностранцы',
                                'Obmen_IC_UVM/Граница/COVID-19 иностранцы выезд']
            list_files_in_main_directory = [ino_name, ino_out_name]
            # Когда файлы скачаны, вызываем функцию для выгрузки их на FTP
            # В функцию передаем поочередно в цикле for - путь на фтп и имя файла для выгрузки
            for path, file in zip(list_path_on_ftp, list_files_in_main_directory):
                conn_ftp.upload_file_to_ftp(arg1=path, arg2=file)
        else:
            print('----------------------------------------------------\n'
                  'Файлы уже скачены!\n'
                  '----------------------------------------------------\n')
            # приостанавиливаем выполнение на 1 час
            time.sleep(3600)
    else:
        print(f'----------------------------------------------------\n'
              f'Скачивание файлов не началось, т.к. ожидаются новые файлы\n'
              f'На сайте выложены файлы за дату:\n'
              f'Иностранцы въезд: {ino_name[4:-4]}\n'
              f'Иностранцы выезд: {ino_out_name[4:-4]}\n'
              f'----------------------------------------------------\n')


if __name__ == '__main__':
    # Авторизация пользователя. Получаем от пользователя логин и пароль
    user_login, user_password = conn_site.get_user_login_and_pass()
    while True:
        if conn_site.test_connect_ibdf() == 200:
            cookie_site, date_site = connect(arg1=user_login, arg2=user_password)
            download(arg1=cookie_site, arg2=date_site)
            time.sleep(3600)
        else:
            print('Вероятно что-то =-)')
            time.sleep(60)
