from iwriter import IWriter


class FileWriter(IWriter):

    def send_data(self, data: str, machine_name: str = None):
        with open(IWriter.file_path, "a") as file:
            file.write(f"{data}\n") #repr
        print("הקובץ עודכן בהצלחה!")

    def deleting_contents(self):
        with open(self.file_path, "w") as file:
            file.write("")
        print("תוכן ההקובץ נמחק בהצלחה!")


if __name__ == "__main__":
    d = FileWriter()
    d.deleting_contents()
    d.send_data("היי מה נשמע", "Machine1")
    d.send_data("הכול טוב", "Machine1")
    d.send_data("מושלם", "Machine1")




