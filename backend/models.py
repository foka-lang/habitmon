from datetime import date
from database import get_db_connection
from config import Config

config = Config()


class User:
    """Работа с пользователями"""

    @staticmethod
    def get_or_create(telegram_id, username=None, full_name=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return dict(user)

        cursor.execute('''
                       INSERT INTO users (telegram_id, username, full_name)
                       VALUES (?, ?, ?)
                       ''', (telegram_id, username, full_name))
        user_id = cursor.lastrowid

        cursor.execute('INSERT INTO user_points (user_id) VALUES (?)', (user_id,))
        cursor.execute('INSERT INTO user_levels (user_id) VALUES (?)', (user_id,))

        conn.commit()
        conn.close()

        return User.get_by_telegram_id(telegram_id)

    @staticmethod
    def get_by_telegram_id(telegram_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_streak(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        today = date.today().isoformat()
        cursor.execute('SELECT current_streak, max_streak, last_activity_date FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return 0

        last_date = user['last_activity_date']
        current_streak = user['current_streak']
        max_streak = user['max_streak']

        if last_date == today:
            conn.close()
            return current_streak

        yesterday = date.today().replace(day=date.today().day - 1).isoformat()
        if last_date == yesterday:
            current_streak += 1
        else:
            current_streak = 0

        if current_streak > max_streak:
            max_streak = current_streak

        cursor.execute('''
                       UPDATE users
                       SET current_streak     = ?,
                           max_streak         = ?,
                           last_activity_date = ?
                       WHERE id = ?
                       ''', (current_streak, max_streak, today, user_id))

        conn.commit()
        conn.close()
        return current_streak


class Habit:
    """Работа с привычками"""

    @staticmethod
    def create(user_id, name, emoji='📌', frequency='daily', custom_days=None, reminder_time=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO habits (user_id, name, emoji, frequency, custom_days, reminder_time)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (user_id, name, emoji, frequency, custom_days, reminder_time))
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return habit_id

    @staticmethod
    def get_user_habits(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT *
                       FROM habits
                       WHERE user_id = ?
                         AND is_active = 1
                       ORDER BY created_at DESC
                       ''', (user_id,))
        habits = cursor.fetchall()
        conn.close()
        return [dict(h) for h in habits]


class HabitLog:
    """Работа с логами привычек"""

    @staticmethod
    def log(habit_id, date_str, completed=1, note=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM habit_logs WHERE habit_id = ? AND date = ?', (habit_id, date_str))
        existing = cursor.fetchone()

        if existing:
            cursor.execute('UPDATE habit_logs SET completed = ?, note = ? WHERE id = ?',
                           (completed, note, existing['id']))
        else:
            cursor.execute('INSERT INTO habit_logs (habit_id, date, completed, note) VALUES (?, ?, ?, ?)',
                           (habit_id, date_str, completed, note))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_completed_count(user_id, start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT COUNT(*) as count
                       FROM habit_logs hl
                           JOIN habits h
                       ON h.id = hl.habit_id
                       WHERE h.user_id = ? AND hl.date BETWEEN ? AND ? AND hl.completed = 1
                       ''', (user_id, start_date, end_date))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0


class UserPoints:
    """Работа с баллами пользователя"""

    @staticmethod
    def add_points(user_id, points):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE user_points
                       SET total_points = total_points + ?,
                           updated_at   = CURRENT_TIMESTAMP
                       WHERE user_id = ?
                       ''', (points, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_points(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT total_points FROM user_points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['total_points'] if result else 0

    @staticmethod
    def spend_points(user_id, points):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT total_points FROM user_points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if not result or result['total_points'] < points:
            conn.close()
            return False

        cursor.execute('''
                       UPDATE user_points
                       SET total_points = total_points - ?,
                           updated_at   = CURRENT_TIMESTAMP
                       WHERE user_id = ?
                       ''', (points, user_id))
        conn.commit()
        conn.close()
        return True


class UserLevel:
    """Работа с уровнями и XP"""

    @staticmethod
    def add_xp(user_id, xp):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT level, xp, total_xp_earned FROM user_levels WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return 0

        level = result['level']
        current_xp = result['xp'] + xp
        total_xp = result['total_xp_earned'] + xp

        leveled_up = 0
        while current_xp >= Config.xp_needed_for_level(level) and level < Config.MAX_LEVEL:
            current_xp -= Config.xp_needed_for_level(level)
            level += 1
            leveled_up += 1

        cursor.execute('''
                       UPDATE user_levels
                       SET level           = ?,
                           xp              = ?,
                           total_xp_earned = ?,
                           updated_at      = CURRENT_TIMESTAMP
                       WHERE user_id = ?
                       ''', (level, current_xp, total_xp, user_id))

        conn.commit()
        conn.close()
        return leveled_up

    @staticmethod
    def get_level_info(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT level, xp, total_xp_earned FROM user_levels WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return {'level': 1, 'xp': 0, 'xp_needed': 50, 'total_xp': 0}

        level = result['level']
        xp = result['xp']
        xp_needed = Config.xp_needed_for_level(level) if level < Config.MAX_LEVEL else None

        return {
            'level': level,
            'xp': xp,
            'xp_needed': xp_needed,
            'total_xp': result['total_xp_earned']
        }