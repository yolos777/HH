# coding=utf-8
import csv

import requests
import json
import time
import os

# задаем функцию, где пропишем основные параметры для парсинга
# def get_info(page = 0):
#     params = {
#         'text': 'NAME:Швея',  # Задаем фильтр по вакансии, в нашем случае "швея"
#         'area': 1,  # так как область поиска Москва, ставим 1
#         'page': page,  # Номер страницы поиска
#         'per_page': 100  # Задаем количество вакансий на странице, по умолчанию 100
#     }
#     req = requests.get(url = 'https://api.hh.ru/vacancies', params = params)  # Отправляем GET-запрос к API HH.ru
#     src = req.content.decode()  # Декодируем, чтобы кириллица не превратилась в кашу нечитаемых символов
#     req.close() # Закрываем
#     return src
#
#
# # Задаем поиск по первым 20 страницам, навскидку этого должно хватить для большинства вакансий
# for page in range(0, 20):
#
#     jsObj = json.loads(get_info(page)) # Преобразуем текст ответа запроса в справочник Python
#     data = './{}.json'.format(len(os.listdir('./'))) # обязательно сохраняем ответ в файл json
#
#     # Создаем новый документ, записываем в него ответ запроса, после закрываем
#     f = open(data, mode='w', encoding='utf8')
#     f.write(json.dumps(jsObj, indent = 4, ensure_ascii=False))
#     f.close()
#
#     if (jsObj['pages'] - page) <= 1: # выполняем проверку на налицие страницы с вакансией
#         break
#
#     time.sleep(0.25) # ставим небольшую задержку, чтобы не перегружать сервер
#
# print('Готово!')

# Теперь у нас есть файлы в json формате с подробной информацией по всем вакансиям в интересующей нас категории

# Cоздадим новый файл csv, в котором зададим основные столбцы данных
with open('file.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            'наименование',
            'зарплата',
            'опыт',
            'требуемые навыки',
            'ссылка'
        )
    )
vac_data = [] # создадим список, куда будем добавлять интересующие нас данные
# пробежимся по всем файлам циклом for и вытащим только интересующую нас информацию
for i in os.listdir('./'):

    # Открываем файл, читаем его содержимое, закрываем файл
    f = open('./{}'.format(i), encoding='utf8')
    jsonText = f.read()
    f.close()

    # Преобразуем полученный текст в объект справочника
    try:
        jsonObj = json.loads(jsonText.encode("UTF-8")) # тут пришлось использовать try-except, потому что возникла проблема с кодировкой и я не смог найти более изящного решения
    except:
        print("no json returned")
    count = 1 # каунтер для отображения прогресса итерации

    # Теперь пробежимся по основному файлу с вакансиями, чтобы собрать только нужную инфу из API
    for v in jsonObj['items']:
        vac_name = v['name'] # наименование вакансии
        try: # во избедание ошибок при столкновении с вакансиями, где не указана зарплата воспользуемся контрукцией try - except
            vac_salary = {'from': v['salary']['from'], 'to': v['salary']['to']}
        except:
            vac_salary = None
        vac_experience = v['experience']['name'] # требуемый опыт
        vac_requirements = v['snippet']['requirement'] # ключевые навыки
        vac_link = v['alternate_url'] # ссылка на саму вакансию на HH.ru

        # Передадим полученные данные в форме словаря в список vac_data
        vac_data.append({
            'наименование': vac_name,
            'зарплата': vac_salary,
            'опыт': vac_experience,
            'требуемые навыки': vac_requirements,
            'ссылка': vac_link
        })

        # Сразу же можно передать данные и в наш csv файл
        with open('file.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    vac_name,
                    vac_salary,
                    vac_experience,
                    vac_requirements,
                    vac_link
                )
            )

        time.sleep(0.25)
        print(f'{v["id"]} is done, {count}/{len(jsonObj["items"])}')
        count += 1
# По окончании всего цикла создаем файл json - тот самый итоговый, где будет храниться интересующая нас инфа
with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vac_data, file, indent=4, ensure_ascii=False)






