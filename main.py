
import requests
from pprint import pprint
import os
import datetime
import time
import json
from alive_progress import alive_bar

TOKEN = ''
NAME = ''
OAUTH_URL = 'https://api.vk.com/method/'




class User():


    def __init__(self, token):
        self.token = token

    def download_vk(self):
        count = 5
        count_check = False

        while count_check == False:
            print()
            count = input("Введите количество фотографий для сохранения (по умолчанию - 5, оставить пустым): ")
            if count.isdigit() == True:
                count = int(count)
                if count > 0:
                    count_check = True
                else:
                    print()
                    print("Невозможно сохранить 0 фотографий")
                    print()
            else:
                print()
                print("Введена не цифра")
                print()

        response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                            'access_token': self.token,
                                'v': 5.126,
                                'album_id': 'profile',
                                'rev': '1',
                                'extended': '1',
                                'photo_sizes': '1',
                                'count': count
                            }
                            )

        # pprint(response.json())
        list_photos = response.json()['response']['items']

        final_list = []

        for items in list_photos:

            best_url = ''
            best_height = 0
            best_width = 0


            for sizes in items["sizes"]:
                best_size = best_height + best_width
                if (sizes['height'] + sizes['width'] ) > best_size:
                    best_url = sizes['url']
                    best_height = sizes['height']
                    best_width = sizes['width']
                    timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d %H_%M_%S_%f")
                    time.sleep(0.01)
            final_list.append(dict(likes = items["likes"]["count"], height = best_height, best_width = best_width, url = best_url, timestamp= timestamp ))

        # pprint(final_list)

        print()
        print('----Создание временной директории----')
        print('----Директория Temp создана----')
        print('----Выполняется загрузка файлов----')
        if os.path.exists('temp') != True:
            os.mkdir('temp')

        os.chdir('temp')
        for items in final_list:
            path = (f'{items["likes"]}.jpg')

            if os.path.exists(path):
                print(f'файл с именем {path} существует, генерация нового имени {items["likes"]}_{items["timestamp"]}.jpg')
                path = (f'{items["likes"]}_{items["timestamp"]}.jpg')
            else:
                print(path)
            items['path'] = path
            with open(path, 'wb') as f:
                image = requests.get(items['url'])
                f.write(image.content)

        print()
        print('----Создание локального JSON словаря----')
        print('----Словарь создан----')

        with open("temp.json", 'w', encoding='utf-8') as f:
            final_json = json.dumps(final_list)
            f.write(final_json)

        print()
        print()
        token_yd = input('Введите OAuth токен: ')
        print()
        print('----начинаю выгрузку на Yandex диск----')
        print()




        url_path = 'Vk_Archive'

        response_put = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                    headers={'Authorization': token_yd}, params={'path': url_path})

        with alive_bar(len(final_list)) as bar:
            for items in final_list:

                final_urlpath = (f'{url_path}_{items}["path"]')
                final_urlpath = items["path"]

                response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                        headers={'Authorization': token_yd}, params={'path': final_urlpath})
                # print(response.status_code)
                # pprint(response.json())
                upload_url = response.json()['href']

                with open(items['path'], 'rb') as f:
                    resp = requests.put(upload_url, files={'file': f})
                print()
                bar()
                time.sleep(1)

        print('загружено')







def intro():
    print(" ______   _                                                  _      _               ")
    print("(_____ \ | |            _                /\                 | |    (_)              ")
    print(" _____) )| | _    ___  | |_    ___      /  \    ____   ____ | | _   _  _   _   ____ ")
    print("|  ____/ | || \  / _ \ |  _)  / _ \    / /\ \  / ___) / ___)| || \ | || | | | / _  )")
    print("| |      | | | || |_| || |__ | |_| |  | |__| || |    ( (___ | | | || | \ V / ( (/ / ")
    print("|_|      |_| |_| \___/  \___) \___/   |______||_|     \____)|_| |_||_|  \_/   \____)")
    print()
    print("      v. 1.1                                                    by Alex Mikhailishin")
    print()
    print("_________________________________Список комманд_____________________________________")



def token_config():
    while True:
        while True:
            global NAME
            print()
            NAME = input('Ввведите ваше имя (латиница): ')
            print()
            if NAME != '':
                break
        TOKEN = input('Ввведите ваше токен: ')
        if TOKEN != '':
            break
    global user
    user = User(TOKEN)




def commands():
    print()
    print(f"Добро пожаловать, {NAME}!")
    print()
    print("--1-- выгрузить последние аватары вк")
    # print("--2-- Скачать фото из выбранного альбома")
    # print("--3-- Скачать фото из выбранного альбома")
    print("--q-- выход")


def interface():
    while True:
        command_list = ["q", "1"]

        print()
        command = input("Введите команду: ")

        if command == "1":
            user.download_vk()

        elif command == "q":
            print()
            print("До свидания!")
            break
        elif command not in command_list:
            print()
            print("Комманды не существует")






def main():



    intro()
    token_config()
    commands()
    interface()






main()




















