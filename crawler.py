from unicodedata import category
from bs4 import BeautifulSoup
import requests
import sqlite3 as sql
from datetime import datetime


home_url = "https://kathmandupost.com"

def getHTMLdocument(url):
      
    response = requests.get(url)
      
    return response.text

def getData(url):
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')

    # Title
    title = soup.title.text

    # Crawl content
    sections = soup.find_all("section", class_="story-section")
    content = ""
    for section in sections:
        content = content + section.text

    # Find date
    div = soup.find_all("div", class_="updated-time")[1]
    date = div.text.replace('Updated at : ', '')

    # Find category
    category = soup.find_all("h4", class_="title--line__red")[0].text

    return title, content, date, category

def exist_in_database(link, conn):
    cursor = conn.execute(f"SELECT * from backendservice_article WHERE link='{link}'")

    exist = False

    for row in cursor:
        exist = True

    return exist

def crawlKathmanduPOST():

    conn = sql.connect('bitesizenews/db.sqlite3')

    html_document = getHTMLdocument(home_url)

    soup = BeautifulSoup(html_document, 'html.parser')

    articles = soup.find_all("article")

    for article in articles:
        link = home_url + article.a['href']

        if exist_in_database(link, conn):
            continue

        title, content, date, category = getData(link)
        # Convert extracted date into correct format for the database
        date = datetime.strptime(date, '%B %d, %Y %H:%M ')

        if content == ' ':
            continue


        publisher = "Kathmandu Post"

        print(title)
        print(link)

        # Insert into the database
        conn.execute(f"INSERT INTO backendservice_article (title, content, link, publisher, category, published_date, summarization) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, content, link, publisher, category, date, ''))

    conn.commit()
    conn.close()


crawlKathmanduPOST()