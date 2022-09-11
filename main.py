import sys
import requests
import time
import csv
from bs4 import BeautifulSoup

def main(argv):
    if(len(argv) == 1):
        print("Something went wrong...")
        return 0
    records = scraping(argv)
    with open('result.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['会社名', '業種', '本社', 'URL'])
        for record in records:
            writer.writerow(record)
    print('file record: ' + str(len(records) + 1))
    print('done!')
    return 0

def scraping(words):
    page_num = 1
    records = []
    while True: 
        url = get_url(words, page_num)
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('li', 'ts-h-search-cassette')
        if len(cards) == 0:
            break

        for i in range(len(cards)):
            records.append(create_record(cards[i]))
           
        page_num += 1
        time.sleep(1.0)
    return records

def get_url(fw, pn):
    request_url = 'https://job.rikunabi.com/2023/s/?fw='
    for i in range(1, len(fw)): 
        request_url += str(fw[i])
        if(fw[i] == fw[len(fw) - 1]):
            request_url += '&pn=' + str(pn)
        else:
            request_url += '+'
    return request_url

def create_record(card):
    atag = card.div.div.a
    job_url = 'https;//job.rikunabi.com' + atag.get('href')
    company_name = card.find('a', 'ts-h-search-cassetteTitleMain').text.strip()
    job_description = card.find_all(class_='ts-h-search-cassetteDefDesc')
    industry = job_description[0].text
    location = job_description[1].text 
    
    record = (company_name, industry, location, job_url)
    return record


if __name__ == '__main__':
    sys.exit(main(sys.argv))
