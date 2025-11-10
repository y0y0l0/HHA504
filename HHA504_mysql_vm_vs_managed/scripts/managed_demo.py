import pandas as pd
import time
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


load_dotenv('.env.example')  # This will automatically load from .env file


sql_username = os.getenv("MAN_USERNAME")
sql_password = os.getenv("MAN_PASSWORD")
sql_hostname = os.getenv("MAN_HOSTNAME")
sql_database = os.getenv("MAN_DATABASE")
sql_port = os.getenv("MAN_PORT")
sql_test_query = os.getenv("MAN_TEST_QUERY")

server_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}"
# --- 1) Connect to server (no DB) and ensure database exists ---

print("[STEP 1] Connecting to MySQL server (no DB):", server_url.replace(sql_password, "*****"))
t0 = time.time()

engine_server = create_engine(server_url, pool_pre_ping=True, connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}})
with engine_server.connect() as conn:
    # Read and execute the init.sql to create database if not exists
    with open("sql/init.sql", "r") as f:
        init_sql = f.read()
     # Execute each SQL command
    for command in init_sql.split(';'):
        if command.strip():  # Skip empty commands
            conn.execute(text(command))
    conn.commit()

print(f"[OK] Database initialized from init.sql")
print(f"[OK] Ensured database `{sql_database}` exists.")

# --- 2) Connect to the target database ---
db_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}/{sql_database}"
engine = create_engine(db_url, connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}})

# --- 3) Create a DataFrame and write to a table ---
table_name = "visits"
df = pd.DataFrame(
    [
        {"patient_id": 1, "visit_date": "2025-09-01", "bp_sys": 118, "bp_dia": 76},
        {"patient_id": 2, "visit_date": "2025-09-02", "bp_sys": 130, "bp_dia": 85},
        {"patient_id": 3, "visit_date": "2025-09-03", "bp_sys": 121, "bp_dia": 79},
        {"patient_id": 4, "visit_date": "2025-09-04", "bp_sys": 110, "bp_dia": 70},
        {"patient_id": 5, "visit_date": "2025-09-05", "bp_sys": 125, "bp_dia": 82},
    ]
)

df.to_sql(table_name, con=engine, if_exists="replace", index=False)

# --- 4) Read back a quick check ---
print("[STEP 4] Reading back row count ...")
with engine.connect() as conn:
    count_df = pd.read_sql(sql_test_query, con=conn)
print(count_df)

elapsed = time.time() - t0
print(f"[DONE] VM path completed in {elapsed:.1f}s at {datetime.now(timezone.utc).isoformat()}Z")