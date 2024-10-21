# Import necessary modules from tkinter and psycopg2
from tkinter import *  # Import everything from tkinter for GUI elements
from tkinter import messagebox  # Import messagebox to show popup messages
from tkinter import ttk  # Import ttk for themed widgets (e.g., buttons, labels)
import psycopg2  # Import psycopg2 to connect and interact with PostgreSQL database

# Function to connect and interact with the PostgreSQL database
def start_database(query, parameters=()):
    # Connect to the PostgreSQL database using the given credentials
    try:
        conn = psycopg2.connect(
            dbname="studentdb",  # Name of the database
            user="postgres",  # Database username
            password="Target@database",  # Database password
            host="localhost",  # Database host (usually localhost for local development)
            port="5432"  # Port where PostgreSQL is listening (default: 5432)
        )
    except psycopg2.Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

    # Create a cursor to execute SQL commands
    cur = conn.cursor()
    query_result = None  # Initialize variable to hold query result

    try:
        # Execute the SQL query with provided parameters
        cur.execute(query, parameters)

        # If it's a SELECT query, fetch and store the result
        if query.lower().startswith("select"):
            query_result = cur.fetchall()

        conn.commit()  # Commit the transaction to save any changes
        print("Connected successfully!")  # Print a success message to the console

    except psycopg2.Error as e:
        # Show an error message box if there is an issue with the database operation
        messagebox.showerror("Database Error", str(e))
    finally:
        # Close the cursor and connection, regardless of success or failure
        cur.close()  # Close the cursor
        conn.close()  # Close the database connection

    return query_result  # Return the result of the query, if applicable

# Function to refresh the tree view with student records
def refresh_treeview():
    # Delete all items in the treeview to avoid duplicates
    for item in tree.get_children():
        tree.delete(item)

    # Retrieve all student records from the database
    records = start_database("SELECT * FROM students;")

    if records:  # Check if records were retrieved
        # Insert each record into the tree view
        for record in records:
            tree.insert('', END, values=record)

# Function to insert new student data into the database
def insert_data():
    # Define the SQL query to insert new student data into the students table
    query = "INSERT INTO students(name, address, age, number) VALUES (%s, %s, %s, %s)"

    # Gather the data from the input fields (name, address, age, number)
    parameters = (name_entry.get().strip(), address_entry.get().strip(), age_entry.get().strip(), student_number_entry.get().strip())

    # Ensure that all fields are filled before inserting
    if not all(parameters):
        messagebox.showwarning("Warning", "All fields must be filled.")
        return

    # Execute the query with the inputted parameters
    start_database(query, parameters)

    # Show a success message when the record is inserted
    messagebox.showinfo("Information", "Records Inserted Successfully!")

    # Refresh the treeview to display the newly added data
    refresh_treeview()

# Function to delete the selected student record from the database
def delete_data():
    # Get the currently selected item in the treeview
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No student selected for deletion.")
        return

    student_id = tree.item(selected_item[0])['values'][0]  # Extract the student's ID

    # Define the SQL query to delete the student record based on the student ID
    query = "DELETE FROM students WHERE student_id=%s"
    parameters = (student_id,)  # Use the student's ID as the parameter

    # Execute the query to delete the student record
    start_database(query, parameters)

    # Show a success message indicating that the record has been deleted
    messagebox.showinfo("Information", "Data Deleted Successfully")

    # Refresh the treeview to remove the deleted record
    refresh_treeview()

# Function to update existing student data in the database
def update_data():
    # Check if a student record is selected in the treeview
    selected_items = tree.selection()
    if not selected_items:
        # Show a warning if no student is selected for update
        messagebox.showwarning("Warning", "No student selected for update.")
        return

    # Get the selected item's data (specifically the student ID)
    selected_item = selected_items[0]
    student_id = tree.item(selected_item)['values'][0]

    # Define the SQL query to update the student's information
    query = "UPDATE students SET name = %s, address = %s, age = %s, number = %s WHERE student_id = %s"

    # Gather the updated values from the input fields
    name = name_entry.get().strip()
    address = address_entry.get().strip()
    age = age_entry.get().strip()
    number = student_number_entry.get().strip()

    # Ensure that all fields are filled before updating
    if not all([name, address, age, number]):
        messagebox.showwarning("Warning", "All fields must be filled.")
        return

    # Set the query parameters (updated values + student ID)
    parameters = (name, address, age, number, student_id)

    # Execute the update query with the new data
    start_database(query, parameters)

    # Show a success message after updating the record
    messagebox.showinfo("Information", "Data updated successfully.")

    # Refresh the treeview to reflect the updated data
    refresh_treeview()

