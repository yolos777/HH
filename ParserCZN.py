# coding=utf-8
import csv
import re

from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests



# for i in range(10):
#     # Значение 10 в данном цикле взято исходя из количества страниц результата по поиску ваканций "швея"
#     # Первым шагом пройдемся по всем страницам и спарсим ссылки на все вакансии
#     url = f'https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=%D1%88%D0%B2%D0%B5%D1%8F&' \
#           f'excluded_text=&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&page={i}'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.2.806 Yowser/2.5 Safari/537.36'
#     }
#     vacancy_links_list = []
#     def get_data(url):
#         # в этой функции прописан алгоритм извлечения данных с помощью selenium
#         # в случае с HH.ru простой библиотеки requests было недостаточно, GET-запрос возвращал неполный объем информации
#         options = webdriver.ChromeOptions()
#         options.set_capability("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.2.806 Yowser/2.5 Safari/537.36")
#
#         try:
#             driver = webdriver.Chrome(
#                 executable_path='/Selenium/chromedriver.exe',
#                 options=options
#             )
#             driver.get(url = url)
#             time.sleep(5)
#
#             with open('Index_1.html', 'w', encoding='utf-8') as file:
#                 file.write(driver.page_source)
#
#         except Exception as ex:
#             print(ex)
#         finally:
#             driver.close()
#             driver.quit()
#
#         with open("Index_1.html", encoding='utf-8') as file:
#             src = file.read()
#
#
#         get_content_soup = BeautifulSoup(src, 'lxml')
#         soup_links = get_content_soup.find_all("a", class_ = 'serp-item__title')
#         for link in soup_links:
#             vacancy_link = link.get('href')
#             vacancy_links_list.append(vacancy_link)
#
#         with open('vacancy_links_list.txt', 'a', encoding='utf-8') as file:
#             for line in vacancy_links_list:
#                 file.write(f'{line}\n')
#
#         print(f'Страница {i} благодарно поделилась своими данными, данные были сохранены')
#
#     def main():
#         get_data(url)
#
#     if __name__ == '__main__':
#         main()

# теперь, когда у нас есть список ссылок на вакансии, пройдемся по нему и вытащим нужные данные
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.2.806 Yowser/2.5 Safari/537.36'
}
with open ('vacancy_links_list.txt') as file:
    url_lines = [url_line for url_line in file.readlines() if len(url_line) < 100]
    vacancy_content = []
    count = 0

    with open('data_2.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    'vacancy_title',
                    'vacancy_salary',
                    'vacancy_experience',
                    'skill_list'
                )
            )

    for url_line in url_lines:
        src = requests.get(url=url_line, headers=headers)
        src_cont = src.content

        q = BeautifulSoup(src_cont, 'lxml')
        try:
            vacancy_title = q.find('div', class_ = 'vacancy-title').find('h1').get_text()
        except:
            vacancy_title = None
        try:
            vacancy_salary = q.find('div', class_ = 'vacancy-title').find('span').text.replace("&nbsp;","").replace("\xa0","").split(' ')
            salary_ammount = vacancy_salary[1]
        except:
            vacancy_salary = None
        try:
            vacancy_experience = q.find(class_ = re.compile('vacancy-description')).find('span').get_text()
        except:
            vacancy_experience = None
        skill_list = []
        try:
            vacancy_skills = q.find(class_ = 'bloko-tag-list').find_all('span')
            for i in vacancy_skills:
                skill = i.text.replace("\xa0", "")
                skill_list.append(skill)
        except:
            vacancy_skills = None

        with open('data_2.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        vacancy_title,
                        salary_ammount,
                        vacancy_experience,
                        skill_list
                    )
                )
        count += 1
        print(f'#{count} link is done!')