#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re

def request():
    url = "https://status.ix.br"
    return requests.get(url)

def parse_result(html):
    bs = BeautifulSoup(html, 'html.parser')
    ixlist = bs.find_all('ul', {'class': 'list-group components'})

    data = {}
    print("[")
    for ix in ixlist:
            name = ix.find('strong').text.strip()
            items = ix.find('div', {'class': 'group-items'}).find_all('li', {'class': 'list-group-item'})
            ix_data = {}
            for item in items:
                status_div = item.find('div', {'class': 'pull-right'})
                status = status_div.text.strip()
                status_div.decompose()
                item_name = item.text.strip()
                if name == 'IX-br - Outras Localidades':
                    ix_grupo = re.sub('.*- ', '', name)
                    ix_nome = re.sub('IX.br ', '', item_name)
                    ix_localizacao = ix_nome
                else:
                    ix_grupo = re.sub('IX.br ', '', name)
                    ix_nome = re.sub(' -.*', '', item_name)
                    ix_localizacao = re.sub('.*- IX.br ', '', item_name)

                print("\t")
                print("\t{")
                print(f'\t\t"{"IX_GRUPO"}": "{ix_grupo}",')
                print(f'\t\t"{"IX_LOCALIZACAO"}": "{ix_localizacao}",')
                print(f'\t\t"{"IX_NOME"}": "{ix_nome}",')
                print(f'\t\t"{"IX_STATUS"}": "{status}"')
                print("\t},")
    return data

if __name__ == '__main__':
    response = request()

print(parse_result(response.text))

print("]")
