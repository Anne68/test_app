import os
from db import get_db, ensure_schema
from price_scraper import fetch_best_price_pc

BATCH_SIZE = int(os.getenv("PRICE_UPDATE_BATCH", "50"))
DAYS_STALE = int(os.getenv("PRICE_STALE_DAYS", "7"))

def pick_games_for_update(cur, limit:int):
    cur.execute(f"""
        SELECT g.game_id_rawg, g.title
        FROM games g
        LEFT JOIN best_price_latest b ON b.game_id_rawg = g.game_id_rawg
        WHERE b.ts IS NULL OR b.ts < NOW() - INTERVAL {DAYS_STALE} DAY
        ORDER BY (b.ts IS NULL) DESC, b.ts ASC
        LIMIT %s
    """, (limit,))
    return cur.fetchall()

def recompute_best_price_latest(cur):
    cur.execute("TRUNCATE TABLE best_price_latest")
    cur.execute("""
        INSERT INTO best_price_latest (game_id_rawg, platform, price, shop, url, ts)
        SELECT ph.game_id_rawg, 'PC' as platform, ph.price, ph.shop, ph.url, ph.ts
        FROM price_history ph
        JOIN (
            SELECT game_id_rawg, MIN(price) AS min_price
            FROM price_history
            GROUP BY game_id_rawg
        ) m
        ON ph.game_id_rawg = m.game_id_rawg AND ph.price = m.min_price
        JOIN (
            SELECT game_id_rawg, price, MAX(ts) AS max_ts
            FROM price_history
            GROUP BY game_id_rawg, price
        ) t
        ON ph.game_id_rawg = t.game_id_rawg AND ph.price = t.price AND ph.ts = t.max_ts
    """)

def run_update():
    conn = get_db()
    ensure_schema(conn)
    cur = conn.cursor()

    items = pick_games_for_update(cur, BATCH_SIZE)
    for game_id, title in items:
        res = fetch_best_price_pc(title)
        if not res:
            continue
        price, shop, url = res
        cur.execute(
            "INSERT INTO price_history (game_id_rawg, platform, price, shop, url) VALUES (%s,%s,%s,%s,%s)",
            (game_id, 'PC', price, shop, url)
        )
    conn.commit()

    recompute_best_price_latest(cur)
    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_update()
