# Step 1: Get all the un summarized data

# Step 2: Run summarization model to predict summary

# Step 3: Update to database
import sqlite3 as sql
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from datetime import datetime

print(f"{datetime.now()} Loading model.......")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-cnn_dailymail")
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-cnn_dailymail")
print(f"{datetime.now()} Loading complete !!")

conn = sql.connect('bitesizenews/db.sqlite3')

cursor = conn.execute("SELECT id, title, content from backendservice_article WHERE summarization=''")

count = 0
results = cursor.fetchall()
total = len(results)

for row in results:
    id = row[0]
    title = row[1]
    content = row[2]

    count = count+1

    t1 = datetime.now()

    # Step 2: Run summarization
    print(f"{t1} Summarizing {title}.......... {count}/{total}")
    inputs = tokenizer(content[:2048], max_length=2048, truncation=True, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"])
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    summary = summary.replace('<n>', '')

    cur = conn.cursor()
    cur.execute(f"UPDATE backendservice_article set summarization = ? where id = ?", (summary, id))
    conn.commit()

    t2 = datetime.now()

    print(f"{datetime.now()} Summarization of {title} completed. {t2-t1}")

print("Summarization complete !!")
conn.close()
