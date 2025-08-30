#!/usr/bin/env python3
# smart_fraud_chatbot.py
# Single-file prototype: Fraud detection + NLP chatbot + SQLite case management

import os
import re
import sqlite3
import time
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple

import pandas as pd
from sklearn.ensemble import IsolationForest

# -----------------------------
# Config
# -----------------------------
DB_PATH = "fraud_system.db"
CONTAMINATION = 0.15  # % of data expected to be anomalous
RANDOM_SEED = 42

# -----------------------------
# Data classes
# -----------------------------
@dataclass
class Transaction:
    user_id: str
    amount: float
    location_code: int      # city/device/location encoded
    hour_of_day: int        # 0..23
    device_new: int         # 0/1
    txn_id: str = ""

@dataclass
class FraudAlert:
    user_id: str
    txn_id: str
    reason: str
    score: float

@dataclass
class Case:
    case_id: int
    user_id: str
    description: str
    status: str = "open"

# -----------------------------
# Database helpers
# -----------------------------
def db_connect(path: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(path)

def db_init():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        txn_id TEXT PRIMARY KEY,
        user_id TEXT,
        amount REAL,
        location_code INTEGER,
        hour_of_day INTEGER,
        device_new INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        txn_id TEXT,
        user_id TEXT,
        reason TEXT,
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases(
        case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        description TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def db_insert_transactions(rows: List[Transaction]):
    conn = db_connect()
    cur = conn.cursor()
    cur.executemany("""
    INSERT OR REPLACE INTO transactions(txn_id,user_id,amount,location_code,hour_of_day,device_new)
    VALUES(?,?,?,?,?,?);
    """, [(t.txn_id, t.user_id, t.amount, t.location_code, t.hour_of_day, t.device_new) for t in rows])
    conn.commit()
    conn.close()

def db_insert_alert(alert: FraudAlert):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO alerts(txn_id,user_id,reason,score) VALUES(?,?,?,?);
    """, (alert.txn_id, alert.user_id, alert.reason, alert.score))
    conn.commit()
    conn.close()

def db_create_case(user_id: str, description: str) -> int:
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO cases(user_id,description,status) VALUES(?,?,?);
    """, (user_id, description, "open"))
    conn.commit()
    case_id = cur.lastrowid
    conn.close()
    return case_id

def db_update_case_status(case_id: int, status: str) -> bool:
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE cases SET status=? WHERE case_id=?;", (status, case_id))
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated

def db_get_latest_alert(user_id: str) -> Dict[str, Any]:
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT txn_id, reason, score, created_at FROM alerts
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {}
    return {"txn_id": row[0], "reason": row[1], "score": row[2], "created_at": row[3]}

def db_list_cases(user_id: str) -> List[Case]:
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT case_id, user_id, description, status FROM cases
    WHERE user_id = ?
    ORDER BY case_id DESC;
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [Case(case_id=r[0], user_id=r[1], description=r[2], status=r[3]) for r in rows]

# -----------------------------
# Simulation & detection
# -----------------------------
def simulate_transactions(user_id: str, n: int = 40, anomaly_boost: int = 4) -> List[Transaction]:
    """
    Generate mostly normal behavior, with a few anomalies:
    - unusually high amount
    - far location_code
    - odd hour
    - first-time device
    """
    rng = random.Random(RANDOM_SEED)
    rows: List[Transaction] = []
    for i in range(n):
        amount = rng.gauss(800, 200)     # INR typical small spends
        amount = max(50, amount)

        location = rng.choice([1, 1, 1, 2])   # Mostly home location (1), sometimes 2
        hour = rng.choice([10, 13, 18, 20, 12, 19])
        device_new = 0

        txn_id = f"TXN-{int(time.time()*1000)}-{i}-{rng.randint(100,999)}"
        rows.append(Transaction(user_id=user_id, amount=amount, location_code=location, hour_of_day=hour,
                                device_new=device_new, txn_id=txn_id))

    # Inject anomalies
    for j in range(anomaly_boost):
        txn_id = f"TXN-{int(time.time()*1000)}-A{j}-{random.randint(100,999)}"
        rows.append(Transaction(
            user_id=user_id,
            amount=rng.uniform(15000, 60000),         # very high
            location_code=rng.choice([5, 6, 7, 9]),   # far location
            hour_of_day=rng.choice([0, 1, 2, 3]),     # odd hours
            device_new=1,
            txn_id=txn_id
        ))

    rng.shuffle(rows)
    return rows

def fit_isolation_forest(df: pd.DataFrame) -> Tuple[IsolationForest, pd.Series]:
    model = IsolationForest(
        contamination=CONTAMINATION,
        random_state=RANDOM_SEED,
        n_estimators=200,
        bootstrap=True
    )
    features = df[["amount", "location_code", "hour_of_day", "device_new"]]
    model.fit(features)
    scores = model.score_samples(features)  # higher = more normal
    preds = model.predict(features)         # 1 normal, -1 anomaly
    return model, pd.Series(preds, index=df.index), pd.Series(scores, index=df.index)

def explain_reason(row: pd.Series, df_stats: Dict[str, Tuple[float, float]]) -> str:
    reasons = []
    amt_mean, amt_std = df_stats["amount"]
    if row["amount"] > amt_mean + 3*amt_std:
        reasons.append("unusually high amount")
    if row["location_code"] >= 5:
        reasons.append("unfamiliar location")
    if row["hour_of_day"] in (0,1,2,3):
        reasons.append("odd login/transaction hour")
    if row["device_new"] == 1:
        reasons.append("new device")
    if not reasons:
        reasons.append("behavior deviates from historical pattern")
    return ", ".join(reasons)

# -----------------------------
# NLP-ish intent detection
# -----------------------------
INTENT_PATTERNS = {
    "why_flagged": re.compile(r"(why|reason).*(flag|alert|blocked|hold)", re.I),
    "report_fraud": re.compile(r"(report|raise|submit).*(fraud|issue|case|complaint)", re.I),
    "check_status": re.compile(r"(status|track|progress).*(case|ticket|complaint|id)", re.I),
    "list_cases": re.compile(r"(my|show|list).*(cases|tickets|complaints)", re.I),
    "help": re.compile(r"(help|what can you do|\?)", re.I),
    "exit": re.compile(r"(exit|quit|bye)", re.I),
}

HELP_TEXT = (
    "I can help with:\n"
    "• Why was my account flagged?\n"
    "• Report a fraud case\n"
    "• Check case status (e.g., 'status of case 3')\n"
    "• List my cases\n"
    "Type 'exit' to quit."
)

# -----------------------------
# Chatbot core
# -----------------------------
class SmartFraudSystem:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.model = None

    def ingest_and_detect(self):
        # Simulate and store transactions
        txns = simulate_transactions(self.user_id)
        db_insert_transactions(txns)

        # Build dataframe from DB for detection
        conn = db_connect()
        df = pd.read_sql_query(
            "SELECT txn_id, user_id, amount, location_code, hour_of_day, device_new FROM transactions WHERE user_id = ?;",
            conn, params=(self.user_id,)
        )
        conn.close()

        # Fit model & detect
        self.model, preds, scores = fit_isolation_forest(df)

        # Stats for simple rule explanations
        df_stats = {
            "amount": (df["amount"].mean(), df["amount"].std() if df["amount"].std() else 1.0),
        }

        anomalies = []
        for idx, pred in preds.items():
            if pred == -1:
                row = df.loc[idx]
                reason = explain_reason(row, df_stats)
                alert = FraudAlert(
                    user_id=row["user_id"],
                    txn_id=row["txn_id"],
                    reason=reason,
                    score=float(scores.loc[idx])
                )
                db_insert_alert(alert)
                anomalies.append(alert)
        return df, anomalies

    # ---- Chatbot responses ----
    def handle_input(self, text: str) -> str:
        text = text.strip()

        if INTENT_PATTERNS["exit"].search(text):
            return "__EXIT__"

        if INTENT_PATTERNS["why_flagged"].search(text):
            latest = db_get_latest_alert(self.user_id)
            if not latest:
                return "You're all clear. I don't see any recent alerts on your account."
            return (
                f"Your account was flagged due to {latest['reason']}.\n"
                f"Txn ID: {latest['txn_id']} | Risk score: {latest['score']:.3f}\n"
                f"Would you like to report this as fraud? If yes, say: report fraud <short description>."
            )

        if INTENT_PATTERNS["report_fraud"].search(text):
            # extract description
            m = re.search(r"report.*?:?\s*(.*)", text, re.I)
            desc = m.group(1).strip() if m and m.group(1) else "Suspected unauthorized activity."
            case_id = db_create_case(self.user_id, desc)
            return f"Your fraud case has been submitted. Case ID: {case_id}. We'll keep you posted."

        if INTENT_PATTERNS["check_status"].search(text):
            # try to find a case id
            m = re.search(r"(case\s*#?\s*)(\d+)", text, re.I)
            if not m:
                return "Please specify a case ID, e.g., 'status of case 3'."
            case_id = int(m.group(2))
            conn = db_connect()
            cur = conn.cursor()
            cur.execute("SELECT status FROM cases WHERE case_id=? AND user_id=?;", (case_id, self.user_id))
            row = cur.fetchone()
            conn.close()
            if not row:
                return f"I couldn't find case {case_id} for your account."
            return f"Case {case_id} status: {row[0]}."

        if INTENT_PATTERNS["list_cases"].search(text):
            cases = db_list_cases(self.user_id)
            if not cases:
                return "You have no cases yet."
            lines = [f"Case {c.case_id}: {c.description} [{c.status}]" for c in cases]
            return "Your cases:\n" + "\n".join(lines)

        if INTENT_PATTERNS["help"].search(text) or text.lower() in ("menu", "options"):
            return HELP_TEXT

        # Default fallback
        return (
            "I didn't fully catch that. " 
            "Try: 'why was I flagged?', 'report fraud <details>', 'list my cases', or 'status of case 2'."
        )

# -----------------------------
# CLI application
# -----------------------------
def main():
    print("="*62)
    print(" Smart Fraud Alert Chatbot (NLP) — Single File Prototype ")
    print("="*62)

    # Fresh DB for demo runs (optional). Comment out if you want persistence.
    if not os.path.exists(DB_PATH):
        db_init()

    # Create/ensure tables exist
    db_init()

    # Demo user
    user_id = "user_1001"

    system = SmartFraudSystem(user_id=user_id)
    df, anomalies = system.ingest_and_detect()

    print(f"\nLoaded {len(df)} transactions for {user_id}.")
    if anomalies:
        print(f"Detected {len(anomalies)} suspicious activities. Latest reasons:")
        for a in anomalies[:3]:
            print(f" - {a.txn_id}: {a.reason} (score {a.score:.3f})")
    else:
        print("No suspicious activity detected.")

    print("\nChat with the bot. Type 'help' to see options. Type 'exit' to quit.\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Stay safe!")
            break

        if not user_text:
            continue

        reply = system.handle_input(user_text)
        if reply == "__EXIT__":
            print("Bot: Goodbye.")
            break
        print(f"Bot: {reply}")

if __name__ == "__main__":
    main()
