from datetime import datetime
import sqlite3
from Encryptor import Encryptor


class DataBase:

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.create_table()
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
                event_date TIMESTAMP,
                machine_name TEXT
            )
        ''')
        self.conn.commit()

    def add_event(self, description, date, machine_name):
        """
        הוספת אירוע חדש עם תאריך
        """
        try:
            # המרה של התאריך לפורמט תקין
            date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')

            # הוספת האירוע לזיכרון זמני
            self.cursor.execute(
                "INSERT INTO events (description, event_date, machine_name) VALUES (?, ?, ?)",
                (description, date_obj, machine_name)
            )
            # שמירה סופית במסד הנתונים
            self.conn.commit()
            print(f"האירוע נוסף בהצלחה לתאריך {date}")
        except ValueError:
            print("שגיאה: התאריך חייב להיות בפורמט YYYY-MM-DD HH:MM")

    def get_events_by_date(self, year=None, month=None, day=None, hour=None, minute=None, machine_name=None):
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

        if machine_name:
            query += " AND machine_name = ?"
            params.append(machine_name)


        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def delete_events_by_date(self, year=None, month=None, day=None, hour=None, minute=None, machine_name=None):
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

        if machine_name:
            query += " AND machine_name = ?"
            params.append(machine_name)

        self.cursor.execute(query, params)
        self.conn.commit()
        print(f"נמחקו {self.cursor.rowcount} אירועים ")
        return self.cursor.rowcount

    def retrieval_from_database(self, year=None, month=None, day=None, hour=None, minute=None, machine_name=None):
        """
        הצגת אירועים לפי תנאי תאריך וזמן
        """

        for event in self.get_events_by_date(year, month, day, hour, minute, machine_name):
            print(f" {event[0]}  |  {event[3]}  |  {event[2]}  |  {event[1]}")
        return self.get_events_by_date(year, month, day, hour, minute, machine_name)

    import requests

def get_machine_tracking_info(self):
    """
    שליפת נתונים על המחשבים המחוברים:
    - כמות המחשבים הייחודיים במסד הנתונים
    - שם כל מחשב
    - תאריך תחילת מעקב לכל מחשב
    - כמות האירועים לכל מחשב
    """
    # קבלת רשימת כל המחשבים הייחודיים
    self.cursor.execute("SELECT DISTINCT machine_name FROM events")
    machines = self.cursor.fetchall()
    num_machines = len(machines)

    # קבלת הנתונים לכל מחשב
    machine_data = {}
    for machine in machines:
        machine_name = machine[0]

        # קבלת תאריך תחילת המעקב של המחשב
        self.cursor.execute(
            "SELECT MIN(event_date) FROM events WHERE machine_name = ?",
            (machine_name,)
        )
        start_date = self.cursor.fetchone()[0]

        # קבלת כמות האירועים של המחשב
        self.cursor.execute(
            "SELECT COUNT(*) FROM events WHERE machine_name = ?",
            (machine_name,)
        )
        event_count = self.cursor.fetchone()[0]

        machine_data[machine_name] = {
            "start_date": start_date,
            "event_count": event_count
        }

    # יצירת מילון עם כל הנתונים
    data = {
        "num_machines": num_machines,
        "machine_data": machine_data
    }

    return data


    def read_file_and_import(self, filename, machine_name):
        """
        קריאת קובץ טקסט והעברת התוכן למסד הנתונים
        הקובץ צריך להיות בפורמט:
        תאריך (שורה ראשונה)
        תוכן (שורה שנייה)
        תאריך (שורה שלישית)
        תוכן (שורה רביעית)
        וכו'
        """
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # בדיקה שיש מספיק שורות
            if len(lines) < 2:
                print("הקובץ קצר מדי - נדרשות לפחות שתי שורות")
                return
            # הוספת האירועים למסד הנתונים
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):  # בדיקה שיש זוג שורות
                    date = Encryptor.decrypt_text(lines[i])
                    content = Encryptor.decrypt_text(lines[i + 1])
                    self.add_event(content, date, machine_name)



# דוגמת שימוש
if __name__ == '__main__':
    # יצירת קישור למסד הנתונים
    with DataBase() as d:
        # d.delete_events_by_date()
        # d.read_file_and_import("data2.txt")
        # d.retrieval_from_database()
        # d.delete_events_by_date(machine_name="zzz")
        c = d.retrieval_from_database(minute=42)
        print(c)
        # from KeyboardParser import KeyboardParser
        # for i in c:
        #     # print(i)
        #     print(KeyboardParser(i[1]).format_as_text())


