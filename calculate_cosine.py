# Calculate cosine

from hashlib import new
import pandas as pd
import sqlite3 as sql
from datetime import date, datetime
import numpy as np
import os

from sentence_transformers import SentenceTransformer, util
import torch

def calculate_cosine(model, target_sentence, target_df):
  target_embedding = model.encode(target_sentence, convert_to_tensor=True)
  title_list = list(target_df["content"])
  list_embedding = model.encode(title_list, convert_to_tensor=True)
  cosine_scores = util.cos_sim(target_embedding, list_embedding)
  cosine_list = torch.squeeze(cosine_scores).tolist()
  return list(target_df.id), cosine_list


# Read from database
def get_batch(last_id):
    conn = sql.connect('bitesizenews/db.sqlite3')
    cursor = conn.execute(f"SELECT id, content from backendservice_article WHERE id <= {last_id}")

    # Get all contents
    results = cursor.fetchall()

    contents = []
    ids = []

    for row in results:
        id = row[0]
        content = row[1]

        ids.append(id)
        contents.append(content)
        
    return ids, contents


# Taking dummy content
#target_id = ids[1]
#target_content = [contents[1]]

def cosine_calculation(target_id, target_content):

    # Loading Model
    print("Loading Model......")
    l1 = datetime.now()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    l2 = datetime.now()
    print(f"Model loaded, Load time {l2-l1}")

    df = pd.read_csv("bitesizenews/cosine.csv")
    df = df.drop(columns=["Unnamed: 0"])
    df["id"] = df["id"].astype("int")

    # Check if cosine is in database
    if target_id not in list(df.columns):

        last_id = df.iloc[-1]["id"].astype("int")

        ids, contents = get_batch(last_id)
        
        ids.append(target_id)
        contents.append(target_content)
        
        print(ids)

        target_dict = {
            "id":ids,
            "content":contents
        }

        target_df = pd.DataFrame.from_dict(target_dict)

        id, cosine = calculate_cosine(model, target_content, target_df)

        new_row = [target_id] + cosine

        print(new_row)

        df[target_id] = np.nan

        df.loc[len(df)] = new_row
        
    else:
        print("Cosine calculation already exists")

    df.to_csv("bitesizenews/cosine.csv")