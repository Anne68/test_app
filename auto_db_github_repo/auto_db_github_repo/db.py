import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "games_db"),
        autocommit=False,
    )
    return conn

def ensure_schema(conn):
    from pathlib import Path
    sql_path = Path(__file__).with_name("create_tables.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cur = conn.cursor()
    for statement in [s.strip() for s in sql_script.split(";") if s.strip()]:
        cur.execute(statement)
    conn.commit()
    cur.close()

def get_state(conn, key: str, default: str = None):
    cur = conn.cursor()
    cur.execute("SELECT state_value FROM api_state WHERE state_key=%s", (key,))
    row = cur.fetchone()
    cur.close()
    if row:
        return row[0]
    return default

def set_state(conn, key: str, value: str):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO api_state(state_key, state_value) VALUES(%s,%s) "
        "ON DUPLICATE KEY UPDATE state_value=VALUES(state_value), updated_at=CURRENT_TIMESTAMP",
        (key, value),
    )
    conn.commit()
    cur.close()
