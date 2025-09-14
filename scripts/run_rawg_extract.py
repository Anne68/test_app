import os
import datetime
import mysql.connector
from mysql.connector import Error
import requests
import time

# ==== Configuration ====
API_KEY = os.getenv("RAWG_API_KEY", "")
PAGE_SIZE = int(os.getenv("RAWG_PAGE_SIZE", "40"))
TOTAL_GAMES = int(os.getenv("RAWG_TOTAL_GAMES", "500"))

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-anne.alwaysdata.net")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "anne_games_db")

# ==== Fonctions utilitaires ====
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return conn
    except Error as e:
        print(f"❌ Erreur MySQL : {e}")
        return None

def get_json_with_retry(url, retries=5, backoff=2):
    for i in range(retries):
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(backoff ** i)
            continue
        r.raise_for_status()
    raise RuntimeError(f"Échec API RAWG après {retries} tentatives: {url}")

# ==== Extraction RAWG ====
def fetch_and_store_games():
    conn = connect_to_db()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INT PRIMARY KEY,
        title VARCHAR(255),
        release_date DATE,
        rating FLOAT,
        metacritic INT,
        last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    total_pages = TOTAL_GAMES // PAGE_SIZE
    for page in range(1, total_pages + 1):
        url = f"https://api.rawg.io/api/games?key={API_KEY}&page={page}&page_size={PAGE_SIZE}"
        data = get_json_with_retry(url)
        for game in data.get("results", []):
            cursor.execute("""
            INSERT INTO games (id, title, release_date, rating, metacritic)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              title=VALUES(title),
              release_date=VALUES(release_date),
              rating=VALUES(rating),
              metacritic=VALUES(metacritic),
              last_update=CURRENT_TIMESTAMP
            """, (
                game["id"],
                game["name"],
                game.get("released"),
                game.get("rating"),
                game.get("metacritic"),
            ))
        conn.commit()
        print(f"✅ Page {page} insérée ({len(data.get('results', []))} jeux).")

    cursor.close()
    conn.close()
    print("🎉 Extraction RAWG terminée.")

if __name__ == "__main__":
    fetch_and_store_games()
