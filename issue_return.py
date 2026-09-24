import tkinter as tk
from tkinter import ttk, messagebox

from services.book_service import get_books
from services.member_service import get_members
from services.issue_service import (
    issue_book,
    return_book,
    get_issues,
)


class IssueReturnWindow:

    def __init__(self, parent, refresh_dashboard):

        self.parent = parent
        self.refresh_dashboard = refresh_dashboard

        self.window = tk.Toplevel(parent)
        self.window.title("Issue / Return Books")
        self.window.geometry("1200x750")
        self.window.minsize(1000, 650)
        self.window.configure(bg="#F4F7FB")
        self.window.transient(parent)

        self.books = []
        self.members = []

        self.selected_issue_id = None

        self.setup_style()
        self.build_ui()
        self.load_data()

    # =====================================================
    # STYLE
    # =====================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Main Label
        style.configure(
            "Main.TLabel",
            background="#F4F7FB",
            foreground="#263238",
            font=("Segoe UI", 10),
        )

        # Card Label
        style.configure(
            "Card.TLabel",
            background="white",
            foreground="#263238",
            font=("Segoe UI", 10),
        )

        # Header
        style.configure(
            "Header.TLabel",
            background="#173F8A",
            foreground="white",
            font=("Segoe UI", 20, "bold"),
        )

        style.configure(
            "SubHeader.TLabel",
            background="#173F8A",
            foreground="#DDE8FF",
            font=("Segoe UI", 10),
        )

        # Section title
        style.configure(
            "Section.TLabel",
            background="white",
            foreground="#173F8A",
            font=("Segoe UI", 13, "bold"),
        )

        # Combobox
        style.configure(
            "Modern.TCombobox",
            padding=8,
            font=("Segoe UI", 10),
        )

        # Buttons
        style.configure(
            "Issue.TButton",
            background="#16A085",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10),
            borderwidth=0,
        )

        style.map(
            "Issue.TButton",
            background=[
                ("active", "#12876F"),
            ],
        )

        style.configure(
            "Return.TButton",
            background="#E74C3C",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10),
            borderwidth=0,
        )

        style.map(
            "Return.TButton",
            background=[
                ("active", "#C0392B"),
            ],
        )

        style.configure(
            "Refresh.TButton",
            background="#2980B9",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9),
            borderwidth=0,
        )

        style.map(
            "Refresh.TButton",
            background=[
                ("active", "#21618C"),
            ],
        )

        style.configure(
            "Clear.TButton",
            background="#7F8C8D",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9),
            borderwidth=0,
        )

        style.map(
            "Clear.TButton",
            background=[
                ("active", "#626E70"),
            ],
        )

        # Treeview
        style.configure(
            "Modern.Treeview",
            background="white",
            foreground="#263238",
            rowheight=36,
            fieldbackground="white",
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        style.configure(
            "Modern.Treeview.Heading",
            background="#173F8A",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=10,
        )

        style.map(
            "Modern.Treeview",
            background=[
                ("selected", "#DCE9FF"),
            ],
            foreground=[
                ("selected", "#173F8A"),
            ],
        )

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(
            self.window,
            bg="#173F8A",
            height=90,
        )

        header.pack(
            fill="x",
        )

        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg="#173F8A",
        )

        title_frame.pack(
            side="left",
            padx=30,
            pady=15,
        )

        ttk.Label(
            title_frame,
            text="📚  Issue / Return Books",
            style="Header.TLabel",
        ).pack(
            anchor="w",
        )

        ttk.Label(
            title_frame,
            text="Manage book issue and return records",
            style="SubHeader.TLabel",
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        # =================================================
        # MAIN CONTAINER
        # =================================================

        main = tk.Frame(
            self.window,
            bg="#F4F7FB",
        )

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20,
        )

        # =================================================
        # ISSUE BOOK CARD
        # =================================================

        issue_card = tk.Frame(
            main,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1,
        )

        issue_card.pack(
            fill="x",
            pady=(0, 18),
        )

        # Card title
        title_frame = tk.Frame(
            issue_card,
            bg="white",
        )

        title_frame.pack(
            fill="x",
            padx=22,
            pady=(18, 10),
        )

        ttk.Label(
            title_frame,
            text="📖  Issue New Book",
            style="Section.TLabel",
        ).pack(
            side="left",
        )

        ttk.Label(
            title_frame,
            text="Select a book and member",
            style="Card.TLabel",
        ).pack(
            side="left",
            padx=15,
        )

        # Form
        form = tk.Frame(
            issue_card,
            bg="white",
        )

        form.pack(
            fill="x",
            padx=22,
            pady=(5, 22),
        )

        # Book
        ttk.Label(
            form,
            text="Book",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7,
        )

        self.book_combo = ttk.Combobox(
            form,
            width=48,
            state="readonly",
            style="Modern.TCombobox",
        )

        self.book_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 25),
        )

        # Member
        ttk.Label(
            form,
            text="Member",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 10),
            pady=7,
        )

        self.member_combo = ttk.Combobox(
            form,
            width=40,
            state="readonly",
            style="Modern.TCombobox",
        )

        self.member_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 25),
        )

        # Issue button
        ttk.Button(
            form,
            text="✓  Issue Book",
            command=self.issue,
            style="Issue.TButton",
        ).grid(
            row=1,
            column=2,
            padx=(5, 0),
        )

        form.columnconfigure(
            0,
            weight=3,
        )

        form.columnconfigure(
            1,
            weight=2,
        )

        # =================================================
        # RECORD CONTROL BAR
        # =================================================

        control_card = tk.Frame(
            main,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1,
        )

        control_card.pack(
            fill="x",
            pady=(0, 15),
        )

        control = tk.Frame(
            control_card,
            bg="white",
        )

        control.pack(
            fill="x",
            padx=18,
            pady=14,
        )

        ttk.Label(
            control,
            text="📊  Issue Records",
            style="Section.TLabel",
        ).pack(
            side="left",
            padx=(0, 25),
        )

        ttk.Label(
            control,
            text="Status:",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="left",
        )

        self.status_combo = ttk.Combobox(
            control,
            values=[
                "All",
                "Issued",
                "Returned",
            ],
            state="readonly",
            width=14,
            style="Modern.TCombobox",
        )

        self.status_combo.set("All")

        self.status_combo.pack(
            side="left",
            padx=10,
        )

        self.status_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_records(),
        )

        ttk.Button(
            control,
            text="↻  Refresh",
            command=self.load_data,
            style="Refresh.TButton",
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            control,
            text="↩  Return Selected",
            command=self.return_selected,
            style="Return.TButton",
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            control,
            text="✕  Clear",
            command=self.clear_selection,
            style="Clear.TButton",
        ).pack(
            side="left",
            padx=5,
        )

        # =================================================
        # TABLE CARD
        # =================================================

        table_card = tk.Frame(
            main,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1,
        )

        table_card.pack(
            fill="both",
            expand=True,
        )

        table_header = tk.Frame(
            table_card,
            bg="white",
        )

        table_header.pack(
            fill="x",
            padx=18,
            pady=(15, 8),
        )

        ttk.Label(
            table_header,
            text="📋  Transaction History",
            style="Section.TLabel",
        ).pack(
            side="left",
        )

        ttk.Label(
            table_header,
            text="Select a record to return a book",
            style="Card.TLabel",
        ).pack(
            side="right",
        )

        # Table container
        table_frame = tk.Frame(
            table_card,
            bg="white",
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18),
        )

        columns = (
            "id",
            "book",
            "member",
            "issue_date",
            "return_date",
            "status",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Modern.Treeview",
        )

        headings = {
            "id": "ID",
            "book": "Book",
            "member": "Member",
            "issue_date": "Issue Date",
            "return_date": "Return Date",
            "status": "Status",
        }

        widths = {
            "id": 60,
            "book": 280,
            "member": 220,
            "issue_date": 170,
            "return_date": 170,
            "status": 110,
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column],
            )

            self.tree.column(
                column,
                width=widths[column],
                minwidth=60,
                anchor="center",
            )

        # Vertical scrollbar
        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        # Horizontal scrollbar
        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview,
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        table_frame.rowconfigure(
            0,
            weight=1,
        )

        table_frame.columnconfigure(
            0,
            weight=1,
        )

        # =================================================
        # TREE EVENTS
        # =================================================

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_record,
        )

        self.tree.bind(
            "<Double-1>",
            self.select_record,
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.mouse_select_record,
        )

        # =================================================
        # FOOTER
        # =================================================

        footer = tk.Frame(
            self.window,
            bg="#EAF0F8",
            height=32,
        )

        footer.pack(
            fill="x",
        )

        footer.pack_propagate(False)

        ttk.Label(
            footer,
            text="Library Management System  •  Issue & Return Module",
            background="#EAF0F8",
            foreground="#607D8B",
            font=("Segoe UI", 9),
        ).pack(
            side="left",
            padx=25,
        )

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        try:

            self.books = get_books()
            self.members = get_members()

            # -------------------------------------------------
            # Available Books
            # -------------------------------------------------

            available_books = [
                book
                for book in self.books
                if int(book["available"]) > 0
            ]

            book_values = [
                f'{book["id"]} - {book["title"]} '
                f'(Available: {book["available"]})'
                for book in available_books
            ]

            # -------------------------------------------------
            # Members
            # -------------------------------------------------

            member_values = [
                f'{member["id"]} - {member["name"]}'
                for member in self.members
            ]

            self.book_combo["values"] = book_values
            self.member_combo["values"] = member_values

            # Select first book
            if book_values:
                self.book_combo.current(0)
            else:
                self.book_combo.set("")

            # Select first member
            if member_values:
                self.member_combo.current(0)
            else:
                self.member_combo.set("")

            self.load_records()

        except Exception as exc:

            messagebox.showerror(
                "Load Error",
                str(exc),
            )

    # =====================================================
    # LOAD ISSUE RECORDS
    # =====================================================

    def load_records(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.selected_issue_id = None

        status = self.status_combo.get()

        if status == "All":
            status = None

        try:

            issues = get_issues(status)

            for issue in issues:

                item_id = self.tree.insert(
                    "",
                    "end",
                    values=(
                        issue["id"],
                        issue["book_title"],
                        issue["member_name"],
                        issue["issue_date"],
                        issue["return_date"] or "",
                        issue["status"],
                    ),
                )

                # Alternating row tags
                children = self.tree.get_children()

                if len(children) % 2 == 0:
                    self.tree.item(
                        item_id,
                        tags=("even",),
                    )
                else:
                    self.tree.item(
                        item_id,
                        tags=("odd",),
                    )

            # Row colors
            self.tree.tag_configure(
                "even",
                background="#F8FAFD",
            )

            self.tree.tag_configure(
                "odd",
                background="white",
            )

        except Exception as exc:

            messagebox.showerror(
                "Load Records Error",
                str(exc),
            )

    # =====================================================
    # SELECT RECORD
    # =====================================================

    def select_record(self, event=None):

        selection = self.tree.selection()

        if not selection:
            return

        selected_item = selection[0]

        # Correct way to get values
        values = self.tree.item(
            selected_item,
            "values",
        )

        if not values:
            return

        try:

            issue_id = int(values[0])

        except (ValueError, TypeError):

            messagebox.showerror(
                "Error",
                "Invalid issue ID.",
            )

            return

        self.selected_issue_id = issue_id

    # =====================================================
    # MOUSE SELECT RECORD
    # =====================================================

    def mouse_select_record(self, event=None):

        if event is None:
            return

        item = self.tree.identify_row(
            event.y
        )

        if not item:
            return

        self.tree.selection_set(item)
        self.tree.focus(item)

        self.select_record()

    # =====================================================
    # ISSUE BOOK
    # =====================================================

    def issue(self):

        book_value = self.book_combo.get()
        member_value = self.member_combo.get()

        if not book_value:

            messagebox.showwarning(
                "Book Required",
                "Please select a book.",
            )

            return

        if not member_value:

            messagebox.showwarning(
                "Member Required",
                "Please select a member.",
            )

            return

        try:

            book_id = int(
                book_value.split(
                    " - ",
                    1,
                )[0]
            )

            member_id = int(
                member_value.split(
                    " - ",
                    1,
                )[0]
            )

            issue_book(
                book_id,
                member_id,
            )

            messagebox.showinfo(
                "Success",
                "Book issued successfully.",
            )

            self.selected_issue_id = None

            self.load_data()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Issue Book Error",
                str(exc),
            )

    # =====================================================
    # RETURN SELECTED BOOK
    # =====================================================

    def return_selected(self):

        selection = self.tree.selection()

        if not selection:

            messagebox.showwarning(
                "Select Record",
                "Please select an issued book from the table first.",
            )

            return

        selected_item = selection[0]

        values = self.tree.item(
            selected_item,
            "values",
        )

        if not values:

            messagebox.showwarning(
                "Select Record",
                "Unable to read selected record.",
            )

            return

        try:

            issue_id = int(values[0])

        except (ValueError, TypeError):

            messagebox.showerror(
                "Error",
                "Invalid issue ID.",
            )

            return

        self.selected_issue_id = issue_id

        status = str(values[5]).strip()

        if status.lower() == "returned":

            messagebox.showwarning(
                "Already Returned",
                "This book has already been returned.",
            )

            return

        answer = messagebox.askyesno(
            "Confirm Return",
            "Are you sure you want to return this book?",
        )

        if not answer:
            return

        try:

            return_book(issue_id)

            messagebox.showinfo(
                "Success",
                "Book returned successfully.",
            )

            self.selected_issue_id = None

            self.load_data()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Return Book Error",
                str(exc),
            )

    # =====================================================
    # CLEAR SELECTION
    # =====================================================

    def clear_selection(self):

        self.selected_issue_id = None

        for item in self.tree.selection():

            self.tree.selection_remove(item)
            