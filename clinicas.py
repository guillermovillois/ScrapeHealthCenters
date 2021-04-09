from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from send_email import send_email
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.refresh()

driver.get(
    'https://www.supersalud.gob.cl/acreditacion/673/w3-propertyvalue-4710.html')

urls = driver.find_element_by_tag_name(
    'ol').find_elements_by_class_name('cid-24')

links = []
for url in urls:
    if url.text != 'Inscripción cancelada':
        links.append(url.find_element_by_tag_name('a').get_attribute('href'))

centros = []
i = 0
h = 1
for link in links:
    datos = {}
    driver.get(link)
    time.sleep(3)
    print(h, driver.find_element_by_class_name('titulo').text)
    #datos['centro'] = driver.find_element_by_class_name('titulo').text
    elementos = []
    for j, item in enumerate(driver.find_element_by_id('accordion').find_elements_by_class_name('panel.panel-default')):
        if item.text.split('\n')[-1] == "Datos del Prestador":
            elementos.append(j)
        elif item.text.split('\n')[-1] == "Representante Legal":
            elementos.append(j)
        # print(item.text.split('\n')[-1])
    items = driver.find_element_by_id(
        'accordion').find_elements_by_class_name('panel.panel-default')
    # print(items, elementos)
    # print(items[elementos[0]].get_attribute('innerHTML'))
    items[elementos[0]].find_element_by_tag_name('a').click()

    for line in items[elementos[0]].find_elements_by_tag_name('tr'):
        datos[line.find_element_by_tag_name(
            'th').text] = line.find_element_by_tag_name('td').text

    datos['URL'] = link

    driver.get(link)
    time.sleep(3)

    items = driver.find_element_by_id(
        'accordion').find_elements_by_class_name('panel.panel-default')
    items[elementos[1]].find_element_by_tag_name('a').click()

    #representante = {}

    for j, line in enumerate(items[elementos[1]].find_elements_by_tag_name('tr')):
        #print(i, line.text)
        try:
            nombre1 = 'Repr_Leg_' + line.find_element_by_tag_name(
                'th').text
        except:
            print(j, "no", line.get_attribute('innerHTML'))
        try:
            nombre2 = line.find_element_by_tag_name(
                'td').find_element_by_tag_name('a').text
        except:
            try:
                nombre2 = line.find_element_by_tag_name(
                    'td').text
            except:
                nombre2 = "NoMail"
        #print(nombre1, nombre2)
        #print(nombre1, nombre2)
        datos[nombre1] = nombre2

        # print(datos)
    # time.sleep(5)
    # print(datos)
    centros.append(datos)
    if i == 100:
        file = pd.DataFrame(centros).to_excel('test.xlsx', index=False)
        send_email('test.xlsx')
        i = 0
    # time.sleep(10)
    i += 1
    h += 1


file = pd.DataFrame(centros).to_excel('test.xlsx', index=False)
send_email('test.xlsx')
driver.close()
