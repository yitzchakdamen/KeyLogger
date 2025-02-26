import requests

class Client:

    def __init__(self,machine_name=None, year=None, month=None, day=None, hour=None, minute=None):
        self.path = 'http://localhost:5000/'
        self.params = {
            "computer_name_device_id": machine_name,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute
        }

    def get_data(self):
        # שליחת הבקשה לשרת
        response = requests.get(f"{self.path}get_data", params =self.params)
        # בדיקה האם הבקשה הצליחה
        if response.status_code == 200:
            for event in response.json():
                print(f"|  {event["machine_name"]}  |  {event["date"]}  |")
                print(f"|  {event["data"]}  |")
        else:
            print(response.text)

    def delete_data(self):
        # שליחת הבקשה לשרת
        response = requests.get(f"{self.path}delete_data", params =self.params)
        # בדיקה האם הבקשה הצליחה
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)

    def get_info(self):
        # שליחת הבקשה לשרת
        response = requests.get(f"{self.path}get_info", params =self.params)
        # בדיקה האם הבקשה הצליחה
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print(response.text)




if __name__ == '__main__':
    Client(minute=41).delete_data()
    Client(minute=41).get_data()
    r = Client().get_info()







