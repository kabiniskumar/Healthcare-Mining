import requests
import pickle
from bs4 import BeautifulSoup
import csv


threads = pickle.load(open("threads.p", "rb"))
hdr = {'User-Agent': 'Mozilla/5.0'}


with open('MayoClinic/mayo_full_bs.csv', mode='w', newline='', encoding="utf8") as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['condition', 'postLink', 'postHeading', 'postContent'])
    for each in threads:
        page = requests.get(each, headers=hdr)
        print(page)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            thread_body = soup.find('div', class_='thread-content').get_text().strip().replace('\n', ' ')
            thread_heading = soup.find('h2', class_='chv4-thread-title').get_text().strip()
            breadcrumbs = soup.find('ol', class_='ch-breadcrumb breadcrumb breadcrumbs-groups')
            condition = breadcrumbs.findAll('a')[2].text

        except Exception as e:
            continue
        writer.writerow([condition, each, thread_heading, thread_body])