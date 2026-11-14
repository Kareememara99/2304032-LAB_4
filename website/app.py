
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from db import get_connection, get_library_connection, get_library_lab4_connection
from functools import wraps
import bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")



@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("library_page"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    name = ""
    email = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name:
            errors.append("Name is required")
        elif len(name) > 100:
            errors.append("Name is too long")

        if not email:
            errors.append("Email is required")
        elif len(email) > 255:
            errors.append("Email is too long")

        if not password:
            errors.append("Password is required")

        if not confirm_password:
            errors.append("Confirm password is required")

        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match")

        if not errors:
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn = None
            cursor = None

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (email, name, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (email, name, password_hash)
                )

                conn.commit()

                cursor.execute(
                    "SELECT user_id FROM users WHERE email = ?",
                    (email,)
                )

                user = cursor.fetchone()

                if not user:
                    raise Exception("Unable to retrieve the registered user")

                session.clear()
                session["user_id"] = user[0]
                session["name"] = name

                return redirect(url_for("todos_page"))

            except Exception as e:
                if conn:
                    conn.rollback()

                error_message = " ".join(
                    str(arg) for arg in getattr(e, "args", ())
                ).lower()

                if (
                    "23000" in error_message
                    or "2627" in error_message
                    or "2601" in error_message
                    or "duplicate key" in error_message
                    or "unique constraint" in error_message
                ):
                    errors.append("Email Already Exists")
                else:
                    app.logger.exception("Registration failed")
                    errors.append(
                        "Registration failed. Please try again."
                    )

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    return render_template(
        "register.html",
        errors=errors,
        name=name,
        email=email
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email:
            errors.append("Email is required")

        if not password:
            errors.append("Password is required")

        if not errors:
            conn = None
            cursor = None

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, name, password_hash
                    FROM users
                    WHERE email = ?
                    """,
                    (email,)
                )

                user = cursor.fetchone()

                if user and bcrypt.checkpw(
                    password.encode("utf-8"),
                    user[2].encode("utf-8")
                ):
                    session.clear()
                    session["user_id"] = user[0]
                    session["name"] = user[1]

                    return redirect(url_for("library_page"))

                errors.append("Invalid email or password")

            except Exception:
                app.logger.exception("Login failed")
                errors.append("Login failed. Please try again.")

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    return render_template("login.html", errors=errors)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


def get_user_todos():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT todo_id, title, is_done, created_at
            FROM todos
            WHERE user_id = ?
            ORDER BY todo_id DESC
            """,
            (session["user_id"],)
        )

        rows = cursor.fetchall()

        return [
            {
                "todo_id": row[0],
                "title": row[1],
                "is_done": row[2],
                "created_at": row[3]
            }
            for row in rows
        ]

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def render_todos_with_errors(errors, status=200):
    todos = get_user_todos()
    open_count = sum(1 for todo in todos if not todo["is_done"])

    return render_template(
        "todos.html",
        todos=todos,
        name=session["name"],
        errors=errors,
        open_count=open_count
    ), status


@app.route("/todos")
@login_required
def todos_page():
    todos = get_user_todos()

    open_count = sum(
        1 for todo in todos
        if not todo["is_done"]
    )

    return render_template(
        "todos.html",
        todos=todos,
        name=session["name"],
        errors=[],
        open_count=open_count
    )


@app.route("/todos/add", methods=["POST"])
@login_required
def add_todo():
    title = request.form.get("title", "").strip()

    if not title:
        return render_todos_with_errors(["Title is required"], 400)

    if len(title) > 200:
        return render_todos_with_errors(["Title is too long"], 400)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO todos (user_id, title)
            VALUES (?, ?)
            """,
            (session["user_id"], title)
        )

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Adding task failed")

        return render_todos_with_errors(
            ["Unable to add task. Please try again."],
            500
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("todos_page"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
@login_required
def edit_todo(todo_id):
    title = request.form.get("title", "").strip()

    if not title:
        return render_todos_with_errors(["Title is required"], 400)

    if len(title) > 200:
        return render_todos_with_errors(["Title is too long"], 400)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE todos
            SET title = ?
            WHERE todo_id = ? AND user_id = ?
            """,
            (title, todo_id, session["user_id"])
        )

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Updating task failed")

        return render_todos_with_errors(
            ["Unable to update task. Please try again."],
            500
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("todos_page"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
@login_required
def toggle_todo(todo_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE todos
            SET is_done = CASE
                WHEN is_done = 1 THEN 0
                ELSE 1
            END
            WHERE todo_id = ? AND user_id = ?
            """,
            (todo_id, session["user_id"])
        )

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Changing task status failed")

        return render_todos_with_errors(
            ["Unable to change task status. Please try again."],
            500
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("todos_page"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM todos
            WHERE todo_id = ? AND user_id = ?
            """,
            (todo_id, session["user_id"])
        )

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Deleting task failed")

        return render_todos_with_errors(
            ["Unable to delete task. Please try again."],
            500
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("todos_page"))




@app.route("/library")
@login_required
def library_page():
    conn = None
    cursor = None

    sort_options = {
        "default": "b.book_id DESC",
        "price_asc": "b.price ASC",
        "price_desc": "b.price DESC",
        "author_asc": "a.name ASC, b.title ASC",
        "author_desc": "a.name DESC, b.title ASC"
    }

    sort_by = request.args.get("sort", "default")

    if sort_by not in sort_options:
        sort_by = "default"

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        # Get all books with their authors
        query = f"""
            SELECT
                b.book_id,
                b.title,
                b.price,
                b.author_id,
                a.name AS author_name,
                a.country AS author_country
            FROM book b
            LEFT JOIN author a
                ON b.author_id = a.author_id
            ORDER BY {sort_options[sort_by]}
        """

        cursor.execute(query)

        books = [
            {
                "book_id": row[0],
                "title": row[1],
                "price": row[2],
                "author_id": row[3],
                "author_name": row[4] or "Unknown",
                "author_country": row[5] or "Unknown"
            }
            for row in cursor.fetchall()
        ]

        # Get all authors
        cursor.execute("""
            SELECT author_id, name, country
            FROM author
            ORDER BY author_id
        """)

        authors = [
            {
                "author_id": row[0],
                "name": row[1],
                "country": row[2]
            }
            for row in cursor.fetchall()
        ]

        return render_template(
            "library.html",
            name=session["name"],
            books=books,
            authors=authors
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/library/authors/add", methods=["POST"])
@login_required
def add_author():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()

    if not name or not country:
        return redirect(url_for("library_page"))

    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO author (name, country) VALUES (?, ?)",
            (name, country)
        )
        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("library_page"))


@app.route("/library/books/add", methods=["POST"])
@login_required
def add_book():
    title = request.form.get("title", "").strip()
    price_text = request.form.get("price", "").strip()
    author_id_text = request.form.get("author_id", "").strip()

    if not title or not price_text or not author_id_text:
        return redirect(url_for("library_page"))

    try:
        price = float(price_text)
        author_id = int(author_id_text)

        if price < 0:
            return redirect(url_for("library_page"))

    except ValueError:
        return redirect(url_for("library_page"))

    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT author_id FROM author WHERE author_id = ?",
            (author_id,)
        )

        if cursor.fetchone() is None:
            return redirect(url_for("library_page"))

        cursor.execute(
            """
            INSERT INTO book (title, price, author_id)
            VALUES (?, ?, ?)
            """,
            (title, price, author_id)
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("library_page"))


