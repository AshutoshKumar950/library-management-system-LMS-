# Library Management System

A desktop Library Management System built with:

- Python
- Tkinter
- SQLite

## Features

- Add books
- Update books
- Delete books
- Search books
- Add members
- Update members
- Delete members
- Search members
- Issue books
- Return books
- Dashboard statistics
- Automatic SQLite database

## Requirements

Python 3.10 or newer is recommended.

No external Python packages are required.

## Project Structure

library_management/
│
├── main.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── library.db
│
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   └── issue.py
│
├── services/
│   ├── __init__.py
│   ├── book_service.py
│   ├── member_service.py
│   └── issue_service.py
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── books.py
│   ├── members.py
│   └── issue_return.py
│
└── utils/
    ├── __init__.py
    └── helpers.py

## How to Run

Open terminal inside the library_management folder.

Run:

python main.py

On Windows you can also use:

py main.py

The SQLite database will be automatically created inside:

database/library.db

