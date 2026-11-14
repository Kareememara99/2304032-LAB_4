# KE Library
### Lab 3 — Database Course Project

**Student Name:** Kareem Emara  
**Student ID:** 2304032

---

## 1. Project Overview

**KE Library** is a web-based Library Management System developed using Python, Flask, and Microsoft SQL Server.

The application provides a simple and user-friendly interface for managing books and authors. Users can register, log in, and perform basic database operations through the website.

The project demonstrates the integration of a web application with relational databases and the implementation of CRUD operations.

## 2. Technologies Used

- **Python** — Application logic and backend development.
- **Flask** — Web framework used to build the application.
- **Microsoft SQL Server** — Relational database management system.
- **SQL Server Management Studio (SSMS)** — Database creation and management.
- **pyodbc** — Connects Python to SQL Server.
- **HTML and CSS** — Website structure and styling.
- **Jinja2** — Dynamic rendering of HTML templates.
- **Git** — Version control (if used).

## 3. Project Structure

```text
LAB3-2304032/
├── problem1_DDL.sql
├── problem1_DML.sql
├── problem1_Answers.txt
├── problem1_questions.sql
├── problem2_DDL.sql
├── problem2_DML.sql
├── README.md
└── website/
    ├── app.py
    ├── db.py
    ├── requirements.txt
    ├── templates/
    │   ├── library.html
    │   ├── login.html
    │   ├── register.html
    │   └── ...
    ├── static/
    │   └── ...
    └── .env
```

*Note: This is an illustrative structure. The actual files and template names may vary depending on the final project files.*

## 4. Database Design

The project uses two SQL Server databases.

### 4.1 Registration Database

The `registration` database handles user authentication.

The `users` table stores information such as:

- `user_id` — Unique user identifier.
- `name` — User's name.
- `email` — User's email address.
- `password_hash` — Hashed password.
- `registration_date` — Registration date.

### 4.2 Library Database

The `library` database stores information about books and their authors.

**AUTHOR table**

| Column | Description |
|---|---|
| `author_id` | Unique author identifier |
| `name` | Author's name |
| `country` | Author's country |

**BOOK table**

| Column | Description |
|---|---|
| `book_id` | Unique book identifier |
| `title` | Book title |
| `price` | Book price |
| `author_id` | ID of the book's author |

### 4.3 Relationship

The `BOOK` table contains a foreign key referencing `AUTHOR.author_id`.

This represents a one-to-many relationship: one author can have multiple books.

The foreign key uses `ON DELETE CASCADE`, so deleting an author also deletes the books associated with that author.

## 5. Main Features

### User Authentication

- User registration.
- User login and logout.
- Password hashing.
- Session-based authentication.

### Author Management

- Add a new author.
- View authors and their countries.
- Edit author information.
- Delete an author.

### Book Management

- Add a new book and assign it to an author.
- View books and their details.
- Edit book information.
- Delete a book.

### User Interface

- Dark-themed interface.
- Responsive layout for different screen sizes.
- Separate forms and cards for books and authors.
- Confirmation prompts before deleting records.

## 6. Requirements

Before running the project, make sure the following are installed:

- Python 3.
- Microsoft SQL Server.
- SQL Server Management Studio (SSMS).
- Microsoft ODBC Driver 17 for SQL Server.

## 7. Database Setup

1. Open SQL Server Management Studio.
2. Connect to your SQL Server instance.
3. Create the required `registration` and `library` databases if they do not already exist.
4. Execute the appropriate SQL scripts to create the tables and insert the initial data.
5. Verify that the required tables and relationships have been created successfully.

Run the SQL scripts in the correct order according to their contents and database dependencies.

## 8. Installation and Execution

### Step 1: Open the Website Directory

Open a terminal and navigate to the website folder:

```powershell
cd "D:\college\level 3\Database\labs\LAB3-2304032\website"
```

Adjust the path if the project is stored in a different location.

### Step 2: Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use the activation method appropriate for your system.

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Configure the Database Connection

Check `db.py` and configure the SQL Server connection settings to match your local environment.

