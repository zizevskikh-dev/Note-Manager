import datetime
import json
import os
from typing import Union, Literal


class NoteManager:
    """
    View for the CLI Note Manager.
    Provide CRUD commands, and several addition functions:
        - Find the record(-s) from the database by the parameters;
        - Display current amount of money;
        - Delete all the records from the database;
        - Create automatically a text file 'db.txt' with all records from the database, when you:
            * create record;
            * update record;
            * delete record.
    """

    def __init__(self):
        self.__balance = self.get_current_balance()

    def create_note(
            self,
            cat: Literal["1", "2"],
            amt: float,
            desc: Union[list, Literal[""]]
    ) -> None:
        """
        Create a new record in the database.
        Display a new record.

        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description, defaults to ""
        """

        if not cat or not amt:
            print("You need to add all the required arguments to create a note", end="\n\n")
            return

        if amt < 0:
            print("The amount of money must be a positive number", end="\n\n")
            return

        db_data, notes_amt = self.get_db_data_and_notes_amt()
        cat, amt, desc = self.prepare_cat_amt_desc(cat=cat, amt=amt, desc=desc)
        note_new = self.create_note_template(cat=cat, amt=amt, desc=desc)
        db_data["notes"].append(note_new)
        self.update_db(db_data=db_data)

        print("The new note has been created!", end="\n\n")
        print("-" * 40)
        print("Created note:")
        print("-" * 40)
        self.print_notes(notes_lst=[note_new])

        if notes_amt == 0:
            self.create_or_update_text_document(action_text="create")
        else:
            self.create_or_update_text_document()

    def read_notes(self) -> None:
        """Display all the records from the database."""

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt > 0:
            print("-" * 40)
            print(f"Database contains {notes_amt} note(-s):")
            print("-" * 40, end="\n\n")
            self.print_notes(notes_lst=db_data["notes"])
        else:
            print("Can't show all notes because of the empty database", end="\n\n")

    def update_note(
            self,
            date_prev: str,
            cat_prev: Literal["1", "2"],
            amt_prev: float,
            desc_prev: Union[list, Literal[""]],
            cat_new: Literal["1", "2"],
            amt_new: float,
            desc_new: Union[list, Literal[""]]
    ) -> None:
        """
        Update an existing record with the new one and write it into the database.
        Display the previous and the updated versions of the record.

        :param date_prev: A previous date
        :param cat_prev: A previous transaction category
        :param amt_prev: A previous amount of money
        :param cat_new: A new transaction category
        :param amt_new: A new amount of money
        :param desc_prev: A previous description, default to ""
        :param desc_new: A new description, default to ""
        """

        if (
                not date_prev
                or not cat_prev
                or not amt_prev
                or not cat_new
                or not amt_new
        ):
            print("You need to add all the required arguments to update the note", end="\n\n")
            return

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt == 0:
            print("Can't update the note(-s) because of the empty database", end="\n\n")
            return

        if not self.check_date(date=date_prev):
            return

        if amt_prev < 0 or amt_new < 0:
            print("The amount of money must be a positive number", end="\n\n")
            return

        cat_prev, amt_prev, desc_prev = self.prepare_cat_amt_desc(cat=cat_prev, amt=amt_prev, desc=desc_prev)
        cat_new, amt_new, desc_new = self.prepare_cat_amt_desc(cat=cat_new, amt=amt_new, desc=desc_new)

        note_found, note_found_index = self.filter_records(
            db_data=db_data,
            date=date_prev,
            cat=cat_prev,
            amt=amt_prev,
            desc=desc_prev,
            action="update"
        )

        if note_found:
            note_new = self.create_note_template(cat=cat_new, amt=amt_new, desc=desc_new)
            db_data["notes"][note_found_index] = note_new
            self.update_db(db_data=db_data)

            print("The update finished successfully!", end="\n\n")
            print("-" * 40)
            print("Before the update:")
            print("-" * 40)
            self.print_notes(notes_lst=[note_found])
            print("-" * 40)
            print("After the update:")
            print("-" * 40)
            self.print_notes(notes_lst=[note_new])
            self.create_or_update_text_document(action_text="update")

    def delete_note(
            self,
            date: str,
            cat: Literal["1", "2"],
            amt: float,
            desc: Union[list, Literal[""]]
    ) -> None:
        """
        Delete a record from the database.
        Display the deleted record.

        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description, defaults to ""
        """

        if not date or not cat or not amt:
            print("You need to add all the required arguments to delete the note", end="\n\n")
            return

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt == 0:
            print("Can't delete the note(-s) because of the empty database", end="\n\n")
            return

        if not self.check_date(date=date):
            return

        if amt < 0:
            print("The amount of money must be a positive number", end="\n\n")
            return

        cat, amt, desc = self.prepare_cat_amt_desc(cat, amt, desc)

        note_found = self.filter_records(
            db_data=db_data,
            date=date,
            cat=cat,
            amt=amt,
            desc=desc,
            action="delete"
        )

        if note_found:
            note_deleted, note_deleted_index = note_found[0], note_found[1]
            del db_data["notes"][note_deleted_index]
            self.update_db(db_data=db_data)

            print("The note has been deleted successfully!", end="\n\n")
            print("-" * 40)
            print("Deleted note:")
            print("-" * 40)
            self.print_notes(notes_lst=[note_deleted])

            notes_amt = self.get_db_data_and_notes_amt()[1]
            if notes_amt == 0:
                print("*" * 40)
                print("Database is empty!")
                self.delete_text_document()
            else:
                self.create_or_update_text_document(action_text="update")

    def find_notes(
            self,
            date: Union[str, None],
            cat: Union[Literal["1", "2"], None],
            amt: Union[float, None]
    ) -> None:
        """
        Find the record(-s) from the database by the next parameters.
        Display the found record(-s).

        :param date: Record date
        :param cat: Record transaction category
        :param amt: Record amount of money
        """

        if not date and not cat and not amt:
            print("You need to add at least one required argument to filter the notes", end="\n\n")
            return

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt == 0:
            print("Can't find the note(-s) because of the empty database", end="\n\n")
            return

        note_found = []
        is_multiple_search = False

        if date:
            if not self.check_date(date=date):
                return

            note_found = [note for note in db_data["notes"] if note[0]["date"] == date]
            is_multiple_search = True

        if cat:
            cat = "waste" if cat == "1" else "income"

            if is_multiple_search:
                note_found = [note for note in note_found if note[1]["category"] == cat]
                is_multiple_search = True
            else:
                note_found = [note for note in db_data["notes"] if note[1]["category"] == cat]
                is_multiple_search = True

        if amt:
            if amt < 0:
                print("The amount of money must be a positive number", end="\n\n")
                return

            if is_multiple_search:
                note_found = [note for note in note_found if abs(note[2]["amount"]) == amt]
            else:
                note_found = [note for note in db_data["notes"] if abs(note[2]["amount"]) == amt]

        if note_found:
            print("-" * 30)
            print("Search result:")
            print("-" * 30, end="\n\n")
            self.print_notes(notes_lst=note_found)
        else:
            print("No matches in your search", end="\n\n")

    def show_balance(self) -> None:
        """Display current amount of money."""

        print("-" * 40)
        print("Your current balance is: {balance:.2f}".format(balance=self.__balance))
        print("-" * 40, end="\n\n")

    def clear_notes(self) -> None:
        """
        Delete all records in the database.
        Remove "db.txt" text file.
        """

        self.add_initial_template_in_db()
        print("The notes history has been cleaned!", end="\n\n")
        self.delete_text_document()

    # DRY Methods
    def check_db_existing_or_crete_db_template(self) -> None:
        """
        Check if the database exists.
        If the database doesn't exist - create 'db.json' with the initial template.
        """

        try:
            open("db.json")
        except FileNotFoundError:
            self.add_initial_template_in_db()
            print("*" * 50)
            print("Database has been created!")
            print("*" * 50, end="\n\n")

    def get_db_data_and_notes_amt(self) -> tuple[dict, int]:
        """
        Read JSON file and deserialize a data.
        Return total amount of notes.

        :return: A tuple which contains a serialized database data and amount of notes
        """

        self.check_db_existing_or_crete_db_template()

        with open("db.json", "r") as file:
            db_data = json.load(file)
        notes_amt = len(db_data["notes"])

        return db_data, notes_amt

    def get_current_balance(self) -> float:
        """Return current amount of money"""

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt > 0:
            balance = sum(
                [
                    val
                    for note in db_data["notes"]
                    for line in note
                    for key, val in line.items()
                    if key == "amount"
                ]
            )
            return round(balance, 2)
        return 0.0

    def add_initial_template_in_db(self) -> None:
        """Add the initial template in the database."""

        initial_template = {"notes": []}
        self.update_db(db_data=initial_template)

    @staticmethod
    def update_db(db_data) -> None:
        """Update the database with a current data."""

        with open("db.json", "w") as file:
            json.dump(obj=db_data, fp=file, indent=4)

    @staticmethod
    def create_note_template(
            cat: Literal["waste", "income"],
            amt: float,
            desc: str
    ) -> list[dict[str, Union[str, float]]]:
        """
        Create a list with the record columns and their values.

        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description
        :return: Note template
        """

        date_current = str(datetime.date.today())
        template = [
            {"date": date_current},
            {"category": cat},
            {"amount": amt},
            {"description": desc},
        ]
        return template

    def create_or_update_text_document(self, action_text: Literal["create", "update"] = None) -> None:
        """Create or update 'db.txt', which contains all records from the database."""

        db_data, notes_amt = self.get_db_data_and_notes_amt()

        if notes_amt == 0:
            print("Can't create 'db.txt' because of the empty database", end="\n\n")
            return

        note_lines_lst = self.prepare_notes_to_text(notes_lst=db_data["notes"])

        with open("db.txt", "w", encoding="utf-8") as file:
            for line in note_lines_lst:
                if line.startswith("Description"):
                    file.write("".join([line, "\n\n"]))
                else:
                    file.write("".join([line, "\n"]))

            file.write("".join([("-" * 30), "\n"]))
            self.__balance = self.get_current_balance()
            file.write("".join(["Current balance is: {balance:.2f}".format(balance=self.__balance), "\n"]))

        if action_text:
            print("*" * 40)
            print(f'File "db.txt" has been {action_text}d!')
            print("*" * 40, end="\n\n")

    @staticmethod
    def delete_text_document() -> None:
        """Delete text file 'db.txt'."""

        try:
            os.remove("db.txt")
        except FileNotFoundError:
            pass
        else:
            print("*" * 40)
            print('File "db.txt" has been deleted!')
            print("*" * 40, end="\n\n")

    def print_notes(self, notes_lst: list) -> None:
        """
        Display note(-s).

        :param notes_lst: A list with the note(-s)
        """

        note_lines_lst = self.prepare_notes_to_text(notes_lst=notes_lst)

        for line in note_lines_lst:
            if line.startswith("Description"):
                print(line, end="\n\n")
            else:
                print(line)

    @staticmethod
    def check_date(date: str) -> bool:
        """
        Check a value of an argument [--data] from the CLI.

        :param date: Record date
        :return: Result of check
        """

        try:
            datetime.date.fromisoformat(date)
            return True
        except ValueError as error:
            print(error, end="\n\n")
            return False

    @staticmethod
    def prepare_cat_amt_desc(
            cat: Literal["1", "2"],
            amt: float,
            desc: Union[list, Literal[""]]
    ) -> tuple:
        """
        Change category value to a string view.
        If the description was sent - change the description type from list to str.

        :param cat: Record transaction category
        :param amt: Record amount of money
        :param desc: Record description
        :return: Return a tuple (cat, amt, desc) after transformation
        """

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
            cat: Literal["waste", "income"],
            amt: float,
            desc: str,
            action: str
    ) -> Union[tuple[list, int], None]:
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
        if not data_filtered:
            print(f'No matches with previous date "{date}" to {action}', end="\n\n")
            return

        data_filtered = [note for note in data_filtered if note[1]["category"] == cat]
        if not data_filtered:
            print(f'No matches with category "{cat}" to {action}', end="\n\n")
            return

        data_filtered = [note for note in data_filtered if note[2]["amount"] == amt]
        if not data_filtered:
            print(f'No matches with amount "{amt}" to {action}', end="\n\n")
            return

        data_filtered = [note for note in data_filtered if note[3]["description"] == desc]
        if not data_filtered:
            if not desc:
                print(f'No matches with the empty description to {action}')
            else:
                print(f'No matches with the description "{desc}" to {action}')
            return

        if data_filtered:
            note_found = data_filtered[0]
            note_found_index = db_data["notes"].index(note_found)
            return note_found, note_found_index

    @staticmethod
    def prepare_notes_to_text(notes_lst: list) -> list[str]:
        """
        Transform record content to 'str' type.

        :param notes_lst: A list with the notes from the database
        :return: A list witch contains note columns and their values in 'str' type
        """

        note_lines_lst = [
            f"{list(line.keys())[0].capitalize()}: {list(line.values())[0]}"
            for note in notes_lst
            for line in note
        ]

        return note_lines_lst
