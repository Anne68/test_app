from db import get_db, ensure_schema
from rawg_client import fetch_platforms_page

def ingest_all_platforms():
    conn = get_db()
    ensure_schema(conn)
    cur = conn.cursor()

    page = 1
    while True:
        data = fetch_platforms_page(page=page, page_size=40)
        results = data.get("results", [])
        if not results:
            break
        for p in results:
            cur.execute(
                """
                INSERT INTO platforms (platform_id, platform_name) VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE platform_name=VALUES(platform_name)
                """,
                (p.get("id"), p.get("name"))
            )
        conn.commit()
        if not data.get("next"):
            break
        page += 1

    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_all_platforms()
