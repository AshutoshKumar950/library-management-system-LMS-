import tkinter as tk
from tkinter import ttk, messagebox

from models.member import Member
from services.member_service import (
    add_member,
    get_members,
    get_member,
    update_member,
    delete_member,
)


class MembersWindow:

    def __init__(self, parent, refresh_dashboard):

        self.parent = parent
        self.refresh_dashboard = refresh_dashboard

        self.selected_id = None

        # =================================================
        # WINDOW
        # =================================================

        self.window = tk.Toplevel(parent)
        self.window.title("Manage Members")
        self.window.geometry("1150x750")
        self.window.minsize(1000, 650)
        self.window.configure(bg="#F4F7FB")
        self.window.transient(parent)

        self.setup_style()
        self.build_ui()
        self.load_members()

    # =====================================================
    # STYLE
    # =====================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        # -------------------------------------------------
        # Labels
        # -------------------------------------------------

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

        style.configure(
            "Section.TLabel",
            background="white",
            foreground="#173F8A",
            font=("Segoe UI", 13, "bold"),
        )

        style.configure(
            "Card.TLabel",
            background="white",
            foreground="#263238",
            font=("Segoe UI", 10),
        )

        # -------------------------------------------------
        # Entry
        # -------------------------------------------------

        style.configure(
            "Modern.TEntry",
            padding=8,
            font=("Segoe UI", 10),
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        style.configure(
            "Add.TButton",
            background="#16A085",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            borderwidth=0,
        )

        style.map(
            "Add.TButton",
            background=[
                ("active", "#12876F"),
            ],
        )

        style.configure(
            "Update.TButton",
            background="#2980B9",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            borderwidth=0,
        )

        style.map(
            "Update.TButton",
            background=[
                ("active", "#21618C"),
            ],
        )

        style.configure(
            "Delete.TButton",
            background="#E74C3C",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            borderwidth=0,
        )

        style.map(
            "Delete.TButton",
            background=[
                ("active", "#C0392B"),
            ],
        )

        style.configure(
            "Clear.TButton",
            background="#7F8C8D",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            borderwidth=0,
        )

        style.map(
            "Clear.TButton",
            background=[
                ("active", "#626E70"),
            ],
        )

        style.configure(
            "Search.TButton",
            background="#8E44AD",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8),
            borderwidth=0,
        )

        style.map(
            "Search.TButton",
            background=[
                ("active", "#71368A"),
            ],
        )

        # -------------------------------------------------
        # Treeview
        # -------------------------------------------------

        style.configure(
            "Modern.Treeview",
            background="white",
            foreground="#263238",
            fieldbackground="white",
            rowheight=38,
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
            text="👥  Member Management",
            style="Header.TLabel",
        ).pack(
            anchor="w",
        )

        ttk.Label(
            title_frame,
            text="Add, update, delete and manage library members",
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
        # MEMBER DETAILS CARD
        # =================================================

        form_card = tk.Frame(
            main,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1,
        )

        form_card.pack(
            fill="x",
            pady=(0, 18),
        )

        # Card header

        card_header = tk.Frame(
            form_card,
            bg="white",
        )

        card_header.pack(
            fill="x",
            padx=22,
            pady=(18, 12),
        )

        ttk.Label(
            card_header,
            text="👤  Member Details",
            style="Section.TLabel",
        ).pack(
            side="left",
        )

        ttk.Label(
            card_header,
            text="Enter member information below",
            style="Card.TLabel",
        ).pack(
            side="left",
            padx=18,
        )

        # =================================================
        # FORM
        # =================================================

        form = tk.Frame(
            form_card,
            bg="white",
        )

        form.pack(
            fill="x",
            padx=22,
            pady=(0, 18),
        )

        self.entries = {}

        # -----------------------------
        # Name
        # -----------------------------

        ttk.Label(
            form,
            text="Full Name",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(3, 5),
        )

        self.entries["name"] = ttk.Entry(
            form,
            width=32,
            style="Modern.TEntry",
        )

        self.entries["name"].grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 25),
        )

        # -----------------------------
        # Email
        # -----------------------------

        ttk.Label(
            form,
            text="Email",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 12),
            pady=(3, 5),
        )

        self.entries["email"] = ttk.Entry(
            form,
            width=32,
            style="Modern.TEntry",
        )

        self.entries["email"].grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 25),
        )

        # -----------------------------
        # Phone
        # -----------------------------

        ttk.Label(
            form,
            text="Phone Number",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 12),
            pady=(3, 5),
        )

        self.entries["phone"] = ttk.Entry(
            form,
            width=25,
            style="Modern.TEntry",
        )

        self.entries["phone"].grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(0, 25),
        )

        # -----------------------------
        # Address
        # -----------------------------

        ttk.Label(
            form,
            text="Address",
            style="Card.TLabel",
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=0,
            column=3,
            sticky="w",
            pady=(3, 5),
        )

        self.entries["address"] = ttk.Entry(
            form,
            width=30,
            style="Modern.TEntry",
        )

        self.entries["address"].grid(
            row=1,
            column=3,
            sticky="ew",
        )

        # Column resizing

        form.columnconfigure(
            0,
            weight=2,
        )

        form.columnconfigure(
            1,
            weight=2,
        )

        form.columnconfigure(
            2,
            weight=1,
        )

        form.columnconfigure(
            3,
            weight=2,
        )

        # =================================================
        # BUTTON BAR
        # =================================================

        button_bar = tk.Frame(
            form_card,
            bg="white",
        )

        button_bar.pack(
            fill="x",
            padx=22,
            pady=(0, 20),
        )

        ttk.Button(
            button_bar,
            text="✓  Add Member",
            command=self.add,
            style="Add.TButton",
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            button_bar,
            text="✎  Update Member",
            command=self.update,
            style="Update.TButton",
        ).pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            button_bar,
            text="🗑  Delete Member",
            command=self.delete,
            style="Delete.TButton",
        ).pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            button_bar,
            text="✕  Clear",
            command=self.clear,
            style="Clear.TButton",
        ).pack(
            side="left",
            padx=8,
        )

        # =================================================
        # SEARCH CARD
        # =================================================

        search_card = tk.Frame(
            main,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1,
        )

        search_card.pack(
            fill="x",
            pady=(0, 15),
        )

        search_frame = tk.Frame(
            search_card,
            bg="white",
        )

        search_frame.pack(
            fill="x",
            padx=18,
            pady=13,
        )

        ttk.Label(
            search_frame,
            text="🔎  Search Members",
            style="Section.TLabel",
        ).pack(
            side="left",
            padx=(0, 20),
        )

        self.search_entry = ttk.Entry(
            search_frame,
            width=42,
            style="Modern.TEntry",
        )

        self.search_entry.pack(
            side="left",
        )

        ttk.Button(
            search_frame,
            text="🔍  Search",
            command=self.load_members,
            style="Search.TButton",
        ).pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.show_all,
            style="Clear.TButton",
        ).pack(
            side="left",
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.load_members(),
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

        # Table heading

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
            text="📋  Members List",
            style="Section.TLabel",
        ).pack(
            side="left",
        )

        ttk.Label(
            table_header,
            text="Click a member to edit or delete",
            style="Card.TLabel",
        ).pack(
            side="right",
        )

        # =================================================
        # TABLE
        # =================================================

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
            "name",
            "email",
            "phone",
            "address",
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
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "address": "Address",
        }

        widths = {
            "id": 70,
            "name": 210,
            "email": 260,
            "phone": 160,
            "address": 300,
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column],
            )

            self.tree.column(
                column,
                width=widths[column],
                minwidth=70,
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
        # SELECTION EVENTS
        # =================================================

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_member,
        )

        self.tree.bind(
            "<Double-1>",
            self.select_member,
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.mouse_select_member,
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

        tk.Label(
            footer,
            text="Library Management System  •  Member Management",
            bg="#EAF0F8",
            fg="#607D8B",
            font=("Segoe UI", 9),
        ).pack(
            side="left",
            padx=25,
        )

    # =====================================================
    # GET MEMBER DATA
    # =====================================================

    def get_member_data(self):

        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        address = self.entries["address"].get().strip()

        if not name:
            raise ValueError(
                "Member name is required."
            )

        if not email:
            raise ValueError(
                "Email is required."
            )

        if not phone:
            raise ValueError(
                "Phone number is required."
            )

        return Member(
            name=name,
            email=email,
            phone=phone,
            address=address,
        )

    # =====================================================
    # ADD MEMBER
    # =====================================================

    def add(self):

        try:

            member = self.get_member_data()

            add_member(member)

            messagebox.showinfo(
                "Success",
                "Member added successfully.",
            )

            self.clear()

            self.load_members()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Add Member Error",
                str(exc),
            )

    # =====================================================
    # UPDATE MEMBER
    # =====================================================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Member",
                "Please select a member from the table first.",
            )

            return

        try:

            member = self.get_member_data()

            update_member(
                self.selected_id,
                member,
            )

            messagebox.showinfo(
                "Success",
                "Member updated successfully.",
            )

            self.selected_id = None

            self.clear_form_only()

            self.load_members()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Update Member Error",
                str(exc),
            )

    # =====================================================
    # DELETE MEMBER
    # =====================================================

    def delete(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Member",
                "Please select a member from the table first.",
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this member?",
        )

        if not answer:
            return

        try:

            delete_member(
                self.selected_id
            )

            messagebox.showinfo(
                "Success",
                "Member deleted successfully.",
            )

            self.selected_id = None

            self.clear_form_only()

            self.load_members()

            self.refresh_dashboard()

        except Exception as exc:

            messagebox.showerror(
                "Delete Member Error",
                str(exc),
            )

    # =====================================================
    # LOAD MEMBERS
    # =====================================================

    def load_members(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_entry.get().strip()

        try:

            members = get_members(search)

            for index, member in enumerate(members):

                item_id = self.tree.insert(
                    "",
                    "end",
                    values=(
                        member["id"],
                        member["name"],
                        member["email"],
                        member["phone"],
                        member["address"] or "",
                    ),
                )

                # Alternating rows
                if index % 2 == 0:

                    self.tree.item(
                        item_id,
                        tags=("even",),
                    )

                else:

                    self.tree.item(
                        item_id,
                        tags=("odd",),
                    )

            self.tree.tag_configure(
                "even",
                background="#F8FAFD",
            )

            self.tree.tag_configure(
                "odd",
                background="white",
            )

            self.selected_id = None

        except Exception as exc:

            messagebox.showerror(
                "Load Members Error",
                str(exc),
            )

    # =====================================================
    # SELECT MEMBER
    # =====================================================

    def select_member(self, event=None):

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

            member_id = int(values[0])

        except (ValueError, TypeError):

            messagebox.showerror(
                "Error",
                "Invalid member ID.",
            )

            return

        try:

            member = get_member(member_id)

        except Exception as exc:

            messagebox.showerror(
                "Error",
                f"Unable to load member:\n{exc}",
            )

            return

        if not member:

            messagebox.showerror(
                "Error",
                "Selected member was not found.",
            )

            return

        self.selected_id = member_id

        self.set_entry(
            "name",
            member["name"],
        )

        self.set_entry(
            "email",
            member["email"],
        )

        self.set_entry(
            "phone",
            member["phone"],
        )

        self.set_entry(
            "address",
            member["address"] or "",
        )

    # =====================================================
    # MOUSE SELECT
    # =====================================================

    def mouse_select_member(self, event=None):

        if event is None:
            return

        item = self.tree.identify_row(
            event.y
        )

        if not item:
            return

        self.tree.selection_set(item)

        self.tree.focus(item)

        self.select_member()

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
    # CLEAR FORM ONLY
    # =====================================================

    def clear_form_only(self):

        for entry in self.entries.values():

            entry.delete(
                0,
                tk.END,
            )

        self.entries["name"].focus()

    # =====================================================
    # CLEAR EVERYTHING
    # =====================================================

    def clear(self):

        self.selected_id = None

        self.clear_form_only()

        for item in self.tree.selection():

            self.tree.selection_remove(item)

    # =====================================================
    # SHOW ALL
    # =====================================================

    def show_all(self):

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.load_members()
        