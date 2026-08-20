import os
import sqlite3
import psycopg2

sqlite_conn = sqlite3.connect("/dane/links.db")
sqlite_cur = sqlite_conn.cursor()

sqlite_cur.execute(
    "SELECT id, code, url, clicks, created_at FROM links"
)
rows = sqlite_cur.fetchall()

pg_conn = psycopg2.connect(
    host="db",
    dbname="linkbox",
    user="linkbox",
    password=os.environ["POSTGRES_PASSWORD"],
)

pg_cur = pg_conn.cursor()

for row in rows:
    pg_cur.execute(
        """
        INSERT INTO links (id, code, url, clicks, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        row,
    )

pg_conn.commit()

pg_cur.close()
pg_conn.close()
sqlite_cur.close()
sqlite_conn.close()

print(f"Przeniesiono rekordów: {len(rows)}")
