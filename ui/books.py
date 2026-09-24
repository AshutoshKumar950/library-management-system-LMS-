import tkinter as tk
from tkinter import ttk, messagebox


from models.book import Book

from services.book_service import (
    add_book,
    get_books,
    get_book,
    update_book,
    delete_book,
)


class BooksWindow:

    def __init__(self, parent, refresh_dashboard):

        self.parent = parent
        self.refresh_dashboard = refresh_dashboard

        self.selected_id = None

        # =================================================
        # WINDOW
        # =================================================

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Library Management System - Books"
        )

        self.window.geometry(
            "1150x720"
        )

        self.window.minsize(
            1000,
            650
        )

        self.window.configure(
            bg="#F4F7FB"
        )

        self.window.transient(parent)

        # =================================================
        # STYLE
        # =================================================

        self.setup_style()

        # =================================================
        # BUILD UI
        # =================================================

        self.build_ui()

        # =================================================
        # LOAD BOOKS
        # =================================================

        self.load_books()

    # =====================================================
    # STYLE
    # =====================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Main labels
        style.configure(
            "Main.TLabel",
            background="#F4F7FB",
            foreground="#172033",
            font=("Segoe UI", 10),
        )

        # Card
        style.configure(
            "Card.TLabelframe",
            background="#FFFFFF",
            foreground="#172033",
            borderwidth=1,
            relief="solid",
        )

        style.configure(
            "Card.TLabelframe.Label",
            background="#FFFFFF",
            foreground="#173F8A",
            font=("Segoe UI", 12, "bold"),
        )

        # Entry
        style.configure(
            "Modern.TEntry",
            padding=8,
            font=("Segoe UI", 10),
        )

        # Buttons
        style.configure(
            "Add.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
            foreground="#FFFFFF",
            background="#198754",
        )

        style.map(
            "Add.TButton",
            background=[
                ("active", "#146C43"),
            ],
        )

        style.configure(
            "Update.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
            foreground="#FFFFFF",
            background="#0D6EFD",
        )

        style.map(
            "Update.TButton",
            background=[
                ("active", "#0B5ED7"),
            ],
        )

        style.configure(
            "Delete.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
            foreground="#FFFFFF",
            background="#DC3545",
        )

        style.map(
            "Delete.TButton",
            background=[
                ("active", "#BB2D3B"),
            ],
        )

        style.configure(
            "Clear.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
            foreground="#172033",
            background="#E9ECEF",
        )

        style.map(
            "Clear.TButton",
            background=[
                ("active", "#DEE2E6"),
            ],
        )

        style.configure(
            "Search.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 7),
            foreground="#FFFFFF",
            background="#6F42C1",
        )

        style.map(
            "Search.TButton",
            background=[
                ("active", "#59359A"),
            ],
        )

        # Treeview
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#172033",
            rowheight=34,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            background="#173F8A",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )

        style.map(
            "Treeview",
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
            height=75,
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # Left title
        title_frame = tk.Frame(
            header,
            bg="#173F8A",
        )

        title_frame.pack(
            side="left",
            padx=25,
            pady=12,
        )

        tk.Label(
            title_frame,
            text="📚  Library Management System",
            bg="#173F8A",
            fg="#FFFFFF",
            font=("Segoe UI", 18, "bold"),
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Manage your library books",
            bg="#173F8A",
            fg="#DCE9FF",
            font=("Segoe UI", 9),
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # =================================================
        # MAIN CONTENT
        # =================================================

        content = tk.Frame(
            self.window,
            bg="#F4F7FB",
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=18,
        )

        # =================================================
        # BOOK DETAILS CARD
        # =================================================

        form = ttk.LabelFrame(
            content,
            text="  📖 Book Details  ",
            style="Card.TLabelframe",
            padding=18,
        )

        form.pack(
            fill="x",
            pady=(0, 15),
        )

        # Grid configuration
        form.columnconfigure(
            1,
            weight=1,
        )

        form.columnconfigure(
            3,
            weight=1,
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        ttk.Label(
            form,
            text="Book Title",
            style="Main.TLabel",
        ).grid(
            row=0,
            column=0,
            padx=(5, 10),
            pady=8,
            sticky="w",
        )

        self.entries = {}

        self.entries["title"] = ttk.Entry(
            form,
            style="Modern.TEntry",
            width=35,
        )

        self.entries["title"].grid(
            row=0,
            column=1,
            padx=5,
            pady=8,
            sticky="ew",
        )

        # -------------------------------------------------
        # AUTHOR
        # -------------------------------------------------

        ttk.Label(
            form,
            text="Author",
            style="Main.TLabel",
        ).grid(
            row=0,
            column=2,
            padx=(20, 10),
            pady=8,
            sticky="w",
        )

        self.entries["author"] = ttk.Entry(
            form,
            style="Modern.TEntry",
            width=35,
        )

        self.entries["author"].grid(
            row=0,
            column=3,
            padx=5,
            pady=8,
            sticky="ew",
        )

        # -------------------------------------------------
        # ISBN
        # -------------------------------------------------

        ttk.Label(
            form,
            text="ISBN",
            style="Main.TLabel",
        ).grid(
            row=1,
            column=0,
            padx=(5, 10),
            pady=8,
            sticky="w",
        )

        self.entries["isbn"] = ttk.Entry(
            form,
            style="Modern.TEntry",
            width=35,
        )

        self.entries["isbn"].grid(
            row=1,
            column=1,
            padx=5,
            pady=8,
            sticky="ew",
        )

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        ttk.Label(
            form,
            text="Category",
            style="Main.TLabel",
        ).grid(
            row=1,
            column=2,
            padx=(20, 10),
            pady=8,
            sticky="w",
        )

        self.entries["category"] = ttk.Entry(
            form,
            style="Modern.TEntry",
            width=35,
        )

        self.entries["category"].grid(
            row=1,
            column=3,
            padx=5,
            pady=8,
            sticky="ew",
        )

        # -------------------------------------------------
        # QUANTITY
        # -------------------------------------------------

        ttk.Label(
            form,
            text="Quantity",
            style="Main.TLabel",
        ).grid(
            row=2,
            column=0,
            padx=(5, 10),
            pady=8,
            sticky="w",
        )

        self.entries["quantity"] = ttk.Entry(
            form,
            style="Modern.TEntry",
            width=15,
        )

        self.entries["quantity"].grid(
            row=2,
            column=1,
            padx=5,
            pady=8,
            sticky="w",
        )

        self.entries["quantity"].insert(
            0,
            "1"
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = tk.Frame(
            form,
            bg="#FFFFFF",
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=(15, 5),
        )

        ttk.Button(
            button_frame,
            text="＋ Add Book",
            style="Add.TButton",
            command=self.add,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="✎ Update Book",
            style="Update.TButton",
            command=self.update,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="✕ Delete Book",
            style="Delete.TButton",
            command=self.delete,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="↻ Clear",
            style="Clear.TButton",
            command=self.clear,
        ).pack(
            side="left",
            padx=5,
        )

        # =================================================
        # SEARCH CARD
        # =================================================

        search_card = tk.Frame(
            content,
            bg="#FFFFFF",
            highlightbackground="#E0E6EF",
            highlightthickness=1,
        )

        search_card.pack(
            fill="x",
            pady=(0, 12),
        )

        tk.Label(
            search_card,
            text="🔍 Search Books",
            bg="#FFFFFF",
            fg="#173F8A",
            font=("Segoe UI", 11, "bold"),
        ).pack(
            side="left",
            padx=(15, 10),
            pady=12,
        )

        self.search_entry = ttk.Entry(
            search_card,
            style="Modern.TEntry",
            width=40,
        )

        self.search_entry.pack(
            side="left",
            padx=5,
            pady=8,
        )

        ttk.Button(
            search_card,
            text="Search",
            style="Search.TButton",
            command=self.load_books,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            search_card,
            text="Show All",
            style="Clear.TButton",
            command=self.show_all,
        ).pack(
            side="left",
            padx=5,
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.load_books()
        )

        # =================================================
        # TABLE CARD
        # =================================================

        table_card = tk.Frame(
            content,
            bg="#FFFFFF",
            highlightbackground="#E0E6EF",
            highlightthickness=1,
        )

        table_card.pack(
            fill="both",
            expand=True,
        )

        # Table title
        table_header = tk.Frame(
            table_card,
            bg="#FFFFFF",
        )

        table_header.pack(
            fill="x",
        )

        tk.Label(
            table_header,
            text="📚 Book Collection",
            bg="#FFFFFF",
            fg="#173F8A",
            font=("Segoe UI", 12, "bold"),
        ).pack(
            side="left",
            padx=15,
            pady=12,
        )

        tk.Label(
            table_header,
            text="Click a book to edit or delete",
            bg="#FFFFFF",
            fg="#6C757D",
            font=("Segoe UI", 9),
        ).pack(
            side="right",
            padx=15,
            pady=12,
        )

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        table_frame = tk.Frame(
            table_card,
            bg="#FFFFFF",
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12),
        )

        columns = (
            "id",
            "title",
            "author",
            "isbn",
            "category",
            "quantity",
            "available",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id": "ID",
            "title": "Book Title",
            "author": "Author",
            "isbn": "ISBN",
            "category": "Category",
            "quantity": "Quantity",
            "available": "Available",
        }

        widths = {
            "id": 55,
            "title": 220,
            "author": 170,
            "isbn": 150,
            "category": 130,
            "quantity": 90,
            "available": 100,
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column],
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center",
            )

        # -------------------------------------------------
        # SCROLLBAR
        # -------------------------------------------------

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        # -------------------------------------------------
        # SELECTION
        # -------------------------------------------------

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_book,
        )

        self.tree.bind(
            "<Double-1>",
            self.select_book,
        )

        # Mouse click
        self.tree.bind(
            "<ButtonRelease-1>",
            self.mouse_select_book,
        )

        # =================================================
        # FOOTER
        # =================================================

        footer = tk.Frame(
            self.window,
            bg="#E9EFF7",
            height=32,
        )

        footer.pack(
            fill="x",
        )

        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="Library Management System  •  Book Management",
            bg="#E9EFF7",
            fg="#526173",
            font=("Segoe UI", 8),
        ).pack(
            side="left",
            padx=20,
            pady=7,
        )

    # =====================================================
    # GET BOOK DATA
    # =====================================================

    def get_book_data(self):

        title = self.entries["title"].get().strip()

        author = self.entries["author"].get().strip()

        isbn = self.entries["isbn"].get().strip()

        category = self.entries["category"].get().strip()

        quantity_text = (
            self.entries["quantity"]
            .get()
            .strip()
        )

        try:

            quantity = int(quantity_text)

        except ValueError:

            raise ValueError(
                "Quantity must be a number."
            )

        if not title:

            raise ValueError(
                "Book title is required."
            )

        if not author:

            raise ValueError(
                "Author name is required."
            )

        if quantity < 1:

            raise ValueError(
                "Quantity must be at least 1."
            )

        return Book(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            quantity=quantity,
        )

    # =====================================================
    # ADD
    # =====================================================

    def add(self):

        try:

            book = self.get_book_data()

            add_book(book)

            messagebox.showinfo(
                "Success",
                "Book added successfully.",
            )

            self.clear()

            self.load_books()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Add Book Error",
                str(exc),
            )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Book",
                "Please select a book from the table first.",
            )

            return

        try:

            book = self.get_book_data()

            update_book(
                self.selected_id,
                book,
            )

            messagebox.showinfo(
                "Success",
                "Book updated successfully.",
            )

            self.selected_id = None

            self.load_books()

            self.clear_form_only()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Update Book Error",
                str(exc),
            )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Book",
                "Please select a book from the table first.",
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this book?",
        )

        if not answer:

            return

        try:

            delete_book(
                self.selected_id
            )

            messagebox.showinfo(
                "Success",
                "Book deleted successfully.",
            )

            self.selected_id = None

            self.clear_form_only()

            self.load_books()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Delete Book Error",
                str(exc),
            )

    # =====================================================
    # LOAD BOOKS
    # =====================================================

    def load_books(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        search = (
            self.search_entry
            .get()
            .strip()
        )

        books = get_books(search)

        for book in books:

            self.tree.insert(
                "",
                "end",
                values=(
                    book["id"],
                    book["title"],
                    book["author"],
                    book["isbn"] or "",
                    book["category"] or "",
                    book["quantity"],
                    book["available"],
                ),
            )

    # =====================================================
    # SHOW ALL
    # =====================================================

    def show_all(self):

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.load_books()

    # =====================================================
    # SELECT BOOK
    # =====================================================

    def select_book(self, event=None):

        selection = self.tree.selection()

        if not selection:

            return

        selected_item = selection[0]

        values = self.tree.item(
            selected_item,
            "values",
        )

        if not values:

            return

        try:

            book_id = int(values[0])

        except (ValueError, TypeError):

            messagebox.showerror(
                "Error",
                "Invalid book ID.",
            )

            return

        try:

            book = get_book(book_id)

        except Exception as exc:

            messagebox.showerror(
                "Error",
                f"Unable to load book:\n{exc}",
            )

            return

        if not book:

            messagebox.showerror(
                "Error",
                "Selected book was not found.",
            )

            return

        # Save selected ID
        self.selected_id = book_id

        # Fill form
        self.set_entry(
            "title",
            book["title"],
        )

        self.set_entry(
            "author",
            book["author"],
        )

        self.set_entry(
            "isbn",
            book["isbn"] or "",
        )

        self.set_entry(
            "category",
            book["category"] or "",
        )

        self.set_entry(
            "quantity",
            book["quantity"],
        )

    # =====================================================
    # MOUSE SELECT
    # =====================================================

    def mouse_select_book(self, event=None):

        if event is None:

            return

        item = self.tree.identify_row(
            event.y
        )

        if not item:

            return

        self.tree.selection_set(item)

        self.tree.focus(item)

        self.select_book()

    # =====================================================
    # SET ENTRY
    # =====================================================

    def set_entry(self, field, value):

        entry = self.entries[field]

        entry.delete(
            0,
            tk.END,
        )

        entry.insert(
            0,
            str(value),
        )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form_only(self):

        for entry in self.entries.values():

            entry.delete(
                0,
                tk.END,
            )

        self.entries["quantity"].insert(
            0,
            "1",
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.selected_id = None

        self.clear_form_only()

        for item in self.tree.selection():

            self.tree.selection_remove(item)

        self.entries["title"].focus()
        