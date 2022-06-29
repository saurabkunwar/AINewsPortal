import sqlite3 as sql
from unicodedata import category
import pandas as pd
from datetime import datetime

df = pd.read_csv("backup.csv")

conn = sql.connect('bitesizenews/db.sqlite3')

def delete_from_df():
    for _, row in df.iterrows():
        id = row["id"]

        conn.execute(f"DELETE FROM backendservice_article WHERE id={id}")

    conn.commit()

for index, row in df.iterrows():
    id = row["id"]
    title = row["title"]
    content = row["content"]
    link = row["link"]
    publisher = row["publisher"]
    category = row["category"]
    published_date = row["published_date"]
    summarization = row["summarization"]

    published_date = datetime.strptime(published_date, '%m/%d/%Y %H:%M')

    conn.execute(f"INSERT INTO backendservice_article (id, title, content, link, publisher, category, published_date, summarization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, title, content, link, publisher, category, published_date, summarization))

conn.commit()
conn.close()