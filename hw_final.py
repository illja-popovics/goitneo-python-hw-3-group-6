from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value.isalpha() or len(value) < 2:
            raise ValueError("Name should only contain alphabetic characters and have at least 2 characters.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday should be in the format DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "Not specified"
        return f"Contact name: {self.name.value}, phones: {phone_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.now().date()
        birthdays_per_week = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Next Monday": [],
        }

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                delta_days = (birthday_date - today).days

                if 0 <= delta_days < 7:
                    day_of_week = (today + timedelta(days=delta_days)).strftime("%A")
                    if day_of_week in ["Saturday", "Sunday"]:
                        birthdays_per_week["Next Monday"].append(record.name.value)
                    else:
                        birthdays_per_week[day_of_week].append(record.name.value)

        return birthdays_per_week

def input_error(func): #decorator to handle exceptions
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input. Please provide the required information."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def handle_add(args, book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "Invalid input. Please provide a name and a phone number."

@input_error
def handle_change(args, book):
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return "Contact updated."
        else:
            return "Contact not found."
    else:
        return "Invalid input. Please provide a name and a new phone number."

@input_error
def handle_phone(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record:
            return record.phones[0].value
        else:
            return "Contact not found."
    else:
        return "Invalid input. Please provide a name."

@input_error
def handle_all(book):
    contacts_info = []
    for record in book.data.values():
        contacts_info.append(str(record))
    return contacts_info

@input_error
def handle_add_birthday(args, book):
    if len(args) == 2:
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        else:
            return "Contact not found."
    else:
        return "Invalid input. Please provide a name and a birthday (DD.MM.YYYY)."

@input_error
def handle_show_birthday(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record and record.birthday:
            return record.birthday.value
        else:
            return "Contact not found or birthday not specified."
    else:
        return "Invalid input. Please provide a name."

@input_error
def handle_birthdays(book):
    birthdays = book.get_birthdays_per_week()
    birthday_messages = []
    for day, names in birthdays.items():
        if names:
            birthday_messages.append(f"Next {day}: {', '.join(names)}")
    return birthday_messages

def handle_help():
    return "Available commands: add, change, phone, all, add-birthday, show-birthday, birthdays, hello, close, exit"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(handle_add(args, book))
        elif command == "change":
            print(handle_change(args, book))
        elif command == "phone":
            print(handle_phone(args, book))
        elif command == "all":
            contacts_info = handle_all(book)
            for info in contacts_info:
                print(info)
        elif command == "add-birthday":
            print(handle_add_birthday(args, book))
        elif command == "show-birthday":
            print(handle_show_birthday(args, book))
        elif command == "birthdays":
            birthday_messages = handle_birthdays(book)
            for message in birthday_messages:
                print(message)
        elif command == "help":
            print(handle_help())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
