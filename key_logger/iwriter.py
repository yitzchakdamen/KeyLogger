from abc import ABC, abstractmethod

class IWriter(ABC):

    file_path = "data.txt"

    @abstractmethod
    def send_data(self, data: str, machine_name: str) -> None:
        pass

