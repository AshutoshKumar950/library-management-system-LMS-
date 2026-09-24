from database.db import execute
from models.book import Book


# =========================================================
# ADD BOOK
# =========================================================

def add_book(book: Book):

    if not book.title.strip():
        raise ValueError("Book title is required.")

    if not book.author.strip():
        raise ValueError("Author name is required.")

    if book.quantity < 1:
        raise ValueError("Quantity must be at least 1.")

    isbn = book.isbn.strip() if book.isbn else None

    # Check duplicate ISBN
    if isbn:
        existing = execute(
            """
            SELECT id
            FROM books
            WHERE isbn = ?
            """,
            (isbn,),
            fetchone=True,
        )

        if existing:
            raise ValueError(
                "A book with this ISBN already exists."
            )

    return execute(
        """
        INSERT INTO books
        (title, author, isbn, category, quantity, available)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            book.title.strip(),
            book.author.strip(),
            isbn,
            book.category.strip() if book.category else "",
            book.quantity,
            book.quantity,
        ),
    )


# =========================================================
# GET ALL BOOKS
# =========================================================

def get_books(search=""):

    search = search.strip()

    if search:
        value = f"%{search}%"

        return execute(
            """
            SELECT *
            FROM books
            WHERE title LIKE ?
               OR author LIKE ?
               OR isbn LIKE ?
               OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value,
            ),
            fetch=True,
        )

    return execute(
        """
        SELECT *
        FROM books
        ORDER BY id DESC
        """,
        fetch=True,
    )


# =========================================================
# GET BOOK BY ID
# =========================================================

def get_book(book_id):

    if book_id is None:
        return None

    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        return None

    return execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        """,
        (book_id,),
        fetchone=True,
    )


# =========================================================
# UPDATE BOOK
# =========================================================

def update_book(book_id, book: Book):

    # Convert ID to integer
    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        raise ValueError("Invalid book ID.")

    # Check book
    old_book = get_book(book_id)

    if old_book is None:
        raise ValueError(
            f"Book with ID {book_id} was not found."
        )

    # Validate title
    title = book.title.strip()

    if not title:
        raise ValueError(
            "Book title is required."
        )

    # Validate author
    author = book.author.strip()

    if not author:
        raise ValueError(
            "Author name is required."
        )

    # Validate quantity
    try:
        quantity = int(book.quantity)
    except (ValueError, TypeError):
        raise ValueError(
            "Quantity must be a number."
        )

    if quantity < 1:
        raise ValueError(
            "Quantity must be at least 1."
        )

    # Clean data
    isbn = (
        book.isbn.strip()
        if book.isbn
        else None
    )

    category = (
        book.category.strip()
        if book.category
        else ""
    )

    # -----------------------------------------------------
    # Calculate issued books
    # -----------------------------------------------------

    old_quantity = int(old_book["quantity"])
    old_available = int(old_book["available"])

    issued_count = old_quantity - old_available

    if issued_count < 0:
        issued_count = 0

    # New quantity cannot be less than issued books
    if quantity < issued_count:
        raise ValueError(
            f"Quantity cannot be less than currently "
            f"issued books ({issued_count})."
        )

    # Calculate available
    new_available = quantity - issued_count

    # -----------------------------------------------------
    # Check duplicate ISBN
    # -----------------------------------------------------

    if isbn:

        duplicate = execute(
            """
            SELECT id
            FROM books
            WHERE isbn = ?
              AND id != ?
            LIMIT 1
            """,
            (
                isbn,
                book_id,
            ),
            fetchone=True,
        )

        if duplicate:
            raise ValueError(
                "Another book with this ISBN already exists."
            )

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    result = execute(
        """
        UPDATE books
        SET
            title = ?,
            author = ?,
            isbn = ?,
            category = ?,
            quantity = ?,
            available = ?
        WHERE id = ?
        """,
        (
            title,
            author,
            isbn,
            category,
            quantity,
            new_available,
            book_id,
        ),
    )

    # -----------------------------------------------------
    # Verify UPDATE
    # -----------------------------------------------------

    updated_book = get_book(book_id)

    if updated_book is None:
        raise ValueError(
            "Book update failed."
        )

    return updated_book


# =========================================================
# DELETE BOOK
# =========================================================

def delete_book(book_id):

    # Convert ID
    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid book ID."
        )

    # Check book exists
    book = get_book(book_id)

    if book is None:
        raise ValueError(
            f"Book with ID {book_id} was not found."
        )

    # -----------------------------------------------------
    # Check active issue
    # -----------------------------------------------------

    try:

        active_issue = execute(
            """
            SELECT id
            FROM issues
            WHERE book_id = ?
              AND status = 'Issued'
            LIMIT 1
            """,
            (book_id,),
            fetchone=True,
        )

    except Exception:
        # If issues table is not available,
        # continue with deletion.
        active_issue = None

    if active_issue:

        raise ValueError(
            "This book is currently issued "
            "and cannot be deleted."
        )

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    result = execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (book_id,),
    )

    # -----------------------------------------------------
    # VERIFY DELETE
    # -----------------------------------------------------

    deleted_book = get_book(book_id)

    if deleted_book is not None:
        raise ValueError(
            "Book could not be deleted."
        )

    return result


# =========================================================
# UPDATE AVAILABLE QUANTITY
# =========================================================

def update_available_quantity(book_id, change):

    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid book ID."
        )

    try:
        change = int(change)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid quantity change."
        )

    book = get_book(book_id)

    if book is None:
        raise ValueError(
            "Book not found."
        )

    new_available = (
        int(book["available"]) + change
    )

    if new_available < 0:
        raise ValueError(
            "No available copies of this book."
        )

    if new_available > int(book["quantity"]):
        raise ValueError(
            "Available quantity cannot exceed total quantity."
        )

    execute(
        """
        UPDATE books
        SET available = ?
        WHERE id = ?
        """,
        (
            new_available,
            book_id,
        ),
    )

    return get_book(book_id)


# =========================================================
# GET AVAILABLE BOOKS
# =========================================================

def get_available_books():

    return execute(
        """
        SELECT *
        FROM books
        WHERE available > 0
        ORDER BY title ASC
        """,
        fetch=True,
    )


# =========================================================
# GET BOOK COUNT
# =========================================================

def get_book_count():

    result = execute(
        """
        SELECT COUNT(*) AS total
        FROM books
        """,
        fetchone=True,
    )

    if result:
        return result["total"]

    return 0
