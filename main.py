import hashlib
import json
from getpass import getpass

class AccountManager:
    def __init__(self, fn, seed='ABC', count=10):
        self.fn = fn
        self.__seed = seed
        self.__hash_count = count

    
    def __get_hash(self, text):
        text += self.__seed

        for _ in range(self.__hash_count):
            text = hashlib.sha256(text.encode()).hexdigest()
        return text


    def __check_hash(self, _hash, query):
        return _hash == self.__get_hash(query)


    def __add_data(self, data):
        with open(self.fn, 'a+', encoding="utf-8") as file:
            file.seek(0)
            if file.read():
                file.seek(0)
                new_data = json.loads(file.read())
                if new_data.get(data[0]):
                    new_data[data[0]].update(data[1])
                else:
                    new_data.update({data[0]: data[1]})

            else:
                new_data = {data[0]: data[1]}
            
            file.seek(0)
            file.truncate(0)
            json.dump(new_data, file, indent=4, ensure_ascii=False)
        return True


    def add_account(self):
        site = input("Please enter site: ")
        email = input("Enter account login(email, username): ")
        password = getpass("Password: ")
        password = self.__get_hash(password)

        data = [site, {email: password}]
        return self.__add_data(data)

    
    def get_account(self):
        with open(self.fn, 'r', encoding="utf-8") as file:
            data = json.loads(file.read())

        site = input("\nPlease enter site: ")
        email = input("Login(email, username): ")
        if data.get(site).get(email):
            while True:
                query = getpass("Password: ")
                if self.__check_hash(data.get(site).get(email), query):
                    print(query)
                    break
                print("Invalid Password")
        else:
            return "Invalid username"


am = AccountManager("db.json")
am.add_account()
am.get_account()
