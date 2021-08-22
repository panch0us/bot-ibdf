import ftplib


def upload_file_to_ftp(arg1, arg2):
    list_print_dirrectory_on_ftp = []
    # Выгрузка файла на ftp
    # Подлючаемся и авторизуемся к ftp (важен параметр кодировки!)
    ftp = ftplib.FTP(host='', user='uvm', passwd='', timeout=100, encoding='cp1251')
    # Указываем путь к дирректории на ftp куда будет сохранен файл
    path_on_ftp = arg1
    # Указываем имя файла для загрузки (файл с этим именем будет искать в дирректории проекта)
    name_file_to_upload = arg2
    # Переходим в нужную дирректорию на ftp
    ftp.cwd(path_on_ftp)
    # Сохраняем список всех файлов в дирректории FTP
    list_files = ftp.nlst()
    print(f'Проверяем, есть ли скачанный файл: "{name_file_to_upload}" '
          f'в дирректории "{path_on_ftp}" на FTP сервере.')
    # Проверяем нет ли файла на FTP, который мы выгружаем. Если нет - выгружаем.
    if name_file_to_upload in list_files:
        print(f'Файл "{name_file_to_upload}" уже находится на FTP. Выгрузка отменена!')
    else:
        # Открываем ранее скачанный файл и сохраняем его в переменную file_to_upload
        try:
            with open(name_file_to_upload, 'rb') as file_to_upload:
                # Выгружаем file_to_upload на ftp (имя файла - name_file_to_upload)
                ftp.storbinary('STOR ' + name_file_to_upload, file_to_upload)
                print(f'Выгрузка файла "{name_file_to_upload}" на ftp завершена')
        except:
            print('Общее исключение: ошибка выгрузки файла')


if __name__ == '__main__':
    path_on_ftp = 'Obmen_IC_UVM/Граница/COVID-19 иностранцы'
    name_file_to_upload = 'ino_20210812.csv'
    upload_file_to_ftp(arg1=path_on_ftp, arg2=name_file_to_upload)