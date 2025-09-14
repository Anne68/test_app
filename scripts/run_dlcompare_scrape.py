import os
import time
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-anne.alwaysdata.net")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "anne_games_db")

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

def scrape_prices():
    conn = connect_to_db()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS best_price_pc (game_id INT, shop VARCHAR(255), price FLOAT)")
    cursor.execute("SELECT id, title FROM games")
    games = cursor.fetchall()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    for game_id, title in games:
        url = f"https://www.dlcompare.fr/recherche/{title.replace(' ', '+')}"
        try:
            driver.get(url)
            time.sleep(3)

            shop_elem = driver.find_element(By.CSS_SELECTOR, ".offers-table .shop a")
            price_elem = driver.find_element(By.CSS_SELECTOR, ".offers-table .price")

            shop = shop_elem.text
            price = float(price_elem.text.replace("€", "").replace(",", ".").strip())

            cursor.execute("""
            INSERT INTO best_price_pc (game_id, shop, price)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE shop=VALUES(shop), price=VALUES(price)
            """, (game_id, shop, price))
            conn.commit()
            print(f"✅ {title} : {price}€ chez {shop}")
        except Exception as e:
            print(f"⚠️ {title} non trouvé ({e})")
            continue

    driver.quit()
    cursor.close()
    conn.close()
    print("🎉 Scraping DLCompare terminé.")

if __name__ == "__main__":
    scrape_prices()
