import requests
from iwriter import IWriter

class NetworkWriter(IWriter):

    def __init__(self):
        self.path = 'http://localhost:5000/upload'

    def send_data(self, data: str = None, machine_name: str="machine_id") -> None:
        """
        פונקציה ששולחת קובץ TXT לשרת
        :param data:
        :param file_path: נתיב הקובץ המקורי
        :return: תשובה מהשרת
        """
        try:
            # פתיחת הקובץ במצב קריאה בינארי
            with open(IWriter.file_path, 'rb') as file:
                #  יוצר מבנה מיוחד שמתאים לשליחת קבצים
                files = {'file': file}

                # שליחת הבקשה לשרת
                response = requests.post(self.path ,
                                         files=files,
                                         json={"computer_name_&_device_id": machine_name})

                # בדיקה האם הבקשה הצליחה
                if response.status_code == 200:
                    print(response.json())
                else:
                    print({'error': 'שגיאה בשליחת הקובץ'})

        except FileNotFoundError:
            print({'error': 'הקובץ לא נמצא'})
        except Exception as e:
            print({'error': f'שגיאה: {str(e)}'})

if __name__ == '__main__':
    response = NetworkWriter().send_data()
    print(response)
