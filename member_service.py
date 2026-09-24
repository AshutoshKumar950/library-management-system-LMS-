from database.db import execute
from models.member import Member


# =========================================================
# ADD MEMBER
# =========================================================

def add_member(member: Member):

    name = member.name.strip()
    email = member.email.strip()
    phone = member.phone.strip()
    address = member.address.strip()

    if not name:
        raise ValueError("Member name is required.")

    if not email:
        raise ValueError("Email is required.")

    if not phone:
        raise ValueError("Phone number is required.")

    # Check duplicate email
    existing = execute(
        """
        SELECT id
        FROM members
        WHERE email = ?
        LIMIT 1
        """,
        (email,),
        fetchone=True,
    )

    if existing:
        raise ValueError(
            "A member with this email already exists."
        )

    return execute(
        """
        INSERT INTO members
        (name, email, phone, address)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            phone,
            address,
        ),
    )


# =========================================================
# GET ALL MEMBERS
# =========================================================

def get_members(search=""):

    search = search.strip()

    if search:

        search_value = f"%{search}%"

        return execute(
            """
            SELECT *
            FROM members
            WHERE name LIKE ?
               OR email LIKE ?
               OR phone LIKE ?
               OR address LIKE ?
            ORDER BY id DESC
            """,
            (
                search_value,
                search_value,
                search_value,
                search_value,
            ),
            fetch=True,
        )

    return execute(
        """
        SELECT *
        FROM members
        ORDER BY id DESC
        """,
        fetch=True,
    )


# =========================================================
# GET MEMBER BY ID
# =========================================================

def get_member(member_id):

    if member_id is None:
        return None

    try:
        member_id = int(member_id)
    except (ValueError, TypeError):
        return None

    return execute(
        """
        SELECT *
        FROM members
        WHERE id = ?
        """,
        (member_id,),
        fetchone=True,
    )


# =========================================================
# UPDATE MEMBER
# =========================================================

def update_member(member_id, member: Member):

    # Convert ID
    try:
        member_id = int(member_id)
    except (ValueError, TypeError):
        raise ValueError("Invalid member ID.")

    # Check member exists
    old_member = get_member(member_id)

    if old_member is None:
        raise ValueError(
            f"Member with ID {member_id} was not found."
        )

    # Get clean values
    name = member.name.strip()
    email = member.email.strip()
    phone = member.phone.strip()
    address = member.address.strip()

    # Validation
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

    # -----------------------------------------------------
    # Check duplicate email
    # -----------------------------------------------------

    duplicate = execute(
        """
        SELECT id
        FROM members
        WHERE email = ?
          AND id != ?
        LIMIT 1
        """,
        (
            email,
            member_id,
        ),
        fetchone=True,
    )

    if duplicate:
        raise ValueError(
            "Another member with this email already exists."
        )

    # -----------------------------------------------------
    # UPDATE MEMBER
    # -----------------------------------------------------

    execute(
        """
        UPDATE members
        SET
            name = ?,
            email = ?,
            phone = ?,
            address = ?
        WHERE id = ?
        """,
        (
            name,
            email,
            phone,
            address,
            member_id,
        ),
    )

    # -----------------------------------------------------
    # Verify update
    # -----------------------------------------------------

    updated_member = get_member(member_id)

    if updated_member is None:
        raise ValueError(
            "Member update failed."
        )

    return updated_member


# =========================================================
# DELETE MEMBER
# =========================================================

def delete_member(member_id):

    # Convert ID
    try:
        member_id = int(member_id)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid member ID."
        )

    # Check member exists
    member = get_member(member_id)

    if member is None:
        raise ValueError(
            f"Member with ID {member_id} was not found."
        )

    # -----------------------------------------------------
    # Check active issue
    # -----------------------------------------------------

    try:

        active_issue = execute(
            """
            SELECT id
            FROM issues
            WHERE member_id = ?
              AND status = 'Issued'
            LIMIT 1
            """,
            (member_id,),
            fetchone=True,
        )

    except Exception:
        active_issue = None

    if active_issue:

        raise ValueError(
            "This member has an active issued book "
            "and cannot be deleted."
        )

    # -----------------------------------------------------
    # DELETE MEMBER
    # -----------------------------------------------------

    execute(
        """
        DELETE FROM members
        WHERE id = ?
        """,
        (member_id,),
    )

    # -----------------------------------------------------
    # Verify delete
    # -----------------------------------------------------

    deleted_member = get_member(member_id)

    if deleted_member is not None:
        raise ValueError(
            "Member could not be deleted."
        )

    return True