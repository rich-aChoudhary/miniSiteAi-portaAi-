# models/user_model.py
import uuid
from werkzeug.security import generate_password_hash
import config

class User:
    @staticmethod
    def save(username, password, email, device_mac=None):
        password_hash = generate_password_hash(password)
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Ensure required columns exist; add them if missing to avoid INSERT errors
                cursor.execute(
                    """
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users'
                    """
                )
                existing_cols = {row['COLUMN_NAME'] for row in cursor.fetchall()} if cursor.description else set()

                # Add password_hash if missing
                if 'password_hash' not in existing_cols:
                    try:
                        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT NULL")
                        existing_cols.add('password_hash')
                    except Exception:
                        pass

                # Add device_mac if missing
                if 'device_mac' not in existing_cols:
                    try:
                        cursor.execute("ALTER TABLE users ADD COLUMN device_mac VARCHAR(255) NULL")
                        existing_cols.add('device_mac')
                    except Exception:
                        pass

                # Add credits column if missing
                if 'credits' not in existing_cols:
                    try:
                        cursor.execute("ALTER TABLE users ADD COLUMN credits INT NOT NULL DEFAULT 1000")
                        existing_cols.add('credits')
                    except Exception:
                        pass

                # Build insert columns according to what's available now
                insert_cols = ['username', 'password_hash', 'email']
                values = [username, password_hash, email]
                # If an older schema uses a 'password' column (NOT NULL), ensure we populate it with the hashed password
                if 'password' in existing_cols and 'password' not in insert_cols:
                    insert_cols.append('password')
                    values.append(password_hash)
                if 'device_mac' in existing_cols:
                    insert_cols.append('device_mac')
                    values.append(device_mac)
                if 'credits' in existing_cols:
                    insert_cols.append('credits')
                    values.append(1000)

                cols_sql = ', '.join(insert_cols)
                placeholders = ', '.join(['%s'] * len(values))

                insert_sql = f"INSERT INTO users ({cols_sql}) VALUES ({placeholders})"
                cursor.execute(insert_sql, tuple(values))
                user_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') and cursor.lastrowid else None
                if not user_id:
                    cursor.execute("SELECT LAST_INSERT_ID() AS id")
                    row = cursor.fetchone()
                    user_id = row['id'] if row and 'id' in row else None
                conn.commit()
                return {
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'credits': 1000
                }
        finally:
            conn.close()
    @staticmethod
    def find_by_username(username):
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                row = cursor.fetchone()
                if row:
                    columns = [col[0] for col in cursor.description]
                    return dict(zip(columns, row))
                return None
        finally:
            conn.close()
    @staticmethod
    def find_by_email(email):
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cursor.fetchone()
                if row:
                    # If the cursor is using DictCursor, row will already be a dict.
                    # Otherwise, build a dict from cursor.description for consistency.
                    try:
                        if isinstance(row, dict):
                            return row
                    except Exception:
                        pass
                    columns = [col[0] for col in cursor.description] if cursor.description else None
                    if columns:
                        return dict(zip(columns, row))
                    return row
                return None
        finally:
            conn.close()

    @staticmethod
    def find_by_mac(device_mac):
        """Return the user row (dict when possible) for a given device MAC, or None."""
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE device_mac = %s", (device_mac,))
                row = cursor.fetchone()
                if row:
                    try:
                        if isinstance(row, dict):
                            return row
                    except Exception:
                        pass
                    columns = [col[0] for col in cursor.description] if cursor.description else None
                    if columns:
                        return dict(zip(columns, row))
                    return row
                return None
        finally:
            conn.close()

    @staticmethod
    def find_by_id(user_id):
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                if row:
                    try:
                        if isinstance(row, dict):
                            return row
                    except Exception:
                        pass
                    columns = [col[0] for col in cursor.description] if cursor.description else None
                    if columns:
                        return dict(zip(columns, row))
                    return row
                return None
        finally:
            conn.close()

    @staticmethod
    def decrement_credits(user_id, amount):
        """Atomically decrement credits if user has enough. Returns new balance or False on insufficient."""
        conn = config.get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET credits = credits - %s WHERE id = %s AND credits >= %s",
                    (amount, user_id, amount)
                )
                if cursor.rowcount == 0:
                    return False
                conn.commit()
                cursor.execute("SELECT credits FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                if row:
                    try:
                        return row.get('credits') if isinstance(row, dict) else row[0]
                    except Exception:
                        return None
                return None
        finally:
            conn.close()

    @staticmethod
    def get_credits(user_id):
        user = User.find_by_id(user_id)
        if not user:
            return None
        try:
            return int(user.get('credits') if isinstance(user, dict) else user[ 'credits' ])
        except Exception:
            return None