@app.route("/library/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            price_text = request.form.get("price", "").strip()
            author_id_text = request.form.get("author_id", "").strip()

            if not title or not price_text or not author_id_text:
                return redirect(url_for("library_page"))

            try:
                price = float(price_text)
                author_id = int(author_id_text)

                if price < 0:
                    return redirect(url_for("library_page"))

            except ValueError:
                return redirect(url_for("library_page"))

            cursor.execute(
                "SELECT author_id FROM author WHERE author_id = ?",
                (author_id,)
            )

            if cursor.fetchone() is None:
                return redirect(url_for("library_page"))

            cursor.execute(
                """
                UPDATE book
                SET title = ?, price = ?, author_id = ?
                WHERE book_id = ?
                """,
                (title, price, author_id, book_id)
            )

            conn.commit()
            return redirect(url_for("library_page"))

        cursor.execute(
            """
            SELECT book_id, title, price, author_id
            FROM book
            WHERE book_id = ?
            """,
            (book_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return redirect(url_for("library_page"))

        book = {
            "book_id": row[0],
            "title": row[1],
            "price": row[2],
            "author_id": row[3]
        }

        cursor.execute(
            "SELECT author_id, name FROM author ORDER BY name"
        )

        authors = [
            {"author_id": row[0], "name": row[1]}
            for row in cursor.fetchall()
        ]

        return render_template(
            "edit_book.html",
            name=session["name"],
            book=book,
            authors=authors
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/library/books/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM book WHERE book_id = ?",
            (book_id,)
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("library_page"))


@app.route("/library/authors/<int:author_id>/delete", methods=["POST"])
@login_required
def delete_author(author_id):
    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM author WHERE author_id = ?",
            (author_id,)
        )

        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("library_page"))


@app.route("/library/authors/<int:author_id>/edit", methods=["GET", "POST"])
@login_required
def edit_author(author_id):
    conn = None
    cursor = None

    try:
        conn = get_library_connection()
        cursor = conn.cursor()

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            country = request.form.get("country", "").strip()

            if not name or not country:
                return redirect(url_for("library_page"))

            cursor.execute(
                """
                UPDATE author
                SET name = ?, country = ?
                WHERE author_id = ?
                """,
                (name, country, author_id)
            )

            conn.commit()
            return redirect(url_for("library_page"))

        cursor.execute(
            """
            SELECT author_id, name, country
            FROM author
            WHERE author_id = ?
            """,
            (author_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return redirect(url_for("library_page"))

        author = {
            "author_id": row[0],
            "name": row[1],
            "country": row[2]
        }

        return render_template(
            "edit_author.html",
            name=session["name"],
            author=author
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# LAB 4 - PROBLEM 2: LIBRARY REPORTING PAGES
# These routes use the separate library_lab4 database.
# The original registration, todos, and Lab 3 library routes
# above remain unchanged.
# ============================================================

def lab4_fetch_all(cursor):
    """Convert the current query result into dictionaries."""
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@app.route("/library-lab4")
@login_required
def lab4_home():
    """Lab 4 library dashboard / catalogue landing page."""
    return redirect(url_for("lab4_catalogue"))


@app.route("/library-lab4/search")
@login_required
def lab4_search():
    keyword = request.args.get("keyword", "").strip()
    min_price_text = request.args.get("min_price", "").strip()
    max_price_text = request.args.get("max_price", "").strip()
    category_text = request.args.get("category_id", "").strip()

    errors = []
    min_price = None
    max_price = None
    category_id = None

    try:
        if min_price_text:
            min_price = float(min_price_text)
            if min_price < 0:
                raise ValueError
        if max_price_text:
            max_price = float(max_price_text)
            if max_price < 0:
                raise ValueError
        if min_price is not None and max_price is not None and min_price > max_price:
            errors.append("Minimum price cannot be greater than maximum price.")
        if category_text:
            category_id = int(category_text)
    except ValueError:
        errors.append("Enter valid non-negative prices and a valid category.")

    conn = cursor = None
    books, categories = [], []
    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_id, name FROM CATEGORY ORDER BY name")
        categories = lab4_fetch_all(cursor)

        if not errors:
            sql = """
                SELECT b.book_id, b.title, b.price, b.publish_year,
                       a.name AS author_name, p.name AS publisher_name,
                       c.name AS category_name
                FROM BOOK b
                INNER JOIN AUTHOR a ON b.author_id = a.author_id
                INNER JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
                INNER JOIN CATEGORY c ON b.category_id = c.category_id
                WHERE b.title LIKE ?
                  AND (? IS NULL OR b.price >= ?)
                  AND (? IS NULL OR b.price <= ?)
                  AND (? IS NULL OR b.category_id = ?)
                ORDER BY b.price ASC, b.title ASC
            """
            cursor.execute(
                sql,
                (f"%{keyword}%", min_price, min_price,
                 max_price, max_price, category_id, category_id)
            )
            books = lab4_fetch_all(cursor)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_search.html", name=session["name"], books=books,
        categories=categories, keyword=keyword,
        min_price=min_price_text, max_price=max_price_text,
        selected_category=category_text, errors=errors
    )



@app.route("/library-lab4/catalogue")
@login_required
def lab4_catalogue():

    # Available sorting columns
    sort_options = {
        "id": "b.book_id",
        "name": "b.title",
        "price": "b.price"
    }

    # Get sorting choices from URL
    sort_by = request.args.get("sort_by", "name").lower()
    sort_order = request.args.get("sort_order", "asc").lower()

    # Validate inputs
    if sort_by not in sort_options:
        sort_by = "name"

    if sort_order not in ("asc", "desc"):
        sort_order = "asc"

    conn = cursor = None
    books = []

    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT b.book_id, b.title, b.price, b.publish_year,
                   a.name AS author_name,
                   p.name AS publisher_name,
                   c.name AS category_name
            FROM BOOK b
            INNER JOIN AUTHOR a ON b.author_id = a.author_id
            INNER JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
            INNER JOIN CATEGORY c ON b.category_id = c.category_id
            ORDER BY {sort_options[sort_by]} {sort_order.upper()}
        """)

        books = lab4_fetch_all(cursor)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_catalogue.html",
        name=session["name"],
        books=books,
        sort_by=sort_by,
        sort_order=sort_order
    )


@app.route("/library-lab4/reports")
@login_required
def lab4_reports():
    conn = cursor = None
    category_stats, author_stats, price_stats = [], [], {}
    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.category_id, c.name AS category_name,
                   COUNT(b.book_id) AS books_count,
                   AVG(b.price) AS average_price
            FROM CATEGORY c
            LEFT JOIN BOOK b ON c.category_id = b.category_id
            GROUP BY c.category_id, c.name
            ORDER BY c.name
        """)
        category_stats = lab4_fetch_all(cursor)

        cursor.execute("""
            SELECT a.author_id, a.name AS author_name,
                   COUNT(b.book_id) AS books_count
            FROM AUTHOR a
            INNER JOIN BOOK b ON a.author_id = b.author_id
            GROUP BY a.author_id, a.name
            HAVING COUNT(b.book_id) >= 2
            ORDER BY books_count DESC, a.name
        """)
        author_stats = lab4_fetch_all(cursor)

        cursor.execute("""
            SELECT COUNT(*) AS total_books,
                   SUM(price) AS total_price,
                   MIN(price) AS minimum_price,
                   MAX(price) AS maximum_price,
                   AVG(price) AS average_price
            FROM BOOK
        """)
        row = cursor.fetchone()
        price_stats = dict(zip([c[0] for c in cursor.description], row))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_reports.html", name=session["name"],
        category_stats=category_stats, author_stats=author_stats,
        price_stats=price_stats
    )



@app.route("/library-lab4/loans")
@login_required
def lab4_loans():

    conn = cursor = None
    history = []
    outstanding = []
    inactive_members = []
    unborrowed_books = []

    # Get the selected history filter
    status_filter = request.args.get("status", "all").lower()

    if status_filter not in ("all", "returned", "not_returned"):
        status_filter = "all"

    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        # Get complete borrowing history
        cursor.execute("""
            SELECT
                l.loan_id,
                b.book_id,
                b.title AS book_title,
                m.member_id,
                m.name AS member_name,
                m.email,
                l.loan_date,
                l.return_date
            FROM LOAN l
            INNER JOIN BOOK b ON l.book_id = b.book_id
            INNER JOIN MEMBER m ON l.member_id = m.member_id
            ORDER BY l.loan_date DESC, l.loan_id DESC
        """)

        all_history = lab4_fetch_all(cursor)

        # Keep all outstanding loans for the return section
        outstanding = [
            row for row in all_history
            if row["return_date"] is None
        ]

        # Apply the selected history filter
        if status_filter == "returned":
            history = [
                row for row in all_history
                if row["return_date"] is not None
            ]

        elif status_filter == "not_returned":
            history = outstanding

        else:
            history = all_history

        # Members who have never borrowed
        cursor.execute("""
            SELECT m.member_id, m.name, m.email
            FROM MEMBER m
            LEFT JOIN LOAN l ON m.member_id = l.member_id
            WHERE l.loan_id IS NULL
            ORDER BY m.name
        """)

        inactive_members = lab4_fetch_all(cursor)

        # Books that have never been borrowed
        cursor.execute("""
            SELECT b.book_id, b.title
            FROM BOOK b
            LEFT JOIN LOAN l ON b.book_id = l.book_id
            WHERE l.loan_id IS NULL
            ORDER BY b.title
        """)

        unborrowed_books = lab4_fetch_all(cursor)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_loans.html",
        name=session["name"],
        history=history,
        outstanding=outstanding,
        inactive_members=inactive_members,
        unborrowed_books=unborrowed_books,
        status_filter=status_filter,
        updated=request.args.get("updated")
    )


