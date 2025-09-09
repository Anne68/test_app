
import os
from typing import Dict
from db import get_db, ensure_schema, get_state, set_state
from rawg_client import fetch_games_page

PAGE_STATE_KEY = "rawg_next_page"

def upsert_game(cur, game: Dict):
    game_id = game.get("id")
    name = game.get("name")
    released = game.get("released")
    rating = game.get("rating") or None
    metacritic = game.get("metacritic") or None
    updated_at = game.get("updated") or None

    genres_list = game.get("genres") or []
    genres_csv = ", ".join([g.get("name") for g in genres_list if g and g.get("name")])

    cur.execute(
        """
        INSERT INTO games (game_id_rawg, title, release_date, genres, rating, metacritic, updated_at_utc)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          title=VALUES(title),
          release_date=VALUES(release_date),
          genres=VALUES(genres),
          rating=VALUES(rating),
          metacritic=VALUES(metacritic),
          updated_at_utc=VALUES(updated_at_utc)
        """,
        (game_id, name, released, genres_csv, rating, metacritic, updated_at)
    )

def upsert_platform(cur, platform: Dict):
    pid = platform.get("id")
    pname = platform.get("name")
    cur.execute(
        """
        INSERT INTO platforms (platform_id, platform_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE platform_name=VALUES(platform_name)
        """,
        (pid, pname)
    )

def link_game_platform(cur, game_id: int, platform_id: int):
    cur.execute(
        """
        INSERT IGNORE INTO game_platforms (game_id_rawg, platform_id)
        VALUES (%s, %s)
        """,
        (game_id, platform_id)
    )

def ingest_games(pages:int=5, page_size:int=40):
    conn = get_db()
    ensure_schema(conn)
    cur = conn.cursor()

    next_page_str = get_state(conn, PAGE_STATE_KEY, "1")
    page = int(next_page_str or "1")

    for _ in range(pages):
        data = fetch_games_page(page=page, page_size=page_size, ordering="-updated")
        results = data.get("results", [])
        if not results:
            page = 1
            continue

        for g in results:
            upsert_game(cur, g)
            for p in (g.get("platforms") or []):
                pinfo = p.get("platform") or {}
                if not pinfo:
                    continue
                upsert_platform(cur, pinfo)
                link_game_platform(cur, g.get("id"), pinfo.get("id"))

        conn.commit()
        page += 1
        set_state(conn, PAGE_STATE_KEY, str(page))

    cur.close()
    conn.close()

if __name__ == "__main__":
    pages = int(os.getenv("RAWG_PAGES_PER_RUN", "5"))
    ingest_games(pages=pages, page_size=40)
