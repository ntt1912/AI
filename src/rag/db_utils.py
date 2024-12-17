import sqlite3
from datetime import datetime

DB_NAME = 'rag.db'

def db_connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = db_connect()
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     model_response TEXT,
                     model TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

# def create_document_store():
#     conn = db_connect()
#     conn.execute('''CREATE TABLE IF NOT EXISTS document_store
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                      filename TEXT,
#                      upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
#     conn.close()

def insert_application_logs(session_id, user_query, model_response, model):
    conn = db_connect()
    conn.execute('INSERT INTO application_logs (session_id, user_query, model_response, model) VALUES (?, ?, ?, ?)',
                 (session_id, user_query, model_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, model_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['user_query']},
            {"role": "ai", "content": row['model_response']}
        ])
    conn.close()
    return messages

# Initialize the database tables
create_application_logs()