# Initialize the main Tkinter window
root = Tk()

# Set the background color of the main window
root.configure(background='#222')

# Create and configure a style object to style the widgets
style = ttk.Style()
style.theme_use('clam')  # Use a modern theme (clam) for the widgets

# Set the background and font styles for various widget types
style.configure("TFrame", background="#181C14")  # Frame background color
style.configure("TLabel", font=("Arial", 13), background="#181C14", foreground="white")  # Label font and color
style.configure("TButton", font=("Arial", 10), padding=(20, 7), background="white", foreground="#222")  # Button style
style.map("TButton", background=[('active', 'blue')])  # Change button color on hover
style.configure("TEntry", padding=5)  # Entry field padding

# Configure the grid layout for the window's rows
root.grid_rowconfigure(0, weight=1)  # Row 0 expands with the window
root.grid_rowconfigure(1, weight=0)  # Row 1 expands slightly
root.grid_rowconfigure(0, weight=1)  # Row 2 does not expand

# Create a frame for the labels and entry fields
frame = ttk.Frame(root, style="TFrame")
frame.grid(row=0, column=0, padx=30, pady=30, sticky='ew')

# Create a separate frame for the buttons
button_frame = ttk.Frame(root, style="Custom.TFrame")
button_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

# Create labels and entry fields for student data input
label = ttk.Label(frame, text="Student Data", style="TLabel")
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Label and entry for student name
label = ttk.Label(frame, text="Name:")
label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
name_entry = ttk.Entry(frame, font=('Arial', 16))
name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Label and entry for student address
label = ttk.Label(frame, text="Address:")
label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
address_entry = ttk.Entry(frame, font=('Arial', 16))
address_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Label and entry for student age
label = ttk.Label(frame, text="Age:")
label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
age_entry = ttk.Entry(frame, font=('Arial', 16))
age_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Label and entry for student number
label = ttk.Label(frame, text="Student Number:")
label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
student_number_entry = ttk.Entry(frame, font=('Arial', 16))
student_number_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# Create buttons for actions (Create Table, Add Data, Update Data, Delete Data)
ttk.Button(button_frame, text="Create Table").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Add Data", command=insert_data).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Update Data", command=update_data).grid(row=0, column=2, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Delete Data", command=delete_data).grid(row=0, column=3, padx=10, pady=10, sticky="ew")

# Create a frame to hold the Treeview (table-like display of student records)
tree_frame = ttk.Frame(root)
tree_frame.grid(row=2, column=0, padx=30, pady=30, sticky="nsew")

# Create a scrollbar for the Treeview
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create the Treeview widget to display student records
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse", style="TButton")
tree_scroll.config(command=tree.yview)  # Configure scrollbar to work with treeview

# Define the columns of the Treeview (student ID, name, address, age, number)
tree['columns'] = ("student_id", "name", "address", "age", "number")

# Hide the default first column (tree column)
tree.column("#0", width=0, stretch=NO)

# Set up each column with width and alignment
tree.column("student_id", anchor=CENTER, width=80)
tree.column("name", anchor=CENTER, width=120)
tree.column("address", anchor=CENTER, width=120)
tree.column("age", anchor=CENTER, width=50)
tree.column("number", anchor=CENTER, width=120)

# Set up the column headings
tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name", text="Name", anchor=CENTER)
tree.heading("address", text="Address", anchor=CENTER)
tree.heading("age", text="Age", anchor=CENTER)
tree.heading("number", text="Number", anchor=CENTER)

# Pack the Treeview into the frame
tree.pack(fill=BOTH, expand=True)

# Refresh the Treeview to show the initial student data
refresh_treeview()

# Start the Tkinter main loop to run the application
root.mainloop()
