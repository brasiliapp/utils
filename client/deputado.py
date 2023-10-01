import datetime
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from logger import log

def extract_secretaries_from_table(table):
    if not table:
        log(
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

def fetch_and_extract_secretaries_data(new_link):
    response_new_link = requests.get(new_link)
    if response_new_link.status_code != 200:
        log(
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

class DeputadoClient:
    def __init__(self):
        self.base_url = "https://www.camara.leg.br/deputados"
        self.current_year = datetime.datetime.now().date().strftime("%Y")

    def fetch_expenses_data(self, deputado_id):
        url_presence = f"{self.base_url}/{deputado_id}/verba-gabinete?ano={self.current_year}"

        response_deputado = requests.get(url_presence)

        if response_deputado.status_code != 200:
            log(f"Error fetching data from {url_presence}. Exiting...")
            return None, None

        soup = BeautifulSoup(response_deputado.text, 'html.parser')

        log("Extracting table data...")

        table = soup.select_one("#main-content > section > div > table")

        if not table:
            log("Error finding the expected table. Exiting...")
            return soup, None

        rows = table.find_all('tr')[1:]
        results = []
        for row in rows:
            columns = row.find_all('td')
            results.append({
                'month': columns[0].text.strip(),
                'available_amount': columns[1].text.strip(),
                'expense_amount': columns[2].text.strip()
            })
        return soup, results

    def fetch_monthly_salary(self, deputado_id):
        salary_url = f"{self.base_url}/{deputado_id}/remuneracao?ano={self.current_year}"

        response_salary = requests.get(salary_url)

        if response_salary.status_code != 200:
            log(f"Error fetching {self.current_year} salary for deputado with ID {deputado_id}")
            return None

        soup = BeautifulSoup(response_salary.text, 'html.parser')

        monthly_salaries = soup.find_all('tr')

        if len(monthly_salaries) > 0:
            try:
                latest_monthly_salary = Decimal(monthly_salaries[-1].find('a').text.strip().replace(".", "").replace(",", "."))

                return f"R$ {latest_monthly_salary:,.2f}".replace(".","%").replace(",",".").replace("%",",")
            except:
                log(f"Error reading {self.current_year} monthly salary for deputado with ID {deputado_id}")
                return None
        else:
            log(f"Error parsing {self.current_year} monthly salary for deputado with ID {deputado_id}")
            return None

    def fetch_secretaries_data(self, soup):
        new_link_element = soup.select_one("#main-content > section > div > p:nth-child(3) > a")

        active_secretaries, inactive_secretaries = None, None

        if new_link_element:
            new_link = new_link_element.get('href')
            active_secretaries, inactive_secretaries = fetch_and_extract_secretaries_data(new_link)

        return active_secretaries, inactive_secretaries
