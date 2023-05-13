import tkinter as tk
import sqlite3
import datetime
import os
from PIL import Image, ImageTk
from tkinter import messagebox

# Create a connection to the SQLite database
mydb = sqlite3.connect('mydatabase.db')
# Get the current working directory
cwd = os.getcwd()

# Construct the path to the database file
db_path = os.path.join(cwd, 'mydatabase.db')

# Create a connection to the SQLite database
mydb = sqlite3.connect(db_path)
# Create a cursor to interact with the database
mycursor = mydb.cursor()

# Create the necessary tables in the SQLite database
mycursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS carers (carer_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY AUTOINCREMENT, c_id INTEGER, message TEXT, datetime TEXT, status TEXT DEFAULT 'pending', FOREIGN KEY(c_id) REFERENCES customers(customer_id))")



mydb.commit()

# Execute a SELECT statement
username = 'zizo'
password = '123456'
mycursor.execute("SELECT * FROM customers WHERE username=? AND password=?", (username, password))
#username1= 'zizo'
#password1 = '123456'
#mycursor.execute("SELECT * FROM carers WHERE username=? AND password=?", (username1, password1))

# Fetch the result of the SELECT statement
result = mycursor.fetchone()
if result:
    print(result)
else:
    print("No such user exists in the database.")

# Create the GUI window
root = tk.Tk()
root.geometry('800x500')
root.title('Home Page')


    # Load the PNG image
image = Image.open('C:/Users/User/Desktop/collaborative dev/z.png')
image1 = Image.open('C:/Users/User/Desktop/collaborative dev/zz.png')
photo = ImageTk.PhotoImage(image)
photo1 = ImageTk.PhotoImage(image1)



    # Create a Label widget with the image as the background
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Keep a reference to the photo object
background_label.image = photo

def logout(user_type):
    # Destroy the current window
    root.destroy()

    # Create a new instance of the root window
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Login")

    # Go back to the login page based on the user type
    if user_type == 'customer':
        customer_login()
    elif user_type == 'carer':
        carer_login() 
    




