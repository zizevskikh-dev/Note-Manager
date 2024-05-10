from typing import Union, Literal
import os
import json
import datetime


class NoteManager:
    """
    View for the CLI Note Manager.
    Provide CRUD commands, and several addition functions:
        - Find the record(-s) from the database by the parameters;
        - Display current amount of money;
        - Delete all the records from the database;
        - Create automatically a text file 'db.txt' with all records from the database, when you:
            - create record
            - update record
            - delete record
    """

    def __init__(self):
        self.__balance = self.get_current_balance()

    # Command methods
    def create_note(self, cat: Literal["1", "2"], amt: float, desc: Union[list, None] = "") -> None:
        """
        Create a new record in the database.
        Display a new record.

        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description, defaults to ""
        :return: A new database record
        """

        if cat is None or amt is None:
            print("You need to add all the required arguments to filter notes", end="\n\n")
            return
        cat, amt, desc = self.check_cat_amt_desc(cat=cat, amt=amt, desc=desc)
        if not amt:
            return
        date_current = str(datetime.date.today())
        note = self.create_note_template(date=date_current, cat=cat, amt=amt, desc=desc)
        db_data, is_record_first = self.check_db_data()
        db_data["notes"].append(note)
        self.write_db(db_data=db_data)

        print("The new note has been created!", end="\n\n")
        print("-" * 40)
        print("Created note:")
        print("-" * 40)
        self.print_notes([note])

        if not is_record_first:
            self.create_text_document(action="create")
        else:
            self.create_text_document(action=False)

    def read_notes(self) -> None:
        """
        Display all the records from the database.
        """

        db_data, check_db = self.check_db_data()
        if not check_db:
            print("Can't show all notes because of the empty database", end="\n\n")
            return
        print("-" * 40)
        print("All of your notes:")
        print("-" * 40, end="\n\n")
        self.print_notes(db_data["notes"])

    def update_note(
            self,
            pr_date: str,
            pr_cat: Literal["1", "2"],
            pr_amt: float,
            new_cat: Literal["1", "2"],
            new_amt: float,
            pr_desc: Union[list, None] = "",
            new_desc: Union[list, None] = ""
    ) -> None:
        """
        Update an existing record with the new one and write it into the database.
        Display the previous and the updated versions of the record.

        :param pr_date: A previous date
        :param pr_cat: A previous transaction category
        :param pr_amt: A previous amount of money
        :param new_cat: A new transaction category
        :param new_amt: A new amount of money
        :param pr_desc: A previous description, default to ""
        :param new_desc: A new description, default to ""
        :return: An updated record in the database
        """

        if (
            pr_date is None
            or pr_cat is None
            or pr_amt is None
            or new_cat is None
            or new_amt is None
        ):
            print("You need to add all the required arguments to update the note", end="\n\n")
            return

        db_data, check_db = self.check_db_data()
        if not check_db:
            print("Can't update the note(-s) because of the empty database", end="\n\n")
            return

        if not self.check_date(date=pr_date):
            return
        pr_cat, pr_amt, pr_desc = self.check_cat_amt_desc(cat=pr_cat, amt=pr_amt, desc=pr_desc)
        if not pr_amt:
            return
        new_cat, new_amt, new_desc = self.check_cat_amt_desc(cat=new_cat, amt=new_amt, desc=new_desc)
        if not pr_amt:
            return
        date_current = str(datetime.date.today())

        matches = self.filter_records(
            db_data=db_data,
            date=pr_date,
            cat=pr_cat,
            amt=pr_amt,
            desc=pr_desc,
            action="update"
        )
        if matches is not None:
            data_filtered, note_index = matches[0], matches[1]
        else:
            return

        note_new = self.create_note_template(date=date_current, cat=new_cat, amt=new_amt, desc=new_desc)
        db_data["notes"][note_index] = note_new
        self.write_db(db_data=db_data)

        print("The update finished successfully!", end="\n\n")
        print("-" * 40)
        print("Before the update:")
        print("-" * 40)
        self.print_notes(data=[data_filtered])
        print("-" * 40)
        print("After the update:")
        print("-" * 40)
        self.print_notes(data=[note_new])
        self.create_text_document(action="update")

    def delete_note(self, date: str, cat: Literal["1", "2"], amt: float, desc: Union[list, None] = "") -> None:
        """
        Delete a record from the database.
        Display the deleted record.

        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description, defaults to ""
        :return: A list of records in the database, except for the deleted record
        """

        if date is None or cat is None or amt is None:
            print("You need to add all the required arguments to delete the note", end="\n\n")
            return

        db_data, check_db = self.check_db_data()
        if not check_db:
            print("Can't delete the note(-s) because of the empty database", end="\n\n")
            return

        if not self.check_date(date=date):
            return
        cat, amt, desc = self.check_cat_amt_desc(cat, amt, desc)
        if not amt:
            return
        matches = self.filter_records(db_data=db_data, date=date, cat=cat, amt=amt, desc=desc, action="delete")
        if matches is not None:
            data_filtered, note_index = matches[0], matches[1]
        else:
            return
        del db_data["notes"][note_index]
        self.write_db(db_data=db_data)

        print("The note has been deleted successfully!", end="\n\n")
        print("-" * 40)
        print("Deleted note:")
        print("-" * 40)
        self.print_notes(data=[data_filtered])

        check_db = self.check_db_data()[1]
        if not check_db:
            print("*" * 40)
            print("Database is empty!")
            self.delete_text_document()
        else:
            self.create_text_document(action=False)

    def find_notes(self, date: str, cat: Literal["1", "2"], amt: float) -> None:
        """
        Find the record(-s) from the database by the next parameters.
        Display the found record(-s).

        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        """

        if date is None and cat is None and amt is None:
            print("You need to add at least one required argument to filter the notes", end="\n\n")
            return

        db_data, check_db = self.check_db_data()
        if not check_db:
            print("Can't find the note(-s) because of the empty database", end="\n\n")
            return

        data_filtered = []
        is_multiple_search = False
        if date:
            if not self.check_date(date=date):
                return
            data_filtered = [
                note for note in db_data["notes"] if note[0]["date"] == date
            ]
            is_multiple_search = True
        if cat:
            cat = "waste" if cat == "1" else "income"

            if is_multiple_search:
                data_filtered = [
                    note for note in data_filtered if note[1]["category"] == cat
                ]
            else:
                data_filtered = [
                    note for note in db_data["notes"] if note[1]["category"] == cat
                ]
                is_multiple_search = True
        if amt:
            if is_multiple_search:
                data_filtered = [
                    note for note in data_filtered if abs(note[2]["amount"]) == amt
                ]
            else:
                data_filtered = [
                    note
                    for note in db_data["notes"]
                    if abs(note[2]["amount"]) == amt
                ]

        if data_filtered:
            print("-" * 30)
            print("Search result:")
            print("-" * 30, end="\n\n")
            self.print_notes(data=data_filtered)
        else:
            print("No matches in your search", end="\n\n")

    def show_balance(self) -> None:
        """
        Display current amount of money.
        """

        print("-" * 40)
        print("Your current balance is: {balance:.2f}".format(balance=self.__balance))
        print("-" * 40, end="\n\n")

    def clear_notes(self) -> None:
        """
        Delete all the records in the database.
        Also, clear "db.txt" text file.

        :return: An empty database template
        """

        self.write_db_template()
        print("The notes history has been cleaned!", end="\n\n")
        self.delete_text_document()

    # DRY Methods
    def check_db_existing_or_crete_db_template(self) -> None:
        """
        Check if the database exists.
        If the database doesn't exist - create 'db.json'.

        :return: The new database with the template | Nothing
        """

        try:
            open("db.json")
        except FileNotFoundError:
            self.write_db_template()
            print("*" * 50)
            print("Database has been created!")
            print("*" * 50, end="\n\n")

    def write_db_template(self) -> None:
        """
        Write a template in the database.

        :return: Database with the template
        """

        template_data = {"notes": []}
        self.write_db(db_data=template_data)

    @staticmethod
    def write_db(db_data) -> None:
        """
        Write records in the database.

        :return: A database with the records
        """

        with open("db.json", "w") as file:
            json.dump(obj=db_data, fp=file, indent=4)

    @staticmethod
    def create_note_template(
            date: str,
            cat: Literal["waste", "income"],
            amt: float,
            desc: str
    ) -> list[dict[str, Union[str, float]]]:
        """
        Create a list with the record.

        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description
        :return: A list with the dicts
        """

        template = [
            {"date": date},
            {"category": cat},
            {"amount": amt},
            {"description": desc},
        ]
        return template

    def deserialize_db(self) -> dict[Literal["notes"], list]:
        """
        Read JSON file and deserialize a data.

        :return: A dict with records
        """

        self.check_db_existing_or_crete_db_template()
        with open("db.json", "r") as file:
            data = json.load(file)
        return data

    def create_text_document(self, action: Union[bool, str]) -> None:
        """
        Create a text file 'db.txt' containing all the records from the database.

        :return: File 'db.txt' in the project directory
        """

        db_data, check_db = self.check_db_data()
        if not check_db:
            print("Can't create 'db.txt' because of the empty database", end="\n\n")
            return
        lines_array = self.parse_db(data=db_data["notes"])

        with open("db.txt", "w", encoding="utf-8") as file:
            for i_num, line in enumerate(lines_array):
                if line.startswith("Description"):
                    file.write("".join([line, "\n\n"]))
                else:
                    file.write("".join([line, "\n"]))
            file.write("".join([("-" * 30), "\n"]))
            self.__balance = self.get_current_balance()
            file.write("".join(["Current balance is: {balance:.2f}".format(balance=self.__balance), "\n"]))

        if action:
            print("*" * 40)
            print(f'File "db.txt" has been {action}d!')
            print("*" * 40, end="\n\n")

    @staticmethod
    def delete_text_document() -> None:
        """
        Delete text file 'db.txt'.
        """

        try:
            os.remove("db.txt")
        except FileNotFoundError:
            pass
        else:
            print("*" * 40)
            print('File "db.txt" has been deleted!')
            print("*" * 40, end="\n\n")

    def check_db_data(self) -> type[dict, bool]:
        """
        Check note(-s) existing.
        Returns record if they exist.

        :return: A dict with the records and bool result of check
        """

        db_data = self.deserialize_db()
        check_db = True if len(db_data["notes"]) > 0 else False
        return db_data, check_db

    @staticmethod
    def check_date(date: str) -> bool:
        """
        Check a value of an argument [--data] from the CLI.

        :param date: Record date
        :return: Bool result of check
        """

        try:
            datetime.date.fromisoformat(date)
            return True
        except ValueError as error:
            print(error, end="\n\n")
            return False

    @staticmethod
    def check_cat_amt_desc(
            cat: Literal["1", "2"],
            amt: float,
            desc: Union[list, str]
    ) -> tuple[Literal["1", "2"], bool, str] | tuple[Literal["waste", "income"], float, str]:
        """
        Check the positive number of the amount of money.
        Change category value to a string view.
        If the description was sent - change the description type from list to str.

        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description
        :return: Return a tuple (cat, amt, desc) after the check
        """

        if amt < 0:
            print("The amount of money must be a positive number", end="\n\n")
            amt = False
            return cat, amt, desc

        if cat == "1":
            amt = -amt
            cat = "waste"
        else:
            cat = "income"

        if desc:
            desc = " ".join(desc)
        return cat, amt, desc

    @staticmethod
    def filter_records(
            db_data: dict,
            date: str,
            cat: str,
            amt: float,
            desc: str,
            action: str
    ) -> Union[None, tuple[list, int]]:
        """
        Filter records by parameters.

        :param db_data: A dict with the records
        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description
        :param action: "update" | "delete"
        :return: A Matching record, and its index | None
        """

        data_filtered = [note for note in db_data["notes"] if note[0]["date"] == date]
        if data_filtered:
            data_filtered = [
                note for note in data_filtered if note[1]["category"] == cat
            ]
        else:
            print(f'No matches with previous date "{date}" to {action}', end="\n\n")
            return

        if data_filtered:
            data_filtered = [note for note in data_filtered if note[2]["amount"] == amt]
        else:
            print(f'No matches with category "{cat}" to {action}', end="\n\n")
            return

        if data_filtered:
            data_filtered = [note for note in data_filtered if note[3]["description"] == desc]
            if not data_filtered:
                print(f'No matches with description "{desc}" to {action}', end="\n\n")
                return

            data_filtered = data_filtered[0]
            note_index = db_data["notes"].index(data_filtered)
            return data_filtered, note_index
        else:
            print(f'No matches with amount "{amt}" to {action}', end="\n\n")
            return

    def get_current_balance(self) -> Union[int, float]:
        """
        Return current amount of money
        """

        db_data, check_db = self.check_db_data()
        if check_db:
            self.__balance = sum(
                [
                    val
                    for note in db_data["notes"]
                    for line in note
                    for key, val in line.items()
                    if key == "amount"
                ]
            )
            self.__balance = round(self.__balance, 2)
            return self.__balance
        return 0

    def print_notes(self, data: list) -> None:
        """
        Display note(-s).

        :param data: A list with the note(-s)
        """

        lines_array = self.parse_db(data=data)
        for line in lines_array:
            if line.startswith("Description"):
                print(line, end="\n\n")
            else:
                print(line)

    @staticmethod
    def parse_db(data: list) -> list[str]:
        """
        Transform records data to strings.

        :param data: A list with the notes
        :return: A list with the string records
        """

        lines_array = [
            f"{list(line.keys())[0].capitalize()}: {list(line.values())[0]}"
            for note in data
            for line in note
        ]
        return lines_array
