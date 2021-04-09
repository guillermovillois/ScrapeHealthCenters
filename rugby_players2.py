import random
from google_sheets import get_tour_table, get_lista_players, adjust_tables
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
# import openpyxl
import xlsxwriter
from match import matches
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import random
# from send_email import send_email
from upload import convert_excel_file
import requests
from bs4 import BeautifulSoup

begin_time = datetime.now()


hoy = datetime.utcnow().date().strftime("%d_%m_%Y")

# jugadores1 = pd.read_excel('lista_found_fr.xlsx', engine='openpyxl')[:1]

torneo_int = get_tour_table(
    '10rOPYqyi9tpDP76EhE-nDO0VUpZCH59KQcjP0piJJ0g', 'INTL!A1:A')
torneo_local = get_tour_table(
    '10rOPYqyi9tpDP76EhE-nDO0VUpZCH59KQcjP0piJJ0g', 'Teams!A1:A')

# listas = pd.read_excel(
#     'TeamLists_2.xlsx', sheet_name='Pro 14', engine='openpyxl')
table = get_lista_players(
    '1t8OZKHw2FldCqAW5kRShYEI8NhbGd2KiLbsnU0BnBsw', "Sheet1!A1:C")
listas = adjust_tables('1RO5xvuu6HwURWaFAMS_a5KpZMJpAgaB1iCxNWJ4wLKI')
print(listas)
jugadores = matches(table, listas)
print(jugadores)
tours = sorted(list(set(jugadores['Tournament'].tolist())))[1::3]
print(tours)
# jugadores = pd.read_excel('nada.xlsx', engine='openpyxl')[:2]
jugadores = jugadores.sample(frac=1).reset_index(drop=True)


def jugarretas(lista_torneos):
    jugadas = 0
    torneos = driver.find_elements_by_tag_name(
        'tbody')[-1].find_elements_by_tag_name('tr')
    for cada in torneos:
        cols = cada.find_elements_by_tag_name('td')
        if cols[0].text == '' and cols[1].text in lista_torneos:
            jugadas += float(cols[5].text if cols[5].text != '-' else 0)
    return jugadas


def jugarretasSoup(soup, lista_torneos):
    torneos = soup.findAll('tbody')[-1].findAll('tr')
    jugadas = 0
    for torneo in torneos:
        cols = torneo.findAll('td')
        if cols[0].text == '' and cols[1].text in lista_torneos:
            jugadas += float(cols[5].text if cols[5].text != '-' else 0)
    return jugadas


def get_players(site):
    lista = []
    for i in site.find('div', {'id': 'slides'}).findAll('tr'):
        player = []
        for j, each in enumerate(i):
            if j > 0:
                player.append(each.text.replace('(', '').replace(')', ''))
                if j == 1:
                    player.append('http://www.itsrugby.co.uk/' +
                                  each.find('a', {'id': 'noir'})['href'])
        lista.append(player)
    return lista


user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
               'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)']


# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("user-agent=" + random.choice(user_agents))
# chrome_options.add_argument("--ignore-certificate-error")
# chrome_options.add_argument("--ignore-ssl-errors")
# chrome_options.add_argument("--log-level=3")  # fatal
# driver = webdriver.Chrome(
#     ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=chrome_options
# )

# driver.delete_all_cookies()


