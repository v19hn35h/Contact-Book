import sqlite3
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()
DATABASE_FILE = 'contacts.db'


def main():
    """Main function to handle the menu and user choices."""
    initialize_database()

    while True:
        try:
            print()
            table = Table(title="Menu")
            table.add_column("Action")
            table.add_column("ID")
            table.add_row("Add Contacts", '1', style="cyan")
            table.add_row("View Contacts", '2', style="cyan")
            table.add_row("Search Contacts", '3', style="cyan")
            table.add_row("Edit Contacts", '4', style="cyan")
            table.add_row("Delete Contacts", '5', style="cyan")
            table.add_row("Exit", '6', style="red")
            console.print(table)
            print()
            ask = Prompt.ask('Enter your choice')
            print()

            if ask == '1':
                firstname = Prompt.ask('First Name')
                lastname = Prompt.ask('Last Name')
                phone = Prompt.ask('Phone Number')
                email = Prompt.ask('Email')
                address = Prompt.ask('Address')
                gender = Prompt.ask('Gender')
                add_contact(firstname, lastname, phone, email, address, gender)

            elif ask == '2':
                view_contacts()
            elif ask == '3':
                console.print('''Search By
[cyan]First Name[/cyan]: Type F
[cyan]Last Name[/cyan]: Type L\n''')
                name_type0 = Prompt.ask("Enter your choice").strip().upper()

                if name_type0 == "F":
                    name = Prompt.ask('Enter First Name').strip()
                    name_type = 'first_name'
                elif name_type0 == "L":
                    name = Prompt.ask('Enter Last Name').strip()
                    name_type = 'last_name'
                else:
                    console.print('[red]Invalid input. Please type F for First Name or L for Last Name.[/red]')
                    continue

                if not name:
                    console.print('[yellow]Search term cannot be empty.[/yellow]')
                    continue
                search_contact(name, name_type)
            elif ask == '4':
                view_contacts()
                print()
                contact_id = Prompt.ask("Enter ID of contact you want to edit")
                firstname = Prompt.ask('First Name (leave blank to keep current)')
                lastname = Prompt.ask('Last Name (leave blank to keep current)')
                phone = Prompt.ask('Phone Number (leave blank to keep current)')
                email = Prompt.ask('Email (leave blank to keep current)')
                address = Prompt.ask('Address (leave blank to keep current)')
                gender = Prompt.ask('Gender (leave blank to keep current)')
                edit_contact(contact_id, firstname, lastname, phone, email, address, gender)
            elif ask == '5':
                view_contacts()
                print()
                contact_id = Prompt.ask("Enter ID")
                delete_contact(contact_id)
                print()
                view_contacts()
            elif ask == '6':
                console.print("[red]Exiting.[/red]")
                sys.exit()
            else:
                console.print("[red]Invalid choice, please try again.[/red]")
        except KeyboardInterrupt:
            console.print("[red]Exiting.[/red]")
            sys.exit()


def initialize_database():
    """Initialize the database and create the contacts table."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                gender TEXT
            )
        ''')
        conn.commit()


def add_contact(firstname, lastname, phone, email, address, gender):
    """Add a new contact to the database."""
    print()
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (first_name, last_name, phone, email, address, gender)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (firstname, lastname, phone, email, address, gender))
        conn.commit()
    console.print(f"[green]Contact [white]{firstname + ' ' + lastname}[/white] added successfully![/green]")


def view_contacts():
    """View all contacts from the database and return them as a string."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        rows = cursor.fetchall()

        table = Table(title="Contacts")
        table.add_column("ID", style="magenta")
        table.add_column("First Name", style="cyan")
        table.add_column("Last Name", style="cyan")
        table.add_column("Phone", style="yellow")
        table.add_column("Email", style="green")
        table.add_column("Address", style="blue")
        table.add_column("Gender", style="red")
        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])

        console.print(table)

    return '\n'.join([f"{row[1]} {row[2]}" for row in rows])  # Return a simplified string for testing


def search_contact(name, name_type):
    """Search for a contact by name and return results as a string."""
    name_lower = name.lower()
    name_upper = name.upper()
    name_title = name.title()

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        query = f"""
        SELECT * FROM contacts 
        WHERE LOWER({name_type}) = ? OR 
              UPPER({name_type}) = ? OR 
              {name_type} = ?
        """
        cursor.execute(query, (name_lower, name_upper, name_title))
        rows = cursor.fetchall()

        if rows:
            table = Table(title=f"Search Results for {name}")
            table.add_column("ID", style="magenta")
            table.add_column("First Name", style="cyan")
            table.add_column("Last Name", style="cyan")
            table.add_column("Phone", style="yellow")
            table.add_column("Email", style="green")
            table.add_column("Address", style="blue")
            table.add_column("Gender", style="red")
            for row in rows:
                table.add_row(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
            console.print(table)

        return '\n'.join([f"{row[1]} {row[2]}" for row in rows])  # Return a simplified string for testing


def delete_contact(contact_id):
    """Delete a contact by ID."""
    print()
    try:
        contact_id = int(contact_id)
    except ValueError:
        console.print('[red]Invalid input. ID must be an integer.[/red]')
        return
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        conn.commit()
        if cursor.rowcount == 0:
            console.print("[red]No contact found with that ID.[/red]")
        else:
            console.print("[red]Contact deleted successfully.[/red]")


def edit_contact(contact_id, firstname=None, lastname=None, phone=None, email=None, address=None, gender=None):
    """Edit an existing contact's details."""
    print()
    try:
        contact_id = int(contact_id)
    except ValueError:
        console.print('[red]Invalid input. ID must be an integer.[/red]')
        return

    updates = []
    values = []

    if firstname:
        updates.append("first_name = ?")
        values.append(firstname)
    if lastname:
        updates.append("last_name = ?")
        values.append(lastname)
    if phone:
        updates.append("phone = ?")
        values.append(phone)
    if email:
        updates.append("email = ?")
        values.append(email)
    if address:
        updates.append("address = ?")
        values.append(address)
    if gender:
        updates.append("gender = ?")
        values.append(gender)

    if not updates:
        console.print("[yellow]No fields to update.[/yellow]")
        return

    values.append(contact_id)

    update_query = f"UPDATE contacts SET {', '.join(updates)} WHERE id = ?"

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(update_query, values)
        conn.commit()

        if cursor.rowcount == 0:
            console.print("[red]No contact found with that ID.[/red]")
        else:
            console.print("[green]Contact updated successfully![/green]")
    view_contacts()


if __name__ == "__main__":
    main()
