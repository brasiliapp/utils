import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from unidecode import unidecode
import datetime


def print_timestamped_message(message):
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"[{timestamp}] {message}")


def get_active_deputados(deputados_url):
    response = requests.get(deputados_url)
    if response.status_code != 200:
        print_timestamped_message("Error fetching deputados. Exiting...")
        return []
    deputados_data = response.json()
    return [deputado for deputado in deputados_data['dados'] if deputado.get('email')]


def fetch_expenses_data(url_presence):
    response_deputado = requests.get(url_presence)
    if response_deputado.status_code != 200:
        print_timestamped_message(
            f"Error fetching data from {url_presence}. Exiting...")
        return None
    return BeautifulSoup(response_deputado.text, 'html.parser')


def extract_table_data(soup):
    table = soup.select_one("#main-content > section > div > table")
    if not table:
        print_timestamped_message(
            "Error finding the expected table. Exiting...")
        return []

    rows = table.find_all('tr')[1:]
    results = []
    for row in rows:
        columns = row.find_all('td')
        results.append({
            'month': columns[0].text.strip(),
            'available_amount': columns[1].text.strip(),
            'expense_amount': columns[2].text.strip()
        })
    return results


def fetch_and_extract_secretaries_data(new_link):
    response_new_link = requests.get(new_link)
    if response_new_link.status_code != 200:
        print_timestamped_message(
            f"Error fetching data from {new_link}. Exiting...")
        return {}, {}

    soup_new_link = BeautifulSoup(response_new_link.text, 'html.parser')

    # Active secretaries
    table_active = soup_new_link.select_one(
        "#main-content > section > div > table:nth-child(2)")
    active_secretaries = extract_secretaries_from_table(table_active)

    # Inactive secretaries
    table_inactive = soup_new_link.select_one(
        "#main-content > section > div > table:nth-child(4)")
    inactive_secretaries = extract_secretaries_from_table(table_inactive)

    return active_secretaries, inactive_secretaries


def extract_secretaries_from_table(table):
    if not table:
        print_timestamped_message(
            "Error finding the expected table. Exiting...")
        return []

    rows = table.find_all('tr')[1:]
    secretaries = []
    for row in rows:
        columns = row.find_all('td')
        secretaries.append({
            'name': columns[0].text.strip(),
            'group': columns[1].text.strip(),
            'role': columns[2].text.strip(),
            'period': columns[3].text.strip()
        })
    return secretaries


# For testing
if not os.path.exists('gabinete'):
    os.makedirs('gabinete')

idLegislatura = 57
deputados_url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}&itens=1000&ordem=ASC&ordenarPor=nome"

print_timestamped_message("Fetching active deputados...")
active_deputados = get_active_deputados(deputados_url)

# For testing
skipDeputados = 150

# Note: I'm keeping your limit of 1 for testing purposes
for deputado in active_deputados[skipDeputados:]:
    print_timestamped_message(
        f"Processing data for deputado: {deputado['nome']}...")
    nome_deputado = unidecode(deputado['nome'])
    nome_deputado_url = quote(nome_deputado, safe='')
    url_presence = f"https://www.camara.leg.br/deputados/{deputado['id']}/verba-gabinete?ano=2023"

    print_timestamped_message("Fetching expenses data...")
    soup = fetch_expenses_data(url_presence)

    print_timestamped_message("Extracting table data...")
    results = extract_table_data(soup)

    print_timestamped_message("Fetching secretaries data...")
    new_link_element = soup.select_one(
        "#main-content > section > div > p:nth-child(3) > a")
    if new_link_element:
        new_link = new_link_element.get('href')
        active_secretaries, inactive_secretaries = fetch_and_extract_secretaries_data(
            new_link)
    else:
        active_secretaries, inactive_secretaries = None, None

    result = {
        'deputado': deputado['nome'],
        "salary": 'R$ 41.650,92',
        'id': deputado['id'],
        'montly_expenses': results,
        'active_secretaries': active_secretaries if active_secretaries is not None else None,
        'inactive_secretaries': inactive_secretaries if inactive_secretaries is not None else None,
        'built_by': 'BrasiliApp - https://brasiliapp.com.br',
        'last_update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # For testing
    json_filename = f'gabinete/{nome_deputado.replace(" ", "-").lower()}-{deputado["id"]}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print_timestamped_message(f"Data for deputado {deputado['nome']} saved!")

print_timestamped_message("All tasks completed.")
