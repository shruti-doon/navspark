import sqlite3
import json
from pathlib import Path
import datetime


class AuditLogger:
    def __init__(self, db_path: str | Path = "data/output/audit_logs.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database table for storing LLM logs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                filename TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                parsed_json TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_interaction(self, filename: str, prompt: str, response: str, parsed_json: dict | None, status: str = "SUCCESS"):
        """Logs a single LLM interaction into the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().isoformat()
        parsed_data_str = json.dumps(parsed_json) if parsed_json else None
        
        cursor.execute('''
            INSERT INTO compliance_logs (timestamp, filename, prompt, response, parsed_json, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, filename, prompt, response, parsed_data_str, status))
        
        conn.commit()
        conn.close()
