# 📚 KE Library — Library Management System

**Student Name:** Kareem Emara  
**Student ID:** 2304032

A full-stack Library Management System built with **Python, Flask, Microsoft SQL Server, and HTML/CSS**. The project combines user authentication, task management, a classic library interface, and an extended database-driven library application developed for Database Lab 4.

The application demonstrates relational database design, SQL queries, joins, filtering, sorting, reporting, and secure database interaction through a Flask web application.

---

## 📌 Project Overview

KE Library is designed to manage library data and provide an interactive interface for exploring books, authors, publishers, categories, members, and borrowing records.

The project includes two main parts:

1. **Original Application:** User registration, login, To-Do management, and the original library pages.
2. **Library Lab 4:** An extended library management application connected to a dedicated SQL Server database, implementing the required database operations and reports.

The original databases and functionality are preserved, while Lab 4 uses a separate database named `library_lab4`.

---

## ✨ Features

### 🔐 1. User Authentication

- User registration and login.
- Password hashing using `bcrypt`.
- Session-based authentication.
- Protected routes using a login-required decorator.
- Logout functionality.

### ✅ 2. To-Do Management

- Manage personal tasks.
- Store and retrieve tasks through the database.
- Keep user-related functionality separate from the library database.

### 📚 3. Book Search — F2.1

Search for books using different criteria:

- Search by book title or keyword.
- Filter books by minimum and maximum price.
- Filter by category.
- Display related author, publisher, and category information.

**Bonus: Prepared Statements**

The search functionality uses parameterized SQL queries with `?` placeholders.

Instead of inserting user input directly into SQL strings, values are passed separately through `cursor.execute()`.

This helps prevent SQL injection and makes database queries safer.

### 📖 4. Book Catalogue — F2.2

Display the complete book catalogue with information such as:

- Book ID
- Book title
- Price
- Publication year
- Author
- Publisher
- Category

**Sorting functionality:**

- Sort by Book ID.
- Sort by Book Name.
- Sort by Price.
- Choose ascending or descending order.

Sorting options are validated before being used in the SQL query.

### 📊 5. Library Reports — F2.3

Display useful statistics and information about the library database.

The reports section provides an overview of the available library data and helps users explore relationships between books and their related records.

### 🔄 6. Loan Management & History — F2.4

Track borrowing activity and manage book returns.

**Outstanding Loans**
- Display books that have been borrowed but not returned.
- Show loan ID, book, member, email, and loan date.
- Identify active borrowing records.

**Complete Loan History**
- Display all borrowing records.
- Show the borrowing date and return date.
- Distinguish between returned and unreturned books.
- Filter records by:
  - All Loans
  - Returned
  - Not Returned

**Mark as Returned**

Authorized users can mark a borrowed book as returned directly from the page.

When the user confirms the action:
- The corresponding loan record is updated.
- SQL Server records the current return date.
- The loan remains in the database as part of the borrowing history.

**Additional Reports**
- Members who have never borrowed a book.
- Books that have never been borrowed.

### 🏆 7. Most Borrowed — F2.5

Analyze borrowing activity to identify popular books and members.

The page provides information about borrowing frequency and helps highlight the most active borrowing records.

### ✍️ 8. Authors — F2.6

Explore author-related information stored in the database.

Includes author information and country-based comparisons to help analyze the authors represented in the library.

### 🎨 9. User Interface

- Dark-themed interface.
- Responsive layouts for different screen sizes.
- Shared navigation between Lab 4 pages.
- Organized tables and report sections.
- Clear status indicators and interactive controls.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Microsoft SQL Server | Relational database management |
| SQL | Database queries and operations |
| pyodbc | Python–SQL Server connectivity |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| Jinja2 | Dynamic HTML templates |
| bcrypt | Password hashing |
| python-dotenv | Environment variable management |

---

## 🗄️ Database Design

The Lab 4 application uses a dedicated SQL Server database:

**Database:** `library_lab4`

### Main Tables

| Table | Description |
|---|---|
| `AUTHOR` | Stores author information |
| `PUBLISHER` | Stores publisher information |
| `CATEGORY` | Stores book categories |
| `BOOK` | Stores book details and relationships |
| `MEMBER` | Stores library member information |
| `LOAN` | Stores borrowing and return records |

