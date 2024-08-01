import sqlite3
import pytest
from project import add_contact, view_contacts, search_contact, delete_contact, edit_contact, initialize_database, DATABASE_FILE


@pytest.fixture
def test_db():
    """Set up a fresh database for testing."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS contacts')
    initialize_database()
    yield conn
    conn.close()


def test_add_contact(test_db):
    """Test adding a contact to the database."""
    add_contact('John', 'Doe', '1234567890', 'john.doe@example.com', '123 Elm St', 'Male')
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM contacts WHERE first_name = ? AND last_name = ?', ('John', 'Doe'))
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == 'John'
    assert row[2] == 'Doe'
    assert row[3] == '1234567890'
    assert row[4] == 'john.doe@example.com'
    assert row[5] == '123 Elm St'
    assert row[6] == 'Male'


def test_view_contacts(test_db):
    """Test viewing contacts from the database."""
    add_contact('Jane', 'Doe', '0987654321', 'jane.doe@example.com', '456 Oak St', 'Female')
    contacts = view_contacts()
    assert 'Jane' in contacts


def test_search_contact(test_db):
    """Test searching for a contact by first name."""
    add_contact('Alice', 'Smith', '5555555555', 'alice.smith@example.com', '789 Pine St', 'Female')
    search_result = search_contact('Alice', 'first_name')
    assert 'Alice Smith' in search_result


def test_edit_contact(test_db):
    """Test editing an existing contact's details."""
    add_contact('Bob', 'Johnson', '1112223333', 'bob.johnson@example.com', '321 Birch St', 'Male')
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE first_name = ? AND last_name = ?', ('Bob', 'Johnson'))
    contact_id = cursor.fetchone()[0]
    edit_contact(contact_id, phone='4445556666', email='bob.newemail@example.com')
    cursor.execute('SELECT phone, email FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()
    assert row[0] == '4445556666'
    assert row[1] == 'bob.newemail@example.com'


def test_delete_contact(test_db):
    """Test deleting a contact from the database."""
    add_contact('Charlie', 'Brown', '7778889999', 'charlie.brown@example.com', '654 Maple St', 'Male')
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE first_name = ? AND last_name = ?', ('Charlie', 'Brown'))
    contact_id = cursor.fetchone()[0]
    delete_contact(contact_id)
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()
    assert row is None
