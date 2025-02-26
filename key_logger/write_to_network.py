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
        if self.full_file_check():
            try:
                # פתיחת הקובץ במצב קריאה בינארי
                with open(IWriter.file_path, 'rb') as file:
                    #  יוצר מבנה מיוחד שמתאים לשליחת קבצים
                    files = {'file': file}
                    data = {"computer_name_device_id": machine_name}
                    # שליחת הבקשה לשרת
                    response = requests.post(self.path ,
                                             files=files,
                                             data=data)
                    # בדיקה האם הבקשה הצליחה
                    if response.status_code == 200:
                        print(response.json())
                    else:
                        print(response.text)
                        print({'error': 'שגיאה בשליחת הקובץ'})

            except FileNotFoundError:
                print({'error': 'הקובץ לא נמצא'})
            except Exception as e:
                print({'error': f'שגיאה: {str(e)}'})

    def full_file_check(self):
        try:
            with open(IWriter.file_path, 'r') as file:
                 if len(file.readline()) > 0:
                     return True
        except FileNotFoundError:
            print({'error': 'הקובץ לא נמצא'})
        except Exception as e:
            print({'error': f'שגיאה: {str(e)}'})


if __name__ == '__main__':
    # response = NetworkWriter().send_data(machine_name="qaqsa_55478844")
    response = NetworkWriter().send_data(machine_name="zzz")
    print(response)