@app.route("/library-lab4/loans/<int:loan_id>/return", methods=["POST"])
@login_required
def lab4_return_book(loan_id):

    conn = cursor = None
    updated = False

    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        # Mark the book as returned and record today's date
        cursor.execute("""
            UPDATE LOAN
            SET return_date = CAST(GETDATE() AS DATE)
            WHERE loan_id = ?
              AND return_date IS NULL
        """, (loan_id,))

        updated = cursor.rowcount > 0

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Updating book return failed")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(
        url_for(
            "lab4_loans",
            updated="1" if updated else "0"
        )
    )


@app.route("/library-lab4/most-borrowed")
@login_required
def lab4_most_borrowed():
    conn = cursor = None
    popular_books, top_members = [], []
    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT TOP 3 b.book_id, b.title,
                   COUNT(l.loan_id) AS loans_count
            FROM BOOK b
            INNER JOIN LOAN l ON b.book_id = l.book_id
            GROUP BY b.book_id, b.title
            ORDER BY COUNT(l.loan_id) DESC, b.title
        """)
        popular_books = lab4_fetch_all(cursor)

        cursor.execute("""
            SELECT TOP 1 m.member_id, m.name, m.email,
                   COUNT(l.loan_id) AS loans_count
            FROM MEMBER m
            INNER JOIN LOAN l ON m.member_id = l.member_id
            GROUP BY m.member_id, m.name, m.email
            ORDER BY COUNT(l.loan_id) DESC, m.name
        """)
        top_members = lab4_fetch_all(cursor)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_most_borrowed.html", name=session["name"],
        popular_books=popular_books, top_members=top_members
    )


@app.route("/library-lab4/authors")
@login_required
def lab4_authors():
    conn = cursor = None
    author_stats, same_country_books = [], []
    try:
        conn = get_library_lab4_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.author_id, a.name AS author_name, a.country,
                   COUNT(b.book_id) AS books_count
            FROM AUTHOR a
            LEFT JOIN BOOK b ON a.author_id = b.author_id
            GROUP BY a.author_id, a.name, a.country
            ORDER BY books_count DESC, a.name
        """)
        author_stats = lab4_fetch_all(cursor)

        cursor.execute("""
            SELECT b.book_id, b.title,
                   a.name AS author_name, a.country AS author_country,
                   p.name AS publisher_name, p.country AS publisher_country
            FROM BOOK b
            INNER JOIN AUTHOR a ON b.author_id = a.author_id
            INNER JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
            WHERE a.country = p.country
            ORDER BY b.title
        """)
        same_country_books = lab4_fetch_all(cursor)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "lab4_authors.html", name=session["name"],
        author_stats=author_stats, same_country_books=same_country_books
    )



if __name__ == "__main__":
    app.run(debug=True)
