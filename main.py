import tkinter as tk

from database.db import initialize_database
from ui.dashboard import Dashboard
from admin import AdminLogin


def open_dashboard(root):
    """
    Open the main library dashboard
    after successful admin login.
    """

    Dashboard(root)


def main():

    # -----------------------------------------
    # Initialize SQLite Database
    # -----------------------------------------
    initialize_database()

    # -----------------------------------------
    # Create Main Window
    # -----------------------------------------
    root = tk.Tk()

    root.title(
        "Library Management System"
    )

    root.geometry(
        "1100x700"
    )

    root.minsize(
        950,
        600
    )

    # -----------------------------------------
    # Open Admin Login
    # -----------------------------------------
    AdminLogin(
        root,
        lambda: open_dashboard(root)
    )

    # -----------------------------------------
    # Start Application
    # -----------------------------------------
    root.mainloop()


if __name__ == "__main__":
    main()
    