def get_players(jugadores, tour):
    # print(jugadores)
    players = []
    j = 0
    for index, each in jugadores.iterrows():
        if each['URL'] == 'NOT FOUND':
            print(each['ListaNames'], each['URL'], 'NOT FOUND')
            player["ListTeam"] = each['ListaTeams']
            player["ListName"] = each['ListaNames']
            player["PLAYER"] = each['PLAYER']
            player["AGE"] = ''
            player["COUNTRY"] = ''
            player["TEAM"] = ''
            player["URL"] = ''
            player["APP"] = ""
            player["CAPS"] = ''
            player["HONOUR"] = 'NOT FOUND'
            player["POSITION"] = ''
        else:

            player = {}
            jugador = each['URL']
            player["ListTeam"] = each['ListaTeams']
            player["ListName"] = each['ListaNames']
            player["URL"] = str(each['URL'])
            driver.implicitly_wait(random.uniform(5.45, 12.5))
            driver.get(jugador)
            WebDriverWait(
                driver, random.uniform(10.45, 20.5)
            )  # .until(cond.alert_is_present())

            print(each['PLAYER'], each['URL'])
            try:
                player["PLAYER"] = driver.find_element_by_tag_name(
                    "h1").text.upper()
                try:
                    player["AGE"] = int(
                        driver.find_element_by_class_name("table")
                        .find_elements_by_tag_name("tr")[0]
                        .find_elements_by_id("noir")[0]
                        .text.split(" ")[0]
                    )
                except:
                    player['AGE'] = ''
                player["COUNTRY"] = (
                    driver.find_element_by_class_name("table")
                    .find_elements_by_tag_name("tr")[1]
                    .find_elements_by_id("noir")[0]
                    .text.strip()
                ).upper()
                try:
                    player["TEAM"] = driver.find_element_by_tag_name(
                        'h2').text.replace('(', '').replace(')', '').strip().upper()
                except:
                    player['TEAM'] = ''
                player["URL"] = each['URL']
                try:
                    player["POSITION"] = int(
                        driver.find_element_by_class_name("table")
                        .find_elements_by_tag_name("tr")[0]
                        .find_elements_by_id("noir")[1]
                        .text.split(" ")[0]
                    )
                except:
                    player["POSITION"] = ''
                try:
                    player["APP"] = jugarretas(torneo_local)
                except:
                    player["APP"] = ""
                try:
                    international = driver.find_element_by_xpath(
                        "//a[contains(text(), 'nternational')]"
                    ).get_attribute("href")
                except:
                    international = ""
                if international != "":
                    driver.implicitly_wait(random.uniform(5, 10))
                    driver.get(international)
                    WebDriverWait(
                        driver, random.uniform(15.45, 30.5)
                    )  # .until(cond.alert_is_present())

                    try:
                        player["CAPS"] = jugarretas(torneo_int)
                    except:
                        player['CAPS'] = 0
                else:
                    player["CAPS"] = 0
                player["HONOUR"] = (
                    'TEAM PLAYER'
                    if player["CAPS"] == 0
                    else (player["COUNTRY"] + " INTERNATIONAL")
                )
            except:
                try:
                    req = requests.get(each['URL'])
                    print(req)
                    soup = BeautifulSoup(req.text, 'html.parser')
                    player["PLAYER"] = soup.find('h1').text.upper()
                    try:
                        player["AGE"] = soup.find('table').find('tr').find(
                            'td', {'id': 'noir'}).text.split('\xa0')[0]
                    except:
                        print('age')
                        player["AGE"] = ''
                    player["COUNTRY"] = soup.find('table').findAll(
                        'tr')[1].find('td', {'id': 'noir'}).text.strip().upper()
                    try:
                        player["TEAM"] = soup.find('h2').text.replace(
                            '(', '').replace(')', '').strip().upper()
                    except:
                        print('team')
                        player["TEAM"] = ''
                    try:
                        player["POSITION"] = soup.find('table').find('tr').findAll(
                            'td', {'id': 'noir'})[1].text.split(' ')[0].replace('\n')
                    except:
                        player["POSITION"] = ''

                    try:
                        player["APP"] = jugarretasSoup(soup, torneo_local)
                    except:
                        print('app')
                        player["APP"] = ""
                    try:
                        stsplit = each['URL'].split('/play')
                        print(stsplit[0] + '/player-international-' +
                              stsplit[1].split('-')[-1])
                        req = requests.get(
                            stsplit[0] + '/player-international-'+stsplit[1].split('-')[-1])
                        soup = BeautifulSoup(req.text, 'html.parser')
                        player["CAPS"] = jugarretasSoup(soup, torneo_int)
                    except:
                        player['CAPS'] = 0

                    player["HONOUR"] = (
                        'TEAM PLAYER'
                        if player["CAPS"] == 0
                        else (player["COUNTRY"] + " INTERNATIONAL")
                    )
                except:
                    player["ListName"] = each['ListaNames']
                    player["ListTeam"] = each['ListaTeams']
                    player["PLAYER"] = each['PLAYER']
                    player["HONOUR"] = "NO RESPONSE"
                    player["AGE"] = ''
                    player["TEAM"] = ''
                    player["APP"] = ""
                    player["CAPS"] = ''
                    player["POSITION"] = ''
        players.append(player)
        if j == 50:
            j = 0
            driver.implicitly_wait(random.uniform(20, 50))
            driver.delete_all_cookies()
        j += 1

    df = pd.DataFrame(players, columns=['ListTeam', "ListName", "TEAM", "POSITION", "PLAYER", "CAPS", "APP", "AGE", "HONOUR",
                                        "COUNTRY", "URL"]).sort_values(["ListTeam", "ListName"]).drop_duplicates()
    # .to_excel(tour + '_' + "RugbyPlayers_" + hoy + ".xlsx", index=False)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(tour + '_' + "RugbyPlayers_" +
                            hoy + ".xlsx", engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Data', index=False)

    # Get the xlsxwriter objects from the dataframe writer object.
    workbook = writer.book
    worksheet = writer.sheets['Data']
    worksheet.freeze_panes(1, 0)
    worksheet.set_column('A:E', 15, None)
    worksheet.set_column('I:K', 15, None)
    (max_row, max_col) = df.shape
    worksheet.autofilter(0, 0, max_row, max_col - 1)
    writer.save()
    convert_excel_file(tour + '_' + "RugbyPlayers_" + hoy + ".xlsx", [
        '1qfOJuWE0yneOmgip1PU2w5onV6RIVBsL'])
    # send_email(tour + '_' + "RugbyPlayers_" + hoy + ".xlsx")
    driver.implicitly_wait(random.uniform(250, 550))


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--log-level=3")  # fatal
chrome_options.add_argument(
    "user-agent=" + random.choice(user_agents))
driver = webdriver.Chrome(
    ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=chrome_options
)


for tour in tours:
    print(tour)
    if tour != '':
        get_players(jugadores[jugadores.Tournament == tour][[
                    'ListaTeams', 'ListaNames', 'PLAYER', 'URL']], tour.replace(' ', ''))

driver.close()
print(datetime.now() - begin_time)
