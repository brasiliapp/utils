# Brasiliapp/Utils: Web Scraping para Dados dos Deputados Federais

Este repositório contém utilitários e funções de web scraping para coletar dados relacionados aos deputados federais na Câmara dos Deputados do Brasil. Essas ferramentas podem ser usadas para extrair as mais diversas informações que não estão disponíveis na api da câmara, ou que não estão estruturada de uma forma organizada.

As informações não disponíveis na API da câmara são estraídas do site oficial do Câmara dos Deputados (https://www.camara.leg.br/)

Se você tiver de alguma outra informação que esteja disponível lá, abra uma issue.

## Funcionalidades

[extract_gabinet_data.py](./extract_gabinet_data.py)
- [x] Coleta dos gastos mensais da verba de cabineta de um/a parlamentar.
- [x] Coleta dos secretários ativos do gabinete de um/a parlamentar.
- [x] Coleta dos secretários inativos do gabinete de um/a parlamentar.
- [ ] Coletar o salário de cada secretário.

[extract_speeches.py](./extract_speeches.py)
- [x] Coleta eventos e gravações de fala do parlamentar.
- [ ] Armazenar em núvem os arquivos para não depender da disponibilidade da cloud da câmara.

## Modo de Uso

### Pré-requisitos

Certifique-se de ter as seguintes dependências instaladas:

- Python 3

### Executando o Web Scraper

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/utils.git

2. Navegue até o diretório do repositório:
   ```bash
   cd utils

3. Instale as dependências rodando o seguinte comando dentro do repositório:
   ```bash
   pip3 install -r requirements.txt

4. Execute o script
   ```bash
   python3 extract_gabinet_data.py

## Como Contribuir

Gostaríamos muito da sua ajuda para melhorar este projeto. Se você deseja contribuir, siga estas etapas:

1. Faça um fork deste repositório.
2. Clone o fork em sua máquina local.
3. Crie uma nova branch: `git checkout -b minha-contribuicao`
4. Faça suas alterações e commit: `git commit -m "Adicionei novos recursos"`
5. Envie suas alterações para o GitHub: `git push origin minha-contribuicao`
6. Abra um pull request para revisão.

## Comunidade

Participe da nossa [comunidade no discord](https://discord.gg/Udb7ZTac9F) para discussões, feedback e suporte:




