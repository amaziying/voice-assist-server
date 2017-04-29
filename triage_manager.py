import os
import urlparse

import psycopg2

# TODO: Move constants to DB/cache
high_p = ['pain', 'hurt', 'hurts', 'medicine', 'nausea', 'nauseous', 'dizzy', 'die', 'dying', 'death']
med_p = ['washroom', 'bathroom', 'toilet', 'uncomfortable']
low_p = ['water', 'food', 'ice', 'blanket', 'pillow', 'bed', 'adjust']

# Connect to PostgreSQL DB
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
columns = [
    'id',
    'patient_id',
    'ts_request',
    'ts_pickup',
    'ts_close',
    'transcription',
    'status',
    'priority_score',
]

def annotate_columns(row):
    row_dict = {}
    for i, val in enumerate(row):
        row_dict[columns[i]] = val

    return row_dict

def get_keyword_score(score, keyword):
    weight = 1
    text = keyword['text'].lower()

    if text in high_p:
        weight = 3
    elif text in med_p:
        weight = 2

    return score + weight*keyword['relevance']

def get_priority_score(sentiment, keywords):
    keyword_score = reduce(get_keyword_score, keywords, 1)
    sentiment_adjustment = 1 + abs(sentiment['score']) if sentiment['label'] == 'negative' else 1
    
    return keyword_score*sentiment_adjustment

def enqueue(patient_id, text, result):
    score = get_priority_score(result['sentiment']['document'], result['keywords'])
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO Requests (patient_id, transcription, status, priority_score) VALUES (%s, %s, %s, %s)""",
            (patient_id, text, 'OPEN', score))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_active_requests():
    result = []

    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Requests WHERE status<>%s ORDER BY priority_score DESC """, ('CLOSED',))
        result = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return map(annotate_columns, result)

def get_closed_requests():
    result = []

    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Requests WHERE status=%s ORDER BY priority_score DESC """, ('CLOSED',))
        result = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return map(annotate_columns, result)

def pickup_request(id):
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE Requests SET status=%s, ts_pickup=CURRENT_TIMESTAMP WHERE id=%s """,
            ('INPROGRESS', id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close_request(id):
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE Requests SET status=%s, ts_close=CURRENT_TIMESTAMP WHERE id=%s """,
            ('CLOSED', id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
