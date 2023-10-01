import os
import requests
import json
from unidecode import unidecode
import datetime
from logger import log
from model.deputado import Deputado
from client.deputado import DeputadoClient

def get_active_deputados(deputados_url):
    response = requests.get(deputados_url)
    if response.status_code != 200:
        log("Error fetching deputados. Exiting...")
        return []
    deputados_data = response.json()
    return [deputado for deputado in deputados_data['dados'] if deputado.get('email')]

# For testing
if not os.path.exists('gabinete'):
    os.makedirs('gabinete')

idLegislatura = 57
deputados_url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}&itens=1000&ordem=ASC&ordenarPor=nome"

log("Fetching active deputados...")
active_deputados = get_active_deputados(deputados_url)

# For testing
skipDeputados = 150

client = DeputadoClient()

# Note: I'm keeping your limit of 1 for testing purposes
for deputado in active_deputados[skipDeputados:]:
    log(f"Processing data for deputado: {deputado['nome']}...")

    log("Fetching expenses data...")
    soup, results = client.fetch_expenses_data(deputado['id'])

    log("Fetching secretaries data...")
    active_secretaries, inactive_secretaries = client.fetch_secretaries_data(soup)

    log("Extracting salary data...")
    salary = client.fetch_monthly_salary(deputado['id'])

    deputado = Deputado(deputado['id'], unidecode(deputado['nome']), salary, results, active_secretaries, inactive_secretaries, datetime.datetime.now())

    result = deputado.to_json()

    # For testing
    json_filename = f'gabinete/{deputado.name.replace(" ", "-").lower()}-{deputado.id}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    log(f"Data for deputado {deputado.name} saved!")

log("All tasks completed.")
