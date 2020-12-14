from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from datetime import datetime
import json

NAVY = '#0A043C'
GREY = '#bbbbbb'
BEIGE = '#ffe3d8'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():

    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!@#$%^&*()_+')
    letters_lower = list(map(str.lower,letters))
    letters.extend(letters_lower)

    #Return a number between a and b (both included):
    num_letters = random.randint(8,10)
    num_numbers = random.randint(1,2)
    num_symbols = random.randint(1,2)

    # Creating password and concat to a list
    rand_letters = [random.choice(letters) for i in range(num_letters)]
    rand_numbers = [random.choice(numbers) for i in range(num_numbers)]
    rand_symbols = [random.choice(symbols) for i in range(num_symbols)]

    created_password = rand_letters + rand_numbers + rand_symbols

    # Shuffle the positions and join to create str
    random.shuffle(created_password)
    created_password = ''.join(created_password)

    # Insert into password_entry label upon clicking "Generate password"
    password_entry.delete(0, END)
    password_entry.insert(0, created_password)

    # Copy created password to clipboard
    pyperclip.copy(created_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def saved_entries():

    # GETTING THE USER INPUTS
    user_website = website_entry.get()
    user_email = email_entry.get()
    user_password = password_entry.get()

    new_data = {
        user_website: {
            'email': user_email,
            'password': user_password
            }
        }
    if len(user_website) != 0 and len(user_password) != 0:

        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open('data.json','w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            is_correct = messagebox.askyesno(
                    title=f"{user_website}",
                    message=f"\n'email': {user_email}\n'password': {user_password}\n\nPlease confirm before saving!")
            if is_correct:
                with open('data.json','w') as data_file:
                    json.dump(data, data_file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
    else:
        # IF WEBSITE OR EMAIL ENTRY IS BLANK
        messagebox.showwarning(
            title='Oops',
            message="Please don't leave any fields empty!"
            )
# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search_website():

    user_website = website_entry.get().capitalize()

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            user_password = data[user_website]['password']
            password_entry.delete(0, END)
            password_entry.insert(0, user_password)
    except KeyError as error_msg:
        messagebox.showinfo(title="Key Error", message=f"{error_msg} password does not exist")
    except FileNotFoundError as error_msg:
        messagebox.showinfo(message="File does not exist. Try using Add instead")
# ---------------------------- UI SETUP ------------------------------- #

root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50, bg=NAVY)

# ROW 0
canvas = Canvas(height=200, width=200, bg=NAVY, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(row=0,column=1)

# ROW 1
website_label = Label(text='Website:', bg=NAVY, fg=BEIGE)
website_label.grid(row=1,column=0,sticky="W")

website_entry = Entry(font=('Arial',15))
website_entry.grid(row=1,column=1, columnspan=2,sticky="EW")
website_entry.focus()

website_search = Button(text='Search', bg=GREY, command=search_website)
website_search.grid(row=1,column=2,sticky="EW")

# ROW 2
email_label = Label(text='Email/Username:', bg=NAVY, fg=BEIGE)
email_label.grid(row=2,column=0,sticky="W")

email_entry = Entry(font=('Arial',15))
email_entry.grid(row=2,column=1, columnspan=2,sticky="EW")
email_entry.insert(0, 'myusername@gmail.com')

# ROW 3
password_label = Label(text='Password:', bg=NAVY, fg=BEIGE)
password_label.grid(row=3,column=0,sticky="W")

password_entry = Entry(font=('Arial',15))
password_entry.grid(row=3,column=1,sticky="EW")

password_button = Button(text='Generate Password', bg=GREY, command=random_password)
password_button.grid(row=3,column=2,sticky="EW")

# ROW 4
button = Button(text='Add', bg=GREY, command=saved_entries)
button.grid(row=4,column=1,columnspan=2,sticky="EW")
button.config(pady=2)


root.mainloop()
