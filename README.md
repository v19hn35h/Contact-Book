# Contact Book

#### Video Demo: https://youtu.be/L4WTK8KFGFM?feature=shared

## Project Overview
The **Contact Book** is a Python application developed as my final project for the CS50P course designed to manage personal contacts. It provides a command-line interface to add, view, search, edit, and delete contacts using an SQLite database.

## Features

- **Add Contacts**: Input and save new contact information.
- **View Contacts**: Display all contacts in a tabular format.
- **Search Contacts**: Find contacts by first name or last name.
- **Edit Contacts**: Update details of existing contacts.
- **Delete Contacts**: Remove contacts from the database.

## Project Structure

- `project.py`: Main application file containing the core functionality.
- `test_project.py`: Contains test cases for the functionalities using `pytest`.
- `requirements.txt`: Lists the necessary Python libraries for the project.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/v19hn35h/Contact-Book.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd Contact-Book
    ```

3. **Install Dependencies**:

    Ensure Python is installed, then install required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application**:

    ```bash
    python project.py
    ```

2. **Interact with the Menu** to add, view, search, edit, or delete contacts.

## Testing

To verify that all functionalities are working, run:

```bash
pytest
```

## Requirements

The `requirements.txt` file includes:

- `rich`: For enhanced command-line interfaces.
- `sqlite3`: For database operations (included with Python).

## Contributing

Contributions are welcome! If you want to contribute to the Contact Book project:

1. **Fork** the repository.
2. **Create** a new branch for your feature or bugfix.
3. **Make** your changes.
4. **Submit** a pull request with a clear description of the changes and their purpose.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