### Relationships

- An author can be associated with multiple books.
- A publisher can publish multiple books.
- A category can contain multiple books.
- A book can have multiple loan records over time.
- A member can borrow multiple books.

### Loan Status Logic

The `LOAN` table contains a `return_date` column.

| Condition | Status |
|---|---|
| `return_date IS NULL` | Not Returned |
| `return_date IS NOT NULL` | Returned |

This approach preserves borrowing history instead of deleting loan records after a book is returned.

---

## 🏗️ Application Structure

The project is organized into backend logic, database connectivity, HTML templates, CSS, and SQL scripts.

```text
KE-Library/
│
├── website/
│   ├── app.py
│   │
│   ├── db.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── ...
│   │   │
│   │   ├── lab4_base.html
│   │   ├── lab4_search.html
│   │   ├── lab4_catalogue.html
│   │   ├── lab4_reports.html
│   │   ├── lab4_loans.html
│   │   ├── lab4_most_borrowed.html
│   │   └── lab4_authors.html
│   │
│   └── static/
│       └── lab4.css
│
├── SQL/
│   ├── DDL.sql
│   └── DML.sql
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above illustrates the main project components. File names and folder locations may differ slightly in your local version.*

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd KE-Library
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file yet, install the main dependencies:

```bash
pip install Flask pyodbc python-dotenv bcrypt
```

### 4. Configure SQL Server

Make sure you have:

- Microsoft SQL Server installed and running.
- SQL Server Management Studio (SSMS).
- A compatible Microsoft ODBC Driver for SQL Server.

Open the SQL scripts in SSMS.

**Create the Lab 4 database and tables:**

Execute `DDL.sql` to create the `library_lab4` database and its tables.

**Insert sample data:**

Execute `DML.sql` to populate the tables with sample records.

> If the database already exists, don't execute the `CREATE DATABASE` statement again. Select the existing database and run only the required table or data scripts.

### 5. Configure Database Connections

Update your database connection settings in `db.py`.

The application uses separate connection functions for its different databases:

```python
get_connection()
get_library_connection()
get_library_lab4_connection()
```

Make sure each function points to the correct SQL Server database and authentication settings.

Keep your actual credentials out of GitHub. Store sensitive configuration in environment variables or a local `.env` file.

### 6. Run the Application

From the appropriate project directory, run:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

Register or log in to access the application.

---

## 🧠 Database Concepts Demonstrated

This project applies several important relational database concepts:

- **DDL:** Creating databases, tables, constraints, and relationships.
- **DML:** Inserting and modifying database records.
- **SELECT Queries:** Retrieving and filtering data.
- **INNER JOIN:** Combining related records from multiple tables.
- **LEFT JOIN:** Identifying members and books without borrowing records.
- **Aggregate Functions:** Calculating statistics and borrowing counts.
- **GROUP BY:** Grouping records for reporting.
- **ORDER BY:** Sorting books and report results.
- **NULL Handling:** Identifying books that have not been returned.
- **Foreign Keys:** Maintaining relationships between tables.
- **Parameterized Queries:** Passing user input safely to SQL Server.
- **UPDATE:** Modifying loan records when books are returned.

---

## 🔒 Security & Good Practices

- Passwords are hashed using `bcrypt`.
- Database queries use parameterized values where applicable.
- User input is not directly concatenated into search SQL statements.
- Sorting options are validated against allowed values.
- Login-protected pages use session authentication.
- Database connections and cursors are closed after use.
- Database credentials should not be committed to the repository.

---

## 🚀 Future Improvements

Potential enhancements include:

- Add new borrowing records directly through the interface.
- Add member and book management forms (CRUD operations).
- Add due dates and overdue loan notifications.
- Add pagination for large catalogues and loan histories.
- Add advanced analytics and visual dashboards.
- Add role-based permissions for administrators and members.

---


## 📄 License

This project was developed for educational purposes as part of a Database Systems Lab assignment.

You may adapt and extend it for learning and personal development.
