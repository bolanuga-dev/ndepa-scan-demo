import socket
import time
import os

MOCK_PII_PAYLOAD = {
    "merchant": "LagosPay_Core_API",
    "bvn_hash": "22490188312",
    "nin_ref": "NIN-NG-8841209",
    "settlement_currency": "NGN"
}

def probe_endpoint(label: str, host: str, port: int):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[OK] {label} -> Connected to {host}:{port}")
    except Exception as e:
        print(f"[TRACE] {label} -> Attempted connect() to {host}:{port} ({type(e).__name__})")

if __name__ == "__main__":
    domestic_host = os.getenv("DOMESTIC_CORE_HOST", "domestic-settlement-db")
    print("[*] Starting LagosPay Mock Fintech Egress Simulator...")

    while True:
        # 1. COMPLIANT: Domestic / Approved Regional Endpoint (NDPA Sec. 41 Compliant)
        probe_endpoint("APPROVED_DOMESTIC_LEDGER", domestic_host, 5432)

        # 2. VIOLATION: Unapproved Cross-Border Analytics / US & EU Cloud Egress (NDPA Sec. 41 Alert)
        probe_endpoint("UNAUTHORIZED_US_ANALYTICS_WEBHOOK", "8.8.8.8", 443)
        probe_endpoint("UNAUTHORIZED_EU_S3_BACKUP", "1.1.1.1", 443)

        time.sleep(5)
