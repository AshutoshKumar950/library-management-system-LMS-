import tkinter as tk
from tkinter import ttk

from services.issue_service import get_dashboard_counts
from ui.books import BooksWindow
from ui.members import MembersWindow
from ui.issue_return import IssueReturnWindow


class Dashboard:
    def __init__(self, root):
        self.root = root

        self.setup_window()
        self.setup_style()
        self.build_ui()
        self.refresh()

    # ---------------------------------------------------------
    # WINDOW
    # ---------------------------------------------------------

    def setup_window(self):
        self.root.title("Library Management System")
        self.root.configure(bg="#F5F7FB")

        # Optional default size
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

    # ---------------------------------------------------------
    # STYLE
    # ---------------------------------------------------------

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Main colors
        self.colors = {
            "bg": "#F5F7FB",
            "sidebar": "#172033",
            "sidebar_hover": "#25324A",
            "white": "#FFFFFF",
            "text": "#172033",
            "muted": "#6B7280",
            "primary": "#2563EB",
            "primary_dark": "#1D4ED8",
            "green": "#16A34A",
            "orange": "#EA580C",
            "purple": "#7C3AED",
            "red": "#DC2626",
            "cyan": "#0891B2",
            "border": "#E5E7EB",
        }

        self.root.configure(bg=self.colors["bg"])

        # General labels
        style.configure(
            "Title.TLabel",
            background=self.colors["bg"],
            foreground=self.colors["text"],
            font=("Segoe UI", 24, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.colors["bg"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 10),
        )

        # Sidebar
        style.configure(
            "Sidebar.TFrame",
            background=self.colors["sidebar"],
        )

        style.configure(
            "SidebarTitle.TLabel",
            background=self.colors["sidebar"],
            foreground="#FFFFFF",
            font=("Segoe UI", 18, "bold"),
        )

        style.configure(
            "SidebarSubtitle.TLabel",
            background=self.colors["sidebar"],
            foreground="#9CA3AF",
            font=("Segoe UI", 9),
        )

        # Cards
        style.configure(
            "Card.TFrame",
            background=self.colors["white"],
            relief="flat",
        )

        style.configure(
            "CardTitle.TLabel",
            background=self.colors["white"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 10),
        )

        style.configure(
            "CardValue.TLabel",
            background=self.colors["white"],
            foreground=self.colors["text"],
            font=("Segoe UI", 23, "bold"),
        )

        # Buttons
        style.configure(
            "Refresh.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 8),
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 14),
        )

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar = ttk.Frame(
            self.root,
            style="Sidebar.TFrame",
            width=240,
        )

        self.sidebar.pack(
            side="left",
            fill="y",
        )

        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = ttk.Frame(
            self.sidebar,
            style="Sidebar.TFrame",
            padding=(25, 30),
        )
        logo_frame.pack(fill="x")

        ttk.Label(
            logo_frame,
            text="📚",
            style="SidebarTitle.TLabel",
            font=("Segoe UI Emoji", 28),
        ).pack(anchor="w")

        ttk.Label(
            logo_frame,
            text="Library Manager",
            style="SidebarTitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        ttk.Label(
            logo_frame,
            text="Management System",
            style="SidebarSubtitle.TLabel",
        ).pack(anchor="w")

        # Navigation
        nav_frame = ttk.Frame(
            self.sidebar,
            style="Sidebar.TFrame",
            padding=(15, 15),
        )
        nav_frame.pack(fill="x")

        self.create_sidebar_button(
            nav_frame,
            "📊  Dashboard",
            self.refresh,
        )

        self.create_sidebar_button(
            nav_frame,
            "📚  Manage Books",
            self.open_books,
        )

        self.create_sidebar_button(
            nav_frame,
            "👥  Manage Members",
            self.open_members,
        )

        self.create_sidebar_button(
            nav_frame,
            "🔄  Issue / Return",
            self.open_issue_return,
        )

        # Bottom information
        bottom = ttk.Frame(
            self.sidebar,
            style="Sidebar.TFrame",
            padding=20,
        )

        bottom.pack(
            side="bottom",
            fill="x",
        )

        ttk.Label(
            bottom,
            text="Library Management System",
            style="SidebarSubtitle.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            bottom,
            text="© 2026",
            style="SidebarSubtitle.TLabel",
        ).pack(anchor="w", pady=(5, 0))

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        self.main = tk.Frame(
            self.root,
            bg=self.colors["bg"],
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            self.main,
            bg=self.colors["bg"],
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 20),
        )

        title_frame = tk.Frame(
            header,
            bg=self.colors["bg"],
        )

        title_frame.pack(side="left")

        ttk.Label(
            title_frame,
            text="Dashboard",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            title_frame,
            text="Overview of your library activity",
            style="Subtitle.TLabel",
        ).pack(
            anchor="w",
            pady=(4, 0),
        )

        refresh_button = ttk.Button(
            header,
            text="↻  Refresh",
            style="Refresh.TButton",
            command=self.refresh,
        )

        refresh_button.pack(
            side="right",
            pady=5,
        )

        # =====================================================
        # STATISTICS
        # =====================================================

        cards_container = tk.Frame(
            self.main,
            bg=self.colors["bg"],
        )

        cards_container.pack(
            fill="x",
            padx=30,
        )

        self.card_values = {}

        card_data = [
            ("books", "Book Titles", "📚", self.colors["primary"]),
            ("total_copies", "Total Copies", "📦", self.colors["purple"]),
            ("available", "Available", "✓", self.colors["green"]),
            ("members", "Members", "👥", self.colors["cyan"]),
            ("issued", "Currently Issued", "📤", self.colors["orange"]),
            ("returned", "Returned", "📥", self.colors["red"]),
        ]

        for index, (key, title, icon, color) in enumerate(card_data):

            card = tk.Frame(
                cards_container,
                bg=self.colors["white"],
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=5,
            )

            cards_container.columnconfigure(
                index,
                weight=1,
            )

            # Colored top border
            top_bar = tk.Frame(
                card,
                bg=color,
                height=5,
            )

            top_bar.pack(
                fill="x",
                side="top",
            )

            content = tk.Frame(
                card,
                bg=self.colors["white"],
                padx=15,
                pady=15,
            )

            content.pack(
                fill="both",
                expand=True,
            )

            # Icon
            icon_label = tk.Label(
                content,
                text=icon,
                bg=self.colors["white"],
                fg=color,
                font=("Segoe UI Emoji", 20),
            )

            icon_label.pack(
                anchor="w",
            )

            # Title
            tk.Label(
                content,
                text=title,
                bg=self.colors["white"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9),
            ).pack(
                anchor="w",
                pady=(8, 2),
            )

            # Value
            value = tk.Label(
                content,
                text="0",
                bg=self.colors["white"],
                fg=self.colors["text"],
                font=("Segoe UI", 22, "bold"),
            )

            value.pack(
                anchor="w",
            )

            self.card_values[key] = value

        # =====================================================
        # MANAGEMENT SECTION
        # =====================================================

        management = tk.Frame(
            self.main,
            bg=self.colors["bg"],
        )

        management.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30,
        )

        # Section heading
        tk.Label(
            management,
            text="Quick Actions",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 16, "bold"),
        ).pack(
            anchor="w",
        )

        tk.Label(
            management,
            text="Access the main library management functions",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(
            anchor="w",
            pady=(3, 15),
        )

        actions = tk.Frame(
            management,
            bg=self.colors["bg"],
        )

        actions.pack(
            fill="x",
        )

        # Action buttons
        self.create_action_button(
            actions,
            "📚",
            "Manage Books",
            "Add, edit and remove books",
            self.open_books,
            self.colors["primary"],
            0,
        )

        self.create_action_button(
            actions,
            "👥",
            "Manage Members",
            "Add and manage library members",
            self.open_members,
            self.colors["purple"],
            1,
        )

        self.create_action_button(
            actions,
            "🔄",
            "Issue / Return",
            "Issue books or process returns",
            self.open_issue_return,
            self.colors["green"],
            2,
        )

        # =====================================================
        # STATUS BAR
        # =====================================================

        status = tk.Frame(
            self.main,
            bg=self.colors["white"],
            height=35,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )

        status.pack(
            side="bottom",
            fill="x",
        )

        tk.Label(
            status,
            text="● System Ready",
            bg=self.colors["white"],
            fg=self.colors["green"],
            font=("Segoe UI", 9, "bold"),
            padx=20,
        ).pack(
            side="left",
            pady=8,
        )

    # ---------------------------------------------------------
    # SIDEBAR BUTTON
    # ---------------------------------------------------------

    def create_sidebar_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors["sidebar"],
            fg="#D1D5DB",
            activebackground=self.colors["sidebar_hover"],
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=12,
            cursor="hand2",
        )

        button.pack(
            fill="x",
            pady=3,
        )

        def on_enter(event):
            button.configure(
                bg=self.colors["sidebar_hover"],
                fg="#FFFFFF",
            )

        def on_leave(event):
            button.configure(
                bg=self.colors["sidebar"],
                fg="#D1D5DB",
            )

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # ---------------------------------------------------------
    # ACTION BUTTON
    # ---------------------------------------------------------

    def create_action_button(
        self,
        parent,
        icon,
        title,
        description,
        command,
        color,
        column,
    ):

        card = tk.Frame(
            parent,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            cursor="hand2",
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=7,
            pady=5,
        )

        parent.columnconfigure(
            column,
            weight=1,
        )

        content = tk.Frame(
            card,
            bg=self.colors["white"],
            padx=20,
            pady=20,
        )

        content.pack(
            fill="both",
            expand=True,
        )

        # Icon
        tk.Label(
            content,
            text=icon,
            bg=self.colors["white"],
            fg=color,
            font=("Segoe UI Emoji", 28),
        ).pack(
            anchor="w",
        )

        # Title
        tk.Label(
            content,
            text=title,
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(
            anchor="w",
            pady=(10, 3),
        )

        # Description
        tk.Label(
            content,
            text=description,
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(
            anchor="w",
        )

        # Arrow
        tk.Label(
            content,
            text="→",
            bg=self.colors["white"],
            fg=color,
            font=("Segoe UI", 16, "bold"),
        ).pack(
            anchor="e",
            pady=(10, 0),
        )

        # Make entire card clickable
        widgets = [card, content]

        for widget in widgets:
            widget.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd(),
            )

        for widget in content.winfo_children():
            widget.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd(),
            )

        # Hover effect
        def on_enter(event):
            card.configure(
                highlightbackground=color,
                highlightthickness=2,
            )

        def on_leave(event):
            card.configure(
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    # ---------------------------------------------------------
    # REFRESH DASHBOARD
    # ---------------------------------------------------------

    def refresh(self):

        try:
            counts = get_dashboard_counts()

            for key, label in self.card_values.items():
                value = counts.get(key, 0)
                label.config(text=str(value))

        except Exception as error:
            print("Dashboard refresh error:", error)

            for label in self.card_values.values():
                label.config(text="0")

    # ---------------------------------------------------------
    # WINDOWS
    # ---------------------------------------------------------

    def open_books(self):
        BooksWindow(
            self.root,
            self.refresh,
        )

    def open_members(self):
        MembersWindow(
            self.root,
            self.refresh,
        )

    def open_issue_return(self):
        IssueReturnWindow(
            self.root,
            self.refresh,
        )
