import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from datetime import datetime
import os
import gc
from constants import DEPUTY_DATA_ENDOINT, LEGISLATURE_ID, FINAL_DATE_DEPUTY_SPEECH_SEARCH, \
    DEPUTY_TO_SKIP_SPEECH_DATA, INITIAL_DATE_DEPUTY_SPEECH_SEARCH

# Function to print a timestamped message
def print_timestamped_message(message):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{formatted_time}] {message}")


# Check if the 'speechs' directory exists and create it if not
if not os.path.exists('speechs'):
    os.makedirs('speechs')


def extrair_mp4_url(url):
    print_timestamped_message(f"Buscando MP4 na URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find('source')
    if video_tag:
        src_attribute = video_tag.get('src')
        if src_attribute:
            print(src_attribute)
            return src_attribute
    print("não encontrou atributo")
    return None


def extrair_links_de_video(url, nome_deputado):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_params = []
    h4_tags = soup.find_all(
        "h4", class_="g-chamada__titulo g-chamada__titulo--simples")

    for h4_tag in h4_tags:
        if h4_tag.get_text(strip=True) == nome_deputado:
            a_tag = h4_tag.find_parent(
                'article', class_='g-chamada').find('a', id='link-trecho-video')
            if a_tag:
                video_params.append(a_tag['href'].split("?")[-1])

    return video_params


deputados_url = f"{DEPUTY_DATA_ENDOINT}?idLegislatura={LEGISLATURE_ID}&itens=1000&ordem=ASC&ordenarPor=nome"
response = requests.get(deputados_url)
deputados_data = response.json()
nomes_deputados = [deputado['nome'] for deputado in deputados_data['dados']]

# for testing
skipDeputados = DEPUTY_TO_SKIP_SPEECH_DATA

for deputado in deputados_data['dados'][skipDeputados:]:
    nome_deputado = deputado['nome']
    nome_deputado_url = quote(nome_deputado, safe='')

    url_deputado = \
        f"https://www2.camara.leg.br/atividade-legislativa/webcamara/arquivos/resultadoPeriodoDep?dep={nome_deputado_url}&dataInicio={INITIAL_DATE_DEPUTY_SPEECH_SEARCH}&dataFim={FINAL_DATE_DEPUTY_SPEECH_SEARCH}"
    response_deputado = requests.get(url_deputado)
    soup = BeautifulSoup(response_deputado.text, 'html.parser')

    resultados = []

    eventos_divs = soup.find_all(class_="itemListaTransmissoes")
    for evento_div in eventos_divs:
        evento = {
            "deputado": nome_deputado,
            "sessao": evento_div.find("a").text if evento_div.find("a") else "N/A",
            "date": evento_div.find(class_="timestamp").find_all("span")[1].text,
            "time": evento_div.find(class_="timestamp").find_all("span")[2].text,
            "place": evento_div.find(class_="timestamp").find_all("span")[0].text,
            "event_title": "",
            "event_url": "",
            "event_id": "",
            "video_links": []
        }

        link_a = evento_div.find("a")
        if link_a:
            evento["event_title"] = link_a.text.replace('\n', '')
            evento["event_url"] = link_a['href']
            evento_id = link_a['href'].split('/')[-2]
            evento["event_id"] = evento_id
            video_params = extrair_links_de_video(
                link_a['href'], nome_deputado)
            for video_param in video_params:
                base_url = 'https://www.camara.leg.br/evento-legislativo/'
                event_id = link_a['href'].split('/')[-2]
                video_url = f'{base_url}{event_id}/?{video_param}&trechosOrador={nome_deputado_url}&crawl=no'
                mp4_url = extrair_mp4_url(video_url)
                evento["video_links"].append(
                    {"video_param": video_param, "mp4_url": mp4_url})

        resultados.append(evento)
# for testing
    json_filename = f'speechs/{nome_deputado.replace(" ", "-").lower()}-{deputado["id"]}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
        gc.collect()
