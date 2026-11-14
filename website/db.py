
import pyodbc


def get_connection():
    """Connect to the registration database."""
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=registration;"
        "Trusted_Connection=yes;"
    )


def get_library_connection():
    """Connect to the old library database."""
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=library;"
        "Trusted_Connection=yes;"
    )


def get_library_lab4_connection():
    """Connect to the new Lab 4 library database."""
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=library_lab4;"
        "Trusted_Connection=yes;"
    )
