import time
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from send_email import send_email
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

with open("cosas.json") as f:
    data = json.load(f)
driver.get(data['url'])
urls = driver.find_element_by_tag_name(
    'ol').find_elements_by_class_name('cid-24')

links = []
for url in urls:
    links.append(url.find_element_by_tag_name('a').get_attribute('href'))

centros = []

for link in links:
    datos = {}
    driver.get(link)
    time.sleep(3)

    elementos = []
    for j, item in enumerate(driver.find_element_by_id('accordion').find_elements_by_class_name('panel.panel-default')):
        if item.text.split('\n')[-1] == "Datos del Prestador":
            elementos.append(j)
        elif item.text.split('\n')[-1] == "Representante Legal":
            elementos.append(j)
    items = driver.find_element_by_id(
        'accordion').find_elements_by_class_name('panel.panel-default')
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

    for j, line in enumerate(items[elementos[1]].find_elements_by_tag_name('tr')):
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

        datos[nombre1] = nombre2

    centros.append(datos)


driver.close()
pd.DataFrame(centros).to_excel('data.xlsx', index=False)
send_email('data.xlsx')