The current project uses Windows trusted authentication and ODBC Driver 17.

Ensure that the required databases exist and that your Windows account has permission to access them.

If the application uses a `.env` file, configure the required environment variables according to the application's code.

### Step 6: Run the Application

```powershell
python app.py
```

Open the local URL displayed in the terminal, typically:

`http://127.0.0.1:5000`

Register an account or log in to access the library management page.

## 9. Testing

The following operations should be tested before submission:

- Registering a new user and logging in.
- Logging out and verifying the redirect behavior.
- Adding, editing, and deleting authors.
- Adding, editing, and deleting books.
- Checking that books are associated with the correct authors.
- Verifying that changes persist in SQL Server.
- Testing the foreign key relationship and cascading deletion.
- Restarting the application and confirming that saved data remains available.

## 10. Security and Configuration

- Passwords should be stored as hashes rather than plain text.
- Database connection settings and secrets should not be committed to a public repository.
- The `.env` file and virtual environment should be excluded from version control.
- Database operations should use parameterized queries to reduce SQL injection risks.

## 11. Conclusion

KE Library demonstrates how Python, Flask, and Microsoft SQL Server can be integrated to build a functional web-based database application.

The project combines user authentication, relational database design, foreign key constraints, and CRUD operations in a simple library management interface.

---


---

## Lab 4 — Problem 2: Library Database Pages

The Lab 4 implementation is added alongside the original Lab 3 library. It uses a separate SQL Server database named `library_lab4`, so the existing `registration` and `library` databases and their routes remain separate.

### Lab 4 website pages

After signing in, open the original KE Library page and choose **Lab 4 Pages**, or visit `/library-lab4`.

| Requirement | Route | Description |
|---|---|---|
| F2.1 | `/library-lab4/search` | Search by title keyword, price range, and category |
| F2.2 | `/library-lab4/catalogue` | Full book catalogue with author, publisher, and category |
| F2.3 | `/library-lab4/reports` | Category statistics, authors with at least two books, and price statistics |
| F2.4 | `/library-lab4/loans` | Outstanding loans, members who never borrowed, and books never borrowed |
| F2.5 | `/library-lab4/most-borrowed` | Top three most borrowed books and the member with most loans |
| F2.6 | `/library-lab4/authors` | All authors including zero-book authors, and same-country author/publisher books |

### Database setup

1. Open SQL Server Management Studio.
2. Create the `library_lab4` database if it does not already exist:
   ```sql
   CREATE DATABASE library_lab4;
   GO
   ```
3. Run `problem2_DDL.sql` in SSMS.
4. Run `problem2_DML.sql` once to insert the sample records.
5. Run `problem2_Queries.sql` to verify the required queries.

**Important:** The DDL script drops and recreates the six Lab 4 tables. Running it again deletes the current Lab 4 table data. Run the DML script only once after DDL unless you intentionally reset the database.

### Run the Flask website

1. Make sure SQL Server is running and the ODBC Driver 17 for SQL Server is installed.
2. In `website/db.py`, verify the SQL Server instance name and database names in the connection strings. The default is `SERVER=localhost` with Windows Trusted Connection.
3. Create a `.env` file in the `website` folder with a Flask secret key:
   ```env
   SECRET_KEY=replace-this-with-a-long-random-secret
   ```
4. Install dependencies (if they are not already installed):
   ```bash
   pip install flask pyodbc python-dotenv bcrypt
   ```
5. Start the application from the `website` folder:
   ```bash
   python app.py
   ```
6. Open the local URL printed by Flask, sign in, and click **Lab 4 Pages** on the original library page.

### SQL Server compatibility note

The assignment brief describes MySQL, while this project is implemented with Microsoft SQL Server. The website and SQL scripts therefore use SQL Server syntax, including `IDENTITY(1,1)` for generated IDs and `TOP` for top-N queries. If the instructor requires MySQL specifically, the scripts need dialect conversion before submission.
#   2 3 0 4 0 3 2 - L A B _ 4  
 