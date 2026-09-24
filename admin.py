import tkinter as tk
from tkinter import ttk, messagebox


class AdminLogin:
    """
    Admin Login Window
    Username: admin
    Password: admin123
    """

    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        # -----------------------------
        # Window Settings
        # -----------------------------
        self.root.title("Admin Login - Library Management System")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        # -----------------------------
        # Colors
        # -----------------------------
        self.bg_color = "#f4f7fb"
        self.primary_color = "#1f4e79"
        self.secondary_color = "#2e75b6"
        self.white = "#ffffff"
        self.text_color = "#333333"

        self.root.configure(bg=self.bg_color)

        # -----------------------------
        # Main Container
        # -----------------------------
        self.main_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )
        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # -----------------------------
        # Login Card
        # -----------------------------
        self.login_card = tk.Frame(
            self.main_frame,
            bg=self.white,
            bd=0,
            highlightthickness=1,
            highlightbackground="#d9e2ec"
        )

        self.login_card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=430,
            height=480
        )

        # -----------------------------
        # Header
        # -----------------------------
        header = tk.Frame(
            self.login_card,
            bg=self.primary_color,
            height=100
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="LIBRARY MANAGEMENT SYSTEM",
            font=("Arial", 16, "bold"),
            fg=self.white,
            bg=self.primary_color
        )

        title.pack(
            pady=(22, 5)
        )

        subtitle = tk.Label(
            header,
            text="Administrator Login",
            font=("Arial", 11),
            fg="#eaf2f8",
            bg=self.primary_color
        )

        subtitle.pack()

        # -----------------------------
        # Login Content
        # -----------------------------
        content = tk.Frame(
            self.login_card,
            bg=self.white
        )

        content.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=30
        )

        # Username Label
        username_label = tk.Label(
            content,
            text="Username",
            font=("Arial", 11, "bold"),
            fg=self.text_color,
            bg=self.white
        )

        username_label.pack(
            anchor="w",
            pady=(0, 7)
        )

        # Username Entry
        self.username_entry = ttk.Entry(
            content,
            font=("Arial", 12)
        )

        self.username_entry.pack(
            fill="x",
            ipady=8
        )

        # Password Label
        password_label = tk.Label(
            content,
            text="Password",
            font=("Arial", 11, "bold"),
            fg=self.text_color,
            bg=self.white
        )

        password_label.pack(
            anchor="w",
            pady=(20, 7)
        )

        # Password Entry
        self.password_entry = ttk.Entry(
            content,
            font=("Arial", 12),
            show="*"
        )

        self.password_entry.pack(
            fill="x",
            ipady=8
        )

        # Show Password
        self.show_password = tk.BooleanVar(
            value=False
        )

        show_password_check = tk.Checkbutton(
            content,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            font=("Arial", 9),
            bg=self.white,
            activebackground=self.white
        )

        show_password_check.pack(
            anchor="w",
            pady=(8, 5)
        )

        # Login Button
        login_button = tk.Button(
            content,
            text="LOGIN",
            command=self.login,
            font=("Arial", 11, "bold"),
            bg=self.secondary_color,
            fg=self.white,
            activebackground=self.primary_color,
            activeforeground=self.white,
            relief="flat",
            cursor="hand2"
        )

        login_button.pack(
            fill="x",
            ipady=10,
            pady=(20, 10)
        )

        # Exit Button
        exit_button = tk.Button(
            content,
            text="EXIT",
            command=self.exit_application,
            font=("Arial", 10),
            bg="#eeeeee",
            fg="#333333",
            activebackground="#dddddd",
            relief="flat",
            cursor="hand2"
        )

        exit_button.pack(
            fill="x",
            ipady=7
        )

        # -----------------------------
        # Default Focus
        # -----------------------------
        self.username_entry.focus()

        # Enter key
        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

        # Escape key
        self.root.bind(
            "<Escape>",
            lambda event: self.exit_application()
        )

    # ==================================================
    # SHOW / HIDE PASSWORD
    # ==================================================

    def toggle_password(self):

        if self.show_password.get():
            self.password_entry.config(
                show=""
            )
        else:
            self.password_entry.config(
                show="*"
            )

    # ==================================================
    # LOGIN
    # ==================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Empty fields
        if not username:
            messagebox.showwarning(
                "Login",
                "Please enter username."
            )

            self.username_entry.focus()
            return

        if not password:
            messagebox.showwarning(
                "Login",
                "Please enter password."
            )

            self.password_entry.focus()
            return

        # -----------------------------
        # Admin Credentials
        # -----------------------------
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin123"

        # Check Login
        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            messagebox.showinfo(
                "Login Successful",
                "Welcome Admin!"
            )

            # Remove login screen
            self.main_frame.destroy()

            # Open Dashboard
            self.on_success()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

            self.password_entry.delete(
                0,
                tk.END
            )

            self.password_entry.focus()

    # ==================================================
    # EXIT
    # ==================================================

    def exit_application(self):

        result = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if result:
            self.root.destroy()


# ======================================================
# TESTING
# ======================================================

if __name__ == "__main__":

    def test_login_success():
        messagebox.showinfo(
            "Success",
            "Admin login successful!"
        )

    root = tk.Tk()

    AdminLogin(
        root,
        test_login_success
    )

    root.mainloop()
    