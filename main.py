import hashlib
import json
from getpass import getpass

class AccountManager:
    def __init__(self, fn):
        self.fn = fn
    
    
    def __get_hash(self, text):
        text += 'Seed'
        for _ in range(5):
            text = hashlib.sha256(text.encode()).hexdigest()

        return text

    def __add_data(self, data):
        with open(self.fn, 'a+', encoding="utf-8") as file:
            file.seek(0)
            if file.read():
                file.seek(0)
                data = data | json.loads(file.read())
            
            file.truncate(0)
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

    def add_account(self):
        email = input("Enter account login(email, username): ")
        password = getpass("Password: ")

        password = self.__get_hash(password)

        data = {email: password}

        return self.__add_data(data)

    
    def get_account(self):
        with open(self.fn, 'r', encoding="utf-8") as file:
            data = json.loads(file.read())

        email = input("\nLogin(email, username): ")
        if data.get(email, None):
            while True:
                query = getpass("Password: ")
                if self.__get_hash(query) == data.get(email):
                    print(query)
                    break
        else:
            return "Invalid username"


am = AccountManager("db.json")
am.add_account()
am.get_account()
