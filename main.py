import os
import requests

RPC_URL = os.getenv("RPC_URL")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
COINGECKO_ID = os.getenv("COINGECKO_ID")

print("🔍 Checking environment variables:")
print(f"RPC_URL = {RPC_URL}")
print(f"WALLET_ADDRESS = {WALLET_ADDRESS}")
print(f"COINGECKO_ID = {COINGECKO_ID}")

if not RPC_URL:
    print("❌ RPC_URL is missing!")
    exit(1)

if not WALLET_ADDRESS:
    print("❌ WALLET_ADDRESS is missing!")
    exit(1)

full_url = f"{RPC_URL}/cosmos/bank/v1beta1/balances/{WALLET_ADDRESS}"
print(f"🌐 Full request URL: {full_url}")

print("📡 Sending request...")
try:
    response = requests.get(full_url)
    print("✅ Response received!")

    print("Raw response text:")
    print(response.text)

except Exception as e:
    print("❌ Request failed:")
    print(str(e))
