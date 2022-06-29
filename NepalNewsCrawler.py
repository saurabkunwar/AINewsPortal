from unicodedata import category
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import requests
from datetime import datetime
import sqlite3 as sql
import calculate_cosine

home_url = "https://www.nepalnews.com/"

def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


def getData(url):
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')

    # Title
    title = soup.title.text.split(' | ')[0]

    # Crawl Content
    div = soup.find_all("div", class_="uk-text-large")[0]
    paragraphs = div.find_all("p")
    content = ""
    for p in paragraphs:
        if p.text.strip() == "":
            continue
        content = content + p.text


    # Find date
    div = soup.find_all("div", class_="el-meta")[0]
    span = div.find_all("span")
    date = ','.join(span[0].text.split(',')[:2])
    date = datetime.strptime(date, '%Y %b %d, %H:%M')

    # Find Category
    category = url.split('/')[4]

    return title, content, date, category

def exist_in_database(link, conn):
    cursor = conn.execute(f"SELECT * from backendservice_article WHERE link='{link}'")

    exist = False

    for row in cursor:
        exist = True

    return exist

def getLinks():
    http = httplib2.Http()
    _, response = http.request(home_url)
    links = []
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):

            href = link['href']
            # Filter out outside links
            if href.startswith('https://www.nepalnews.com/s/'):
                # Remove link of categories
                if len(href.split('/')) == 5:
                    continue
                
                # Avoid duplicate url
                if href in links:
                    continue

                links.append(href)

    return links

def crawlNepalNews():
    conn = sql.connect('bitesizenews/db.sqlite3')
    links = getLinks()

    for link in links:
        if exist_in_database(link, conn):
            continue

        
        title, content, date, category = getData(link)

        publisher = "Nepal News"

        print(title)
        print(link)

        cursor=conn.cursor()

        cursor.execute(f"INSERT INTO backendservice_article (title, content, link, publisher, category, published_date, summarization) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, content, link, publisher, category, date, ''))

        #calculate_cosine.cosine_calculation(cursor.lastrowid, content)

    conn.commit()
    conn.close()

crawlNepalNews()