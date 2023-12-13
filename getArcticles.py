import requests, time, random, os, logging
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#url = 'https://www.spiegel.de/nachrichtenarchiv/artikel-01.01.2023.html'
url = 'https://www.spiegel.de/nachrichtenarchiv/artikel-01.01.2023.html'
sub_dir = 'spiegel_artikel'
abs_path = os.path.join(os.getcwd(),sub_dir)

timeout_duration = 500

# identifier for /schlagzeilen
#div_headline_identifier = {"data-area":"article_teaser>news-s-wide"}

# identifier for archive
# only one article: div_headline_identifier = {"data-block-el":"articleTeaser"}
section_headline_identifier = {"data-area":"article-teaser-list"}

response = requests.get(url).content
soup = BeautifulSoup(response,'html.parser')
headlines = soup.find('section',attrs=section_headline_identifier)

for a in headlines.find_all('a'):
			# get link and title
            link = a['href']
            file_path = os.path.join(abs_path,link.replace('/','.')[1:])
            full_link = urljoin(url, link)
            title = a['title']
            
            # get arcticle content
            article_content = requests.get(full_link, timeout=timeout_duration).content
            # Can use soup for text
            #soup1 = BeautifulSoup(article_content,'html.parser')
            #print(soup1.get_text())

            with open("test.html",'wb') as f:
                        f.write(article_content)
            break