# database.py
# Purpose: Manages SQLite storage for session results, stability scores,
# weak area tracking, and historical performance retrieval.
# Primary Owner: Sabyasachi Hazra

# storage/database.py

import sqlite3
import uuid
from datetime import datetime


class DatabaseManager:
    """
    Handles SQLite storage for:
    - Session results
    - Stability scores
    - Weak area tracking
    - Historical retrieval
    """

    def __init__(self, db_path="aynaeaagent.db"):
        self.db_path = db_path
        self._create_table()


    # ---------------------------------
    # Connection Helper
    # ---------------------------------

    def _connect(self):
        return sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )


    # ---------------------------------
    # Table Initialization
    # ---------------------------------

    def _create_table(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                topic TEXT,
                score REAL,
                mode TEXT,
                weak_area TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()


    # ---------------------------------
    # Save Session
    # ---------------------------------

    def save_session(self, topic, score, mode, weak_area=None):
        """
        Stores one evaluation cycle result.
        """

        conn = self._connect()
        cursor = conn.cursor()

        session_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO sessions (
                session_id, topic, score,
                mode, weak_area, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            topic,
            score,
            mode,
            weak_area,
            timestamp
        ))

        conn.commit()
        conn.close()

        return session_id


    # ---------------------------------
    # Retrieve Topic History
    # ---------------------------------

    def get_topic_history(self, topic):
        """
        Returns all past sessions for a topic.
        """

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, score, mode, weak_area, timestamp
            FROM sessions
            WHERE topic = ?
            ORDER BY timestamp ASC
        """, (topic,))

        rows = cursor.fetchall()
        conn.close()

        return rows


    # ---------------------------------
    # Retrieve Recent Sessions
    # ---------------------------------

    def get_recent_sessions(self, limit=10):
        """
        Returns most recent session results.
        """

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT topic, score, mode, timestamp
            FROM sessions
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return rows


    # ---------------------------------
    # Get Weak Areas
    # ---------------------------------

    def get_weak_areas(self, threshold=50):
        """
        Returns topics with low average stability.
        """

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT topic, AVG(score) as avg_score
            FROM sessions
            GROUP BY topic
            HAVING avg_score < ?
        """, (threshold,))

        rows = cursor.fetchall()
        conn.close()

        return rows