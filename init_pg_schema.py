from pathlib import Path
import os
import psycopg


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL manquant")

    schema_path = Path(__file__).resolve().parent / "schema_cities.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"schema_cities.sql introuvable: {schema_path}")

    sql = schema_path.read_text(encoding="utf-8")

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print("Schéma PostgreSQL créé avec succès.")


if __name__ == "__main__":
    main()
