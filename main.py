from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    gen_password = "".join(password_list)

    password_entry.insert(0, gen_password)
    pyperclip.copy(gen_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "User": user,
            "Password": password
        }
    }

    if website == "" or password == "":
        messagebox.showwarning(title="Retard!", message="YOU CANNOT LEAVE ANY FIELD EMPTY!")

    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
            account = data[website_entry.get()]
            messagebox.showinfo(title="Log in info", message="Your username/email is: {}\nYour password is: {}"
                                .format(account["User"], account["Password"]))
            pyperclip.copy(account["Password"])
            website_entry.delete(0, END)
    except FileNotFoundError:
        messagebox.showwarning(title="File Not Found", message="No Data File Found.")
    except KeyError:
        messagebox.showwarning(title="Website Error", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #

# Window

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Canvas

canvas = Canvas(height=200, width=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels

website_label = Label(text="Website:")
user_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

website_label.grid(row=1, column=0)
user_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)

# Entries

website_entry = Entry(width=21)
user_entry = Entry(width=35)
password_entry = Entry(width=21)

website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
user_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
password_entry.grid(row=3, column=1, sticky="ew")

user_entry.insert(0, "filipzara@gmail.com")

# Buttons

password_gen_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=36, command=save)
search_button = Button(text="Search", command=find_password)

password_gen_button.grid(row=3, column=2, sticky="ew")
add_button.grid(row=4, column=1, columnspan=2, sticky="ew")
search_button.grid(row=1, column=2, sticky="ew")

window.mainloop()
