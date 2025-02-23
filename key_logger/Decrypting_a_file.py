from Encryptor import Encryptor

with open("data.txt", "r") as file:
    for line in file:
        print(Encryptor.decrypt_text(line))

with open("data2.txt", "w") as f:
    with open("data.txt", "r") as file:
        for line in file:
            f.write(f"{Encryptor.decrypt_text(line)}\n")
