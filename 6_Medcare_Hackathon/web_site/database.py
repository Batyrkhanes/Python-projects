import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Web users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    name TEXT,
                    iin TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    telegram_user_id INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    iin TEXT,
                    temperature REAL,
                    heart_rate INTEGER,
                    breathing_rate INTEGER,
                    symptoms TEXT,
                    priority INTEGER DEFAULT 5,
                    status TEXT DEFAULT 'Плановое',
                    ai_analysis TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    telegram_user_id INTEGER,
                    web_user_id INTEGER,
                    FOREIGN KEY (web_user_id) REFERENCES web_users(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    iin TEXT,
                    specialist TEXT,
                    appointment_date TEXT,
                    appointment_time TEXT,
                    qr_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    telegram_user_id INTEGER,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS telegram_users (
                    telegram_id INTEGER PRIMARY KEY,
                    iin TEXT,
                    name TEXT,
                    osms_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def add_patient(self, data):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO patients (name, age, iin, temperature, heart_rate, 
                                     breathing_rate, symptoms, priority, status, 
                                     ai_analysis, telegram_user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('name'),
                data.get('age'),
                data.get('iin'),
                data.get('temperature'),
                data.get('heart_rate'),
                data.get('breathing_rate'),
                data.get('symptoms'),
                data.get('priority', 5),
                data.get('status', 'Плановое'),
                data.get('ai_analysis'),
                data.get('telegram_user_id')
            ))
            return cursor.lastrowid
    
    def get_patients(self, limit=50):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM patients 
                ORDER BY priority DESC, created_at DESC 
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_patient(self, patient_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
            return cursor.rowcount > 0
    
    def add_appointment(self, data):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (patient_id, iin, specialist, 
                                         appointment_date, appointment_time, 
                                         qr_data, telegram_user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('patient_id'),
                data.get('iin'),
                data.get('specialist'),
                data.get('appointment_date'),
                data.get('appointment_time'),
                data.get('qr_data'),
                data.get('telegram_user_id')
            ))
            return cursor.lastrowid
    
    def get_appointments(self, telegram_user_id=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if telegram_user_id:
                cursor.execute('''
                    SELECT * FROM appointments 
                    WHERE telegram_user_id = ? 
                    ORDER BY created_at DESC
                ''', (telegram_user_id,))
            else:
                cursor.execute('''
                    SELECT * FROM appointments 
                    ORDER BY created_at DESC
                ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def save_chat_message(self, user_id, role, content):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_history (user_id, role, content)
                VALUES (?, ?, ?)
            ''', (user_id, role, content))
    
    def get_chat_history(self, user_id, limit=50):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, content, created_at 
                FROM chat_history 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            messages = [dict(row) for row in cursor.fetchall()]
            return list(reversed(messages))
    
    def clear_chat_history(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    
    def save_telegram_user(self, telegram_id, iin, name, osms_status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO telegram_users 
                (telegram_id, iin, name, osms_status)
                VALUES (?, ?, ?, ?)
            ''', (telegram_id, iin, name, osms_status))
    
    def get_telegram_user(self, telegram_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM telegram_users WHERE telegram_id = ?
            ''', (telegram_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    def create_web_user(self, email, password_hash, name=None, iin=None):
        """Create new web user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO web_users (email, password_hash, name, iin)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, name, iin))
            return cursor.lastrowid
            
    def get_web_user(self, email):
        """Get web user data by email"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM web_users WHERE email = ?', (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    def link_telegram_to_web(self, web_user_id, telegram_user_id):
        """Link Telegram account to web account"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE web_users 
                SET telegram_user_id = ? 
                WHERE id = ?
            ''', (telegram_user_id, web_user_id))
            
    def get_user_appointments(self, user_id, is_telegram=False):
        """Get user appointments (web or telegram)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if is_telegram:
                cursor.execute('''
                    SELECT * FROM appointments 
                    WHERE telegram_user_id = ? 
                    ORDER BY appointment_date DESC, appointment_time DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT a.* FROM appointments a
                    JOIN web_users w ON a.web_user_id = w.id
                    WHERE w.id = ?
                    ORDER BY a.appointment_date DESC, a.appointment_time DESC
                ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
