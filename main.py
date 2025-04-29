import requests
import psycopg2
from datetime import datetime
import os

# Environment variables (set later in GitHub or Railway)
RPC_URL = os.getenv("RPC_URL")  # RPC endpoint for Celestia or another Cosmos chain
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")  # Wallet address to monitor
PGHOST = os.getenv("PGHOST")  # PostgreSQL host
PGUSER = os.getenv("PGUSER")  # PostgreSQL user
PGPASSWORD = os.getenv("PGPASSWORD")  # PostgreSQL password
PGDATABASE = os.getenv("PGDATABASE")  # PostgreSQL database name
PGPORT = os.getenv("PGPORT", "5432")  # PostgreSQL port (default is 5432)
COINGECKO_ID = os.getenv("COINGECKO_ID", "celestia")  # CoinGecko token ID

def get_balance():
    """Fetch wallet balances from the RPC endpoint."""
    url = f"{RPC_URL}/cosmos/bank/v1beta1/balances/{WALLET_ADDRESS}"
    response = requests.get(url)
    balances = response.json().get('balances', [])
    return balances

def get_price():
    """Fetch the current USD price for the token using CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_ID}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()[COINGECKO_ID]['usd']

def save_to_db(balances, price):
    """Save balances and token price to PostgreSQL."""
    conn = psycopg2.connect(
        dbname=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        host=PGHOST,
        port=PGPORT
    )
    cursor = conn.cursor()
    now = datetime.utcnow()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            id SERIAL PRIMARY KEY,
            address TEXT,
            denom TEXT,
            amount FLOAT,
            price_usd FLOAT,
            timestamp TIMESTAMP
        );
    """)

    # Insert each token balance
    for balance in balances:
        denom = balance['denom']
        amount = int(balance['amount']) / 10**6  # Cosmos tokens use 6 decimal places
        cursor.execute("""
            INSERT INTO balances (address, denom, amount, price_usd, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (WALLET_ADDRESS, denom, amount, price, now))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    balances = get_balance()
    price = get_price()
    save_to_db(balances, price)
    print("✅ Balances updated.")
