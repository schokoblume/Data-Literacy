import requests, time, random, os, logging
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

# Run this script to download spiegel articles from 2000 until now

# if folder does not exist, create it
folder_name = os.getcwd() + '/spiegel_articles'
Path(folder_name).mkdir(exist_ok=True)

# identifier for archive headlines
# only one article
# div_headline_identifier = {"data-block-el":"articleTeaser"}
# all articles
# section_headline_identifier = {"data-area":"article-teaser-list"}
section_headline_identifier = {"data-area":"article-teaser-list"}

errors = 0
sleeptimes = list(range(1,5,1))

# iterate over all dates from 01.01.2000 until recently
# we use a fixed date rather than today for a fixed data set
start_date = datetime.date(2000, 1, 1)
end_date = datetime.date(2023, 12, 22)
print("Starting download...")
while (start_date <= end_date):
    # format according to spiegel link
    date = start_date.strftime('%d') + "." + start_date.strftime('%m') + "." + start_date.strftime('%Y')
    url = 'https://www.spiegel.de/nachrichtenarchiv/artikel-' + date + '.html'
    # create folders per year and per month, in case we want to check specific dates later (easier to find)
    folder_year = folder_name + '/' + start_date.strftime('%Y')
    Path(folder_year).mkdir(exist_ok=True)
    folder_month = folder_year + '/' + start_date.strftime('%m')
    Path(folder_month).mkdir(exist_ok=True)
    file_name = folder_month + '/' + date + '.txt'

    # increase start_date by one day for next interation, use date from here
    start_date += datetime.timedelta(days=1)

    # if file exists, we don't want to redownload, as the articles shouldn't change
    if (os.path.exists(file_name)):
        print(date + " already exists. Skipping download.")
        continue

    # pause to avoid aborted connection
    sleeptime = random.choice(sleeptimes)
    time.sleep(sleeptime)
    # download the headlines using Beautiful Soup package
    try:    
        response = requests.get(url).content
        soup = BeautifulSoup(response,'html.parser')
        headlines = soup.find('section',attrs=section_headline_identifier)
        # save headlines to the txt file named with the date
        file = open(file_name, mode='a', encoding='latin1') # if file does not exists we create it, otherwise text is appended
        for headline in headlines.find_all('a'):
            file.write(headline['title'] + "\n")
        file.close()
        print(date + " successfully downloaded.")
    except Exception as e:
        # if error occurs delete the current file, so we do not re-download
        errors += 1
        if (os.path.exists(file_name)):
            file.close()
            os.remove(file_name)
        print("Error occured for date: " + date + ". " + "Not downloaded.")
        print(e)

print("Finished download with " + errors + " error." if errors == 1 else " errors.")