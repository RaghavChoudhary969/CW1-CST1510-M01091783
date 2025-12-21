# main.py

from contextlib import closing
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.tickets import insert_ticket, list_tickets, ticket_exists
from app.data.users import user_exists
from app.services.user_service import authenticate, create_account

def main():
    print("Initializing database...")

    with closing(connect_database()) as db:
        # Create tables if not exist
        create_all_tables(db)

        # Admin user setup
        admin_username = "admin67892341239987"
        admin_password = "admin123"

        # Delete old admin if exists (optional, to avoid bcrypt errors)
        db.execute("DELETE FROM users WHERE username = ?", (admin_username,))
        db.commit()

        # Create admin user with hashed password
        if not user_exists(admin_username):
            create_account(admin_username, admin_password, role="admin")
            print("Admin user created with hashed password.")
        else:
            print("Admin already exists. Skipping.")

        # Demo ticket setup
        ticket_id = "TCK001122"

        if not ticket_exists(ticket_id):
            insert_ticket(
                ticket_id=ticket_id,
                priority="High",
                status="Open",
                category="Software",
                subject="Login Issue",
                description="Test ticket",
                created_date="2024-09-12",
                resolved_date=None,
                assigned_to="test"
            )
            print("Demo ticket added.")
        else:
            print("Demo ticket already exists. Skipping.")

        # Show all tickets
        print("\nAll Tickets:")
        print(list_tickets())

        # Test login/authentication
        print("\nAuthentication Test:")
        result = authenticate(admin_username, admin_password)
        if result:
            print("Login successful:", result)
        else:
            print("Login failed")


if __name__ == "__main__":
    main()
