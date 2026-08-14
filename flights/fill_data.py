from faker import Faker
from psycopg2 import connect
from psycopg2.extras import execute_values
import random
from config import Settings

fake = Faker()

config = Settings()

conn = connect(
    host=config.POSTGRES_HOSTNAME,
    port=config.DATABASE_PORT,
    database=config.POSTGRES_DB,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
)

with conn.cursor() as cursor:
    with open("airports_filtered.csv", "r", encoding="utf-8") as f:
        cursor.copy_expert(
            """
            COPY airport (
                name,
                city,
                country
            )
            FROM STDIN
            WITH (FORMAT csv, HEADER true)
            """,
            f,
        )

cursor = conn.cursor()

cursor.execute("SELECT id FROM airport")
airport_ids = [row[0] for row in cursor.fetchall()]
print(airport_ids)

TOTAL_ROWS = 1_000_000
BATCH_SIZE = 10_000

insert_query = """
    INSERT INTO flight (
        flight_number,
        datetime,
        from_airport_id,
        to_airport_id,
        price
    )
    VALUES %s
"""

for start in range(0, TOTAL_ROWS, BATCH_SIZE):
    batch_size = min(BATCH_SIZE, TOTAL_ROWS - start)

    rows = []

    for _ in range(batch_size):
        from_id, to_id = random.sample(airport_ids, 2)

        rows.append((
            fake.bothify("??###").upper(),
            fake.date_time_between(
                start_date="-30d",
                end_date="+365d",
            ),
            from_id,
            to_id,
            random.randint(50, 2000),
        ))

    execute_values(
        cursor,
        insert_query,
        rows,
        page_size=BATCH_SIZE,
    )

    conn.commit()

    print(f"Inserted {start + batch_size:,} / {TOTAL_ROWS:,}")

cursor.close()
conn.close()

