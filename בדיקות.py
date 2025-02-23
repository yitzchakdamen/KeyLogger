from datetime import datetime
import sqlite3


class DataBase:

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self):
        """
        יצירת טבלה לאחסון אירועים עם מזהה, תיאור ותאריך
        הערה: כל השינויים במסד הנתונים צריכים להישמר באמצעות conn.commit()
        כדי שיהיו קבועים ולא יאבדו
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                event_date TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_event(self, description, date):
        """
        הוספת אירוע חדש עם תאריך
        """
        try:
            # המרה של התאריך לפורמט תקין
            date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            # הוספת האירוע לזיכרון זמני
            self.cursor.execute(
                "INSERT INTO events (description, event_date) VALUES (?, ?)",
                (description, date_obj)
            )

            # שמירה סופית במסד הנתונים
            self.conn.commit()
            print(f"האירוע נוסף בהצלחה לתאריך {date}")
        except ValueError:
            print("שגיאה: התאריך חייב להיות בפורמט YYYY-MM-DD HH:MM:SS")

    def get_events_by_date(self, year=None, month=None, day=None, hour=None, minute=None):
        """
        קבלת אירועים לפי תנאי תאריך וזמן
        ניתן לספק כל אחד מהפרמטרים הבאים:
            year - שנה
            month - חודש
            day - יום
            hour - שעה
            minute - דקה
        """
        query = "SELECT * FROM events WHERE 1=1"
        params = []

        if year:
            query += " AND strftime('%Y', event_date) = ?"
            params.append(str(year))

        if month:
            query += " AND strftime('%m', event_date) = ?"
            params.append(str(month))

        if day:
            query += " AND strftime('%d', event_date) = ?"
            params.append(str(day))

        if hour:
            query += " AND strftime('%H', event_date) = ?"
            params.append(str(hour))

        if minute:
            query += " AND strftime('%M', event_date) = ?"
            params.append(str(minute))

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def delete_events_by_date(self, year=None, month=None, day=None, hour=None, minute=None):
        """
        מחיקת אירועים לפי תנאי תאריך וזמן
        ניתן לספק כל אחד מהפרמטרים הבאים:
            year - שנה
            month - חודש
            day - יום
            hour - שעה
            minute - דקה
        """
        query = "DELETE FROM events WHERE 1=1"
        params = []

        if year:
            query += " AND strftime('%Y', event_date) = ?"
            params.append(str(year))

        if month:
            query += " AND strftime('%m', event_date) = ?"
            params.append(str(month))

        if day:
            query += " AND strftime('%d', event_date) = ?"
            params.append(str(day))

        if hour:
            query += " AND strftime('%H', event_date) = ?"
            params.append(str(hour))

        if minute:
            query += " AND strftime('%M', event_date) = ?"
            params.append(str(minute))

        self.cursor.execute(query, params)
        self.conn.commit()
        print(f"נמחקו {self.cursor.rowcount} אירועים")
        return self.cursor.rowcount

    def retrieval_from_database(self, year=None, month=None, day=None, hour=None, minute=None):
        """
        הצגת אירועים לפי תנאי תאריך וזמן
        """
        for event in self.get_events_by_date(year, month, day, hour, minute):
            print(f"מזהה: {event[0]}, תיאור: {event[1]}, תאריך: {event[2]}")


# דוגמת שימוש
if __name__ == '__main__':
    # יצירת קישור למסד הנתונים
    with DataBase() as d:
        # יצירת הטבלה
        d.create_table()

        # הוספת אירועים
        d.add_event("פגישת צוות", "2025-03-01 14:30:00")
        d.add_event("ישיבת לקוח", "2025-03-01 15:45:00")

        # הצגת כל האירועים
        print("\n=== כל האירועים ===")
        d.retrieval_from_database()

        # הצגת אירועים מהשעה 14:30
        print("\n=== אירועים בשעה 14:30 ===")
        d.retrieval_from_database(hour=14, minute=30)

        # מחיקת אירועים מהשעה 14:30
        print("\n=== מחיקת אירועים בשעה 14:30 ===")
        d.delete_events_by_date(hour=14, minute=30)

        d.retrieval_from_database()
        d.delete_events_by_date()
        d.retrieval_from_database()