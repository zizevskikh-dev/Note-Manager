# Note Manager CLI App
## The app can help you create and manage notes with your transactions via CLI

---
## The database includes next columns for each note:
- `Date` - Date when a note was created | updated, **created automatically**
- `Category` - Transaction category:
  - `waste`  -  leads to a reduction in your balance *(changes* `Amount` *to a negative number)*
  - `income` - leads to an increase in your balance
- `Amount` - Note amount of money
- `Description` - Note description*(optional column)*

---
> First run creates the database `db.json` with the note template **automatically**
> ```c
> > python manage.py 
> or
> > python manage.py [plus any supported command]
>```
>
> Template content in `db.json`:
> ``` JS
> {
>     "notes": [] 
> }
> ```

---
## Note Manager supports typical CRUD commands, and several addition functions:
### 0. Help `-h | --help`
```C
> python manage.py -h
... Display the list of supported commands and their description:
```

---
### 1. Create a new record `-c | -create`
#### Create a note in the database by following additional arguments:
`--cat` Add a number of transaction category to the new note:
  - `--cat 1` = "waste"
  - `--cat 2` = "income"
 
 `--amt`  Add a positive amount of money to the new note.
* If the number of transaction category is `"waste"`, the amount of money will change to a negative number **automatically.**

*Optional argument:*  
`--desc` Add a description to the new note.
> **The order of arguments doesn't play any role.**
#### Example:
```C
> python manage.py -create --amt 34.69 --cat 2 --desc Cashback 
The new note has been created!

----------------------------------------
Created note:
----------------------------------------
Date: 2024-05-09
Category: income
Amount: 34.69
Description: Cashback

****************************************
File "db.txt" has been created!
****************************************
```
#### `db.json` template content:
```JS
{  
    "notes": [  
        [  
            {  
                "date": "2024-05-09"  
            },  
            {  
                "category": "income"  
            },  
            {  
                "amount": 34.69  
            },  
            {  
                "description": "Cashback"  
            }  
        ]  
    ]  
}
```
#### The creation of the first note also leads to the creation of `db.txt` file:

```
Date: 2024-05-09  
Category: income  
Amount: 34.69  
Description: Cashback  
  
------------------------------  
Current balance is: 34.69
```

---
### 2. Display all notes `-r | -read`
> **Doesn't require any additional arguments.**
#### Example:
```c
> python manage.py -read                                 
----------------------------------------
All of your notes:
----------------------------------------

Date: 2024-05-09
Category: income
Amount: 34.69
Description: Cashback

```

---
### 3. Update the note `-u | -upd`
#### Update a note from the database by following additional arguments:
`--date` Add the previous date to the note you want to update.
`--cat` Add the previous number of transaction category to the note you want to update:
- `--cat 1` = "waste"
- `--cat 2` = "income"

- `--amt` Add a previous positive amount of money to the note that you want to update.
* If the number of transaction category is `"waste"`, the amount of money will change to a negative number **automatically.**

`--decs` Add the previous description to the note you want to update.
- **Skip this argument if an updated note doesn't have any description!**

`--newcat` Add a new number of transaction category to the note you want to update:
- `--newcat 1` = "waste"
- `--newcat` 2 = "income"

`--newamt` Add a new positive amount of money to the note you want to update.
* If the number of transaction category is `"waste"`, the amount of money will change to a negative number **automatically.**

*Optional argument:*
`--newdesc` Add a new description to the note you want to update.
> **The order of arguments doesn't play any role.**
#### Example:
```c
> python manage.py -upd --amt 34.69 --cat 2 --desc Cashback --newcat 1  --date 2024-05-09  --newamt 42
The update finished successfully!

----------------------------------------
Before the update:
----------------------------------------
Date: 2024-05-09
Category: income
Amount: 34.69
Description: Cashback

----------------------------------------
After the update:
----------------------------------------
Date: 2024-05-09
Category: waste
Amount: -42.0
Description:

****************************************
File "db.txt" has been updated!
****************************************
```
#### Text file `db.txt` has also been updated automatically:
```
Date: 2024-05-09  
Category: waste  
Amount: -42.0  
Description:   
  
------------------------------  
Current balance is: -42.00
```

---
### 4. Delete the note `-d | -del`
#### Delete the note from the database by following additional arguments:
`--date` Add a date to the note you want to delete.
`--cat` Add a number of transaction category to the note you want to delete:
- `--cat 1` = "waste"
- `--cat 2` = "income"

`--amt` Add a positive amount of money to the note you want to delete.
* If the number of transaction category is `"waste"`, the amount of money will change to a negative number **automatically.**

`--decs` Add a description to the note you want to delete.
- **Skip this argument if an updated note doesn't have any description!**
> **The order of arguments doesn't play any role.**
#### Example:
```c
> -del --amt 42.00 --date 2024-05-09 --cat 1    
The note has been deleted successfully!

----------------------------------------
Deleted note:
----------------------------------------
Date: 2024-05-09
Category: waste
Amount: -42.0
Description:

****************************************
Database is empty
****************************************
File "db.txt" has been deleted!
****************************************
```
#### If this note is the last in the database - text file `db.txt` will be deleted automatically.

---
### 5. Find a note(-s)  `-f | -find`
#### Find a note(-s) from the database by following additional arguments:
`--date` Add a date to the note(-s) you want to find.
`--cat` Add a number of transaction category to the note(-s) you want to find:
- `--cat 1` = "waste"
- `--cat 2` = "income"

`--amt` Add a positive amount of money to the note(-s) you want to find.
* If the number of transaction category is `"waste"`, the amount of money will change to a negative number **automatically.**

*Searching by [--desc] can be included into the next version of this app* 🤙
> **You can use 1, 2 or 3 of these arguments for the search.**
> **Each argument will filter notes in the database and then display search result in the Terminal.**
#### First of all, I will prepare several notes:
```c
> -create --amt 34.69 --cat 1 --desc Parking fine
The new note has been created!

----------------------------------------
Created note:
----------------------------------------
Date: 2024-05-09
Category: waste
Amount: -34.69
Description: Parking fine

****************************************
File "db.txt" has been created!
****************************************

> -c --amt 42 --cat 2 --desc Spice must flow
The new note has been created!

----------------------------------------
Created note:
----------------------------------------
Date: 2024-05-09
Category: income
Amount: 42.0
Description: Spice must flow
```
#### Note content in `db.txt`:
```
Date: 2024-05-09  
Category: waste  
Amount: -34.69  
Description: Parking fine  
  
Date: 2024-05-09  
Category: income  
Amount: 42.0  
Description: Spice must flow  
  
------------------------------  
Current balance is: 7.31
```
#### Now, we can try `-f | -find` command:
```c
> python manage.py -f --amt 9000
No matches in your search

> -f --amt 42  
------------------------------
Search result:
------------------------------

Date: 2024-05-09
Category: income
Amount: 42.0
Description: Spice must flow

> python manage.py -f --cat 1 --amt 34.69
------------------------------
Search result:
------------------------------

Date: 2024-05-09
Category: waste
Amount: -34.69
Description: Parking fine

> python manage.py -f --date 2024-05-09  
------------------------------
Search result:
------------------------------

Date: 2024-05-09
Category: waste
Amount: -34.69
Description: Parking fine

Date: 2024-05-09
Category: income
Amount: 42.0
Description: Spice must flow

> python manage.py -f --cat 2 --date 2024-05-09 --amt 42.00
------------------------------
Search result:
------------------------------

Date: 2024-05-09
Category: income
Amount: 42.0
Description: Spice must flow
```

---
### 6. Display your current balance `-s | -show`
> **Doesn't require any additional argument.**
#### Example:
```c
> python manage.py -show
----------------------------------------
Your current balance is: 7.31
----------------------------------------
```

---
### 7. Clear all notes from the database `-clear`
> **Doesn't require any additional argument.**
#### Example:
```c
> python manage.py -clear
The notes history has been cleaned!

****************************************
File "db.txt" has been deleted!
****************************************
```
#### It also leads to the removal of the `db.txt` text file.

---

<br>

Enjoy the Note Manager experience ❤ ❤ ❤
<br>
Note Manager ver.1.0.0
<br>
Created by Aleksander Zizevskikh
<br>
Email: zizevskikh.dev@gmail.com
<br>
