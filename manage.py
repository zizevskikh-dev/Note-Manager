import argparse
from views import NoteManager


if __name__ == "__main__":
    user = NoteManager()
    parser = argparse.ArgumentParser(
        prog="Note Manager CLI App",
        usage="[-c | -create] [-r | -read] [-u | -upd] [-d | -del] [-f | -find] [-s | - show] [-clear]",
        description="This app can help you create and manage your notes via next options",
        epilog="""
Enjoy the Note Manager experience ❤ ❤ ❤ !
You can see more information and examples in 'README.md' or GitHub:
https://github.com/howmuchisthe-fish/Note-Manager.git
Note Manager ver.1.0.0
Created by Aleksander Zizevskikh, 2024
Email: zizevskikh.dev@gmail.com""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Commands
    parser.add_argument(
        "-c",
        "-create",
        "--create_note",
        action="store_true",
        help="""Create the note in the database by following additional arguments:
[--cat] Add the number of transaction category to the new note:
    --cat 1 = "waste"
    --cat 2 = "income"
[--amt] Add a positive amount of money to the new note
        
Optional argument:
[--desc] Add a description to the new note""",
    )
    parser.add_argument(
        "-r",
        "-read",
        "--read_notes",
        action="store_true",
        help="""Show note(-s) from the database:
Doesn't require any additional arguments""",
    )
    parser.add_argument(
        "-u",
        "-upd",
        "--update_note",
        action="store_true",
        help="""Update the note from the database by following additional arguments:
[--date] Add the previous date to the note you want to update
[--cat] Add the previous number of transaction category to the note you want to update:
    --cat 1 = "waste"
    --cat 2 = "income"
[--amt] Add the previous positive amount of money to the note you want to update
[--decs] Add the previous description to the note you want to update ***
    *** Skip this argument if an updated note doesn't have any description!
[--newcat] Add a new number of transaction category to the note you want to update:
    --newcat 1 = "waste"
    --newcat 2 = "income"
[--newamt] Add a new positive amount of money to the note you want to update
        
Optional argument:
[--newdesc] Add a new description to the note you want to update""",
    )
    parser.add_argument(
        "-d",
        "-del",
        "--delete_note",
        action="store_true",
        help="""Delete the note from the database by following additional arguments:
[--date] Add a date to the note you want to delete
[--cat] Add a number of transaction category to the note you want to delete:
    --cat 1 = "waste"
    --cat 2 = "income"
[--amt] Add a positive amount of money to the note you want to delete
[--desc] Add a description to the note you want to delete ***
    *** Skip this argument if the deleted note doesn't have any description!""",
    )
    parser.add_argument(
        "-f",
        "-find",
        "--find_notes",
        action="store_true",
        help="""Find a note(-s) from the database by following additional arguments:
[--date] Add a date to the note(-s) you want to find
[--cat] Add a number of transaction category to the note(-s) you want to find:
    --cat 1 = "waste"
    --cat 2 = "income"
[--amt] Add a positive amount of money to the note(-s) you want to find

*** Searching by [--desc] can be included into the next version of this app 🤙""",
    )
    parser.add_argument(
        "-s",
        "-show",
        "--show_balance",
        action="store_true",
        help="""Show your current balance
Doesn't require any additional argument""",
    )
    parser.add_argument(
        "-clear",
        "--clear_notes",
        action="store_true",
        help="""Clear all notes from the database
Doesn't require any additional argument""",
    )

    # Arguments
    group_args = parser.add_argument_group("Arguments")
    group_args.add_argument(
        "--date",
        type=str,
        help="""Note date, format:
    --date yyyy-mm-dd
Like:
    --date 1943-04-19""",
    )
    group_args.add_argument(
        "--cat",
        choices=["1", "2"],
        help="""Note transaction category 
There are only 2 options:
    --cat 1 (for "waste")
    --cat 2 (for "income")""",
    )
    group_args.add_argument(
        "--amt",
        type=float,
        help="""Note amount of money [positive int|float]
Like:
    --amt 42""",
    )
    group_args.add_argument(
        "--desc",
        default="",
        nargs="+",
        help="""Note description
Like:
    --desc Spice must flow""",
    )
    group_args.add_argument(
        "--newcat",
        choices=["1", "2"],
        help="""New note transaction category (only for the update)
There are only 2 options:
    --newcat 1 (for "waste")
    --newcat 2 (for "income")""",
    )
    group_args.add_argument(
        "--newamt",
        type=float,
        help="""New note amount of money (only for the update) [positive int|float]
Like:
    --newamt 34.69""",
    )
    group_args.add_argument(
        "--newdesc",
        default="",
        nargs="+",
        help="""New note description (only for the update)
Like:
    --newdesc Beautiful is better than ugly""",
    )

    args = parser.parse_args()
    if args.create_note:
        user.create_note(cat=args.cat, amt=args.amt, desc=args.desc)
    if args.read_notes:
        user.read_notes()
    if args.update_note:
        user.update_note(
            pr_date=args.date,
            pr_cat=args.cat,
            pr_amt=args.amt,
            pr_desc=args.desc,
            new_cat=args.newcat,
            new_amt=args.newamt,
            new_desc=args.newdesc,
        )
    if args.delete_note:
        user.delete_note(
            date=args.date,
            cat=args.cat,
            amt=args.amt,
            desc=args.desc,
        )
    if args.find_notes:
        user.find_notes(date=args.date, cat=args.cat, amt=args.amt)
    if args.show_balance:
        user.show_balance()
    if args.clear_notes:
        user.clear_notes()
