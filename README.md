Student Management System
Description
This Student Management System is a desktop application built with Python and Tkinter. It provides a user-friendly interface for managing student records, allowing users to add, update, and delete student information. The application connects to a PostgreSQL database to store and retrieve data.
Features

Add new student records
Update existing student information
Delete student records
View all student records in a table format
Database integration for persistent storage

Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.x installed
PostgreSQL database server installed and running
psycopg2 library installed (pip install psycopg2)
tkinter library (usually comes pre-installed with Python)

Installation

Clone the repository:
Copygit clone https://github.com/kelvinnseth/Student_management_system.git

Navigate to the project directory:
Copycd student-management-system

Install the required dependencies:
Copypip install psycopg2


Configuration

Open the script in a text editor.
Locate the start_database function.
Update the database connection parameters:
pythonCopyconn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)


Usage

Run the script:
Copypython student_management_system.py

Use the GUI to interact with the student management system:

Enter student details in the provided fields
Click "Add Data" to insert a new student record
Select a record and click "Update Data" to modify existing information
Select a record and click "Delete Data" to remove a student entry
The table at the bottom displays all current student records



Contributing
Contributions to the Student Management System are welcome.




Project Link: https://github.com/yourusername/student-management-system
