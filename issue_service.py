from datetime import datetime

from database.db import execute


def issue_book(book_id, member_id):
    book = execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,),
        fetchone=True,
    )

    if not book:
        raise ValueError("Book not found.")

    if book["available"] <= 0:
        raise ValueError("No available copy of this book.")

    member = execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,),
        fetchone=True,
    )

    if not member:
        raise ValueError("Member not found.")

    existing = execute(
        """
        SELECT id
        FROM issues
        WHERE book_id = ?
          AND member_id = ?
          AND status = 'Issued'
        LIMIT 1
        """,
        (book_id, member_id),
        fetchone=True,
    )

    if existing:
        raise ValueError(
            "This member already has this book issued."
        )

    issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    execute(
        """
        INSERT INTO issues
        (book_id, member_id, issue_date, status)
        VALUES (?, ?, ?, 'Issued')
        """,
        (book_id, member_id, issue_date),
    )

    execute(
        """
        UPDATE books
        SET available = available - 1
        WHERE id = ?
        """,
        (book_id,),
    )


def return_book(issue_id):
    issue = execute(
        """
        SELECT *
        FROM issues
        WHERE id = ?
        """,
        (issue_id,),
        fetchone=True,
    )

    if not issue:
        raise ValueError("Issue record not found.")

    if issue["status"] == "Returned":
        raise ValueError("This book has already been returned.")

    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    execute(
        """
        UPDATE issues
        SET return_date = ?,
            status = 'Returned'
        WHERE id = ?
        """,
        (return_date, issue_id),
    )

    execute(
        """
        UPDATE books
        SET available = available + 1
        WHERE id = ?
        """,
        (issue["book_id"],),
    )


def get_issues(status=None):
    query = """
        SELECT
            issues.id,
            issues.book_id,
            issues.member_id,
            books.title AS book_title,
            members.name AS member_name,
            issues.issue_date,
            issues.return_date,
            issues.status
        FROM issues
        JOIN books ON books.id = issues.book_id
        JOIN members ON members.id = issues.member_id
    """

    params = ()

    if status:
        query += " WHERE issues.status = ? "
        params = (status,)

    query += " ORDER BY issues.id DESC"

    return execute(
        query,
        params,
        fetch=True,
    )


def get_dashboard_counts():
    books = execute(
        "SELECT COUNT(*) AS count FROM books",
        fetchone=True,
    )["count"]

    total_copies = execute(
        "SELECT COALESCE(SUM(quantity), 0) AS count FROM books",
        fetchone=True,
    )["count"]

    available = execute(
        "SELECT COALESCE(SUM(available), 0) AS count FROM books",
        fetchone=True,
    )["count"]

    members = execute(
        "SELECT COUNT(*) AS count FROM members",
        fetchone=True,
    )["count"]

    issued = execute(
        """
        SELECT COUNT(*) AS count
        FROM issues
        WHERE status = 'Issued'
        """,
        fetchone=True,
    )["count"]

    returned = execute(
        """
        SELECT COUNT(*) AS count
        FROM issues
        WHERE status = 'Returned'
        """,
        fetchone=True,
    )["count"]

    return {
        "books": books,
        "total_copies": total_copies,
        "available": available,
        "members": members,
        "issued": issued,
        "returned": returned,
    }

