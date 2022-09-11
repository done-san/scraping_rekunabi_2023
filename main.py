import csv
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

def get_url(fw, pn):
    template = 'https://job.rikunabi.com/2023/s/?fw={}&pn={}'
    url = template.format(fw, pn)
    return url

page_num = 1
while True:

    url = get_url('インフラエンジニア', page_num)

    response = requests.get(url)
    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('li', 'ts-h-search-cassette')
    print(len(cards))
    if len(cards) == 0:
        print('done!')
        break

    for i in range(len(cards)):
        card = cards[i]
        atag = card.div.div.a
        job_title = atag.get('title')
        job_url = 'https;//job.rikunabi.com' + atag.get('href')
        company_name = card.find('a', 'ts-h-search-cassetteTitleMain').text.strip()
        job_description = card.find_all(class_='ts-h-search-cassetteDefDesc')
        industry = job_description[0].text
        location = job_description[1].text

        print(job_url)
        print(company_name)
        print(industry)
        print(location)
        print()

    page_num += 1
    time.sleep(1.0)

