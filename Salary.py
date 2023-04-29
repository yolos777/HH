# coding=utf-8
import csv
import re
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


plt.style.use('classic')
fig = plt.figure(figsize = (7, 4))
fig.suptitle('Зависимость уровня заработной платы от требуемого опыта')

x = np.random.randint(1, 4, 30)
y = np.random.randint(45, 125, 30)
x2 = np.random.randint(4, 7, 30)
y2 = np.random.randint(50, 155, 30)
x3 = np.random.randint(6, 9, 30)
y3 = np.random.randint(60, 125, 30)

ax = fig.add_subplot(1, 3, 1)
# первый график построен на основании зарплатного диапазона, разделенного на три временные категории:
# 1-3 лет: от 45 до 125 тыс.руб., 3-6 лет: от 50 до 155 тыс.руб., более 6 лет: от 60 до 125 тыс.руб.
ax.grid(True)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(5))
plt.xlim(0, 10)
plt.ylim(30, 160)
plt.xlabel('опыт, лет', c = 'g')
plt.ylabel('з/п, тыс.руб.', c = 'g')
ax.scatter(x, y, s = 50)
ax.scatter(x2, y2, s = 50, c = 'g')
ax.scatter(x3, y3, s = 50, c = 'm')


x21 = np.random.normal(0, 0.3, 100)
y21 = np.random.normal(87.5, 15, 100)
x22 = np.random.normal(2, 0.5, 100)
y22 = np.random.normal(85, 15, 100)
x23 = np.random.normal(4, 0.5, 100)
y23 = np.random.normal(102.5, 15, 100)
x24 = np.random.normal(7, 0.5, 100)
y24 = np.random.normal(95, 15, 100)

ax2 = fig.add_subplot(1, 3, 2)
# второй график - это мой поиск более правильного отображения значений, однако здесь учитываются приблизительные величины
# в качетсве центральных точек, вокруг которых располагаются значения были выбраны средние показатели зарплат
ax2.grid()
ax2.xaxis.set_major_locator(MultipleLocator(1))
ax2.yaxis.set_major_locator(MultipleLocator(5))
plt.xlim(0, 10)
plt.ylim(30, 160)
plt.xlabel('опыт, лет', c = 'g')
plt.ylabel('з/п, тыс.руб.', c = 'g')
ax2.scatter(x21, y21, s = 50)
ax2.scatter(x22, y22, s = 50, c = 'g')
ax2.scatter(x23, y23, s = 50, c = 'r')
ax2.scatter(x24, y24, s = 50, c = 'm')

ax3 = fig.add_subplot(1, 3, 3)
# третий график - прямая, проходящая по средним значениям зарплат "от" и "до"
ax3.grid()
ax3.xaxis.set_major_locator(MultipleLocator(1))
ax3.yaxis.set_major_locator(MultipleLocator(5))
plt.xlim(0, 10)
plt.ylim(30, 160)
plt.xlabel('опыт, лет', c = 'g')
plt.ylabel('з/п, тыс.руб.', c = 'g')
x31 = [0, 1, 6, 8]
y31 = [59.77, 63.29, 69.09, 73.8]
y32 = [102.91, 93.16, 120.37, 107.77]
ax3.plot(x31, y31)
ax3.plot(x31, y32, c = 'g')

plt.show()