# Define the functions to handle button clicks
def customer_login():
    
    # Create the customer login page
    customer_window = tk.Toplevel(root)
    #customer_window.geometry('500x500')
    customer_window.geometry('1300x1000')
    customer_window.title('Customer Login')

     # Create the Label widget with the background image
    background_label = tk.Label(customer_window, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

   

    # Create the form to enter customer details
    tk.Label(customer_window, text='Customer Login').pack()
    tk.Label(customer_window, text='Username').pack()
    customer_username = tk.Entry(customer_window)
    customer_username.pack()
    tk.Label(customer_window, text='Password').pack()
    customer_password = tk.Entry(customer_window, show='*')
    customer_password.pack()

    

    # Create a button to submit the form and validate the customer details
    def validate_customer_login():
        username = customer_username.get()
        password = customer_password.get()
        mycursor.execute("SELECT * FROM customers WHERE username=? AND password=?", (username, password))
        result = mycursor.fetchone()
        if result:
            customer_id = result[0]
            customer_home_window = customer_home(customer_id)
            #send_button = tk.Button(customer_home_window, text="Send", command=lambda: send_message(customer_id))
            #send_button.pack()
        else:
            tk.Label(customer_window, text='Invalid username or password').pack()


    tk.Button(customer_window, text='Login', command=validate_customer_login).pack()
    
    # Create the "Back" button
    tk.Button(customer_window, text='Back', command=customer_window.destroy).pack()

def go_back():
    # Destroy the current window and go back to the login page
    root.deiconify()
    root.geometry('500x500')
    root.title('Login')
    tk.Button(root, text='Customer Login', command=customer_login).pack()
    tk.Button(root, text='Carer Login').pack()


    # Create the send button
def customer_home(customer_id):
    # Create the customer home window
    customer_home_window = tk.Toplevel(root)

    customer_home_window.title("Customer Home")

    # Set the window size to fill the screen
    w, h = customer_home_window.winfo_screenwidth(), customer_home_window.winfo_screenheight()
    customer_home_window.geometry("%dx%d+0+0" % (w, h))

    # Create the Label widget with the background image
    background_label = tk.Label(customer_home_window, image=photo1)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create the message label and entry
    tk.Label(customer_home_window, text="Message").place(relx=0.5, rely=0.4, anchor="center")
    message_entry = tk.Entry(customer_home_window)
    message_entry.place(relx=0.5, rely=0.5, anchor="center")

    # Create the send button
    def send_message(customer_id):
        # Get the message text
        message = message_entry.get()

        # Get the current datetime
        now = datetime.datetime.now()

        # Format the datetime as a string in the correct format
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        # Insert the message into the database along with the customer id
        sql = "INSERT INTO messages (c_id, message, datetime) VALUES (?, ?, ?)"
        val = (customer_id, message, formatted_datetime)
        mycursor.execute(sql, val)
        mydb.commit()

        # Show a confirmation message
        confirmation_window = tk.Toplevel(customer_home_window)
        confirmation_window.title("Message Sent")
        confirmation_label = tk.Label(confirmation_window, text="Your message has been sent to the carer.")
        confirmation_label.pack(pady=10)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack()


        # Empty the message box
        message_entry.delete(0, tk.END)

    send_button = tk.Button(customer_home_window, text="Send", command=lambda: send_message(customer_id))
    send_button.place(relx=0.5, rely=0.6, anchor="center")

  
   

    def logout_customer():
        # Destroy the current window
        customer_home_window.destroy()

        # Go back to the customer login page
        customer_login()

    logout_button = tk.Button(customer_home_window, text="Logout", command=logout_customer)
    logout_button.pack()

    return customer_home_window



    
def carer_login():
    # Create the carer login page
    carer_window = tk.Toplevel(root)
    carer_window.geometry('1300x1000')
    carer_window.title('Carer Login')

     # Create the Label widget with the background image
    background_label = tk.Label(carer_window, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create the form to enter carer details
    tk.Label(carer_window, text='Carer Login').pack()
    tk.Label(carer_window, text='Username').pack()
    carer_username = tk.Entry(carer_window)
    carer_username.pack()
    tk.Label(carer_window, text='Password').pack()
    carer_password = tk.Entry(carer_window, show='*')
    carer_password.pack()

    def validate_carer_login():
        username = carer_username.get()
        password = carer_password.get()
        mycursor.execute("SELECT * FROM carers WHERE username=? AND password=?", (username, password))
        result1 = mycursor.fetchone()
        if result1:
            carer_id = result1[0]
            carer_home(carer_id)
        else:
            tk.Label(carer_window, text='Invalid username or password').pack()

    tk.Button(carer_window, text='Login', command=validate_carer_login).pack()
    # Create the "Back" button
    tk.Button(carer_window, text='Back', command=carer_window.destroy).pack()

def carer_home(carer_id):
    # Create the carer home window
    carer_home_window = tk.Toplevel(root)
    carer_home_window.title("Carer Home")
    # Set the window size to fill the screen
    w, h = carer_home_window.winfo_screenwidth(), carer_home_window.winfo_screenheight()
    carer_home_window.geometry("%dx%d+0+0" % (w, h))
    # Create the Label widget with the background image
    background_label = tk.Label(carer_home_window, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Retrieve the carer's username from the database
    mycursor.execute("SELECT username FROM carers WHERE carer_id = ?", (carer_id,))
    username = mycursor.fetchone()[0]

    # Display the carer's username in a label
    tk.Label(carer_home_window, text="Welcome, " + username + "!").place(relx=0.5, rely=0.1, anchor="center")

    # Retrieve the messages from the database
    mycursor.execute("SELECT message, datetime, c_id FROM messages")
    messages = mycursor.fetchall()

    # Create the message listbox
    tk.Label(carer_home_window, text="Messages").place(relx=0.5, rely=0.4, anchor="center")
    message_listbox = tk.Listbox(carer_home_window, height=10, width=60)
    message_listbox.grid(row=2, column=0, columnspan=2)
    message_listbox.place(relx=0.5, rely=0.5, anchor="center")

    # Add column headers to the message listbox
    headers = ["Message", "Date Time", "Customer ID"]
    message_listbox.insert(tk.END, f"{headers[0]:<50} {headers[1]:<25} {headers[2]:<15}")
    message_listbox.itemconfig(0, {'fg': 'white', 'bg': 'black'})

    for message in messages:
        # Align the message text with the column headers
        #message_text = f"{message[0]:<50} {str(message[1]):<25} {str(message[2]):<15}"
        #message_listbox.insert(tk.END, message_text)
    # Format the message and datetime strings
    # Combine the message and datetime into a single string
        message_text = message[0].ljust(40) + str(message[1]).rjust(30) + str(message[2]).rjust(20)
        message_listbox.insert(tk.END, message_text)



    
    # Create the accept and reject buttons
        def accept_message():
            # Get the selected message from the listbox
            selected_index = message_listbox.curselection()
            if len(selected_index) == 0:
                root.withdraw()
                tk.messagebox.showerror("Error", "Please select a message.")
                root.deiconify()
                carer_home(carer_id)

                return

            selected_message = message_listbox.get(selected_index[0])

            # Update the status of the message in the database
            sql = "UPDATE messages SET status = ? WHERE message = ?"
            val = ("accepted", selected_message)
            mycursor.execute(sql, val)
            mydb.commit()

            # Remove the message from the listbox
            message_listbox.delete(selected_index)

            # Hide the main window and show a message box
            root.withdraw()
            message_box = tk.messagebox.showinfo("Message Accepted", "You have accepted the message.")
            root.deiconify()

            # Redirect to the same page
            carer_home(carer_id)











    def reject_message():
       # Get the selected message from the listbox
        selected_index = message_listbox.curselection()
        if len(selected_index) == 0:
            root.withdraw()
            tk.messagebox.showerror("Error", "Please select a message.")
            root.deiconify()
            carer_home(carer_id)

            return

        selected_message = message_listbox.get(selected_index[0])

        # Update the status of the message in the database
        sql = "UPDATE messages SET status = ? WHERE message = ?"
        val = ("rejected", selected_message)
        mycursor.execute(sql, val)
        mydb.commit()

        # Remove the message from the listbox
        message_listbox.delete(selected_index)

        # Hide the main window and show a message box
        root.withdraw()
        message_box = tk.messagebox.showinfo("Message Rejected", "You have rejected the message.")
        root.deiconify()

        # Redirect to the same page
        carer_home(carer_id)



    def logout_carer():
        # Destroy the current window
        carer_home_window.destroy()

        # Go back to the customer login page
        carer_login()

    logout_button = tk.Button(carer_home_window, text="Logout", command=logout_carer)
    logout_button.pack()    

    accept_button = tk.Button(carer_home_window, text="Accept", command=accept_message)
    accept_button.place(relx=0.35, rely=0.8, anchor='center')
    reject_button = tk.Button(carer_home_window, text="Reject", command=reject_message)
    reject_button.place(relx=0.65, rely=0.8, anchor='center')


 
# Close the database connection



tk.Label(root, text='Welcome to the Home Page').pack()
tk.Button(root, text='Customer', command=customer_login).pack()
tk.Button(root, text='Carer', command=carer_login).pack()

root.mainloop()
