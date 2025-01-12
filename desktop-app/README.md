# Desktop App for Data Entry and Management

This project is a desktop application developed using Python and Ttkbootstrap. It provides a user-friendly interface for entering and managing data, with features for filtering, exporting, and displaying records.

## Features

- **Data Entry Form**: Users can input T.C. Kimlik Numarası, İsim Soyisim, İşlem Tarihi, İşlem Tipi, and an optional Açıklama.
- **Dynamic Table View**: Displays entered data with filtering options and export functionality.
- **Info Icon**: Each row includes an info icon that shows the record time and the name of the computer that saved the data.
- **Export Options**: Users can export data to Excel and PDF formats.
- **SQLite3 Database**: Data is stored in a local SQLite3 database, allowing for easy data management.

## Project Structure

```
desktop-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui
│   │   ├── form.py            # Data entry form implementation
│   │   ├── table.py           # Table view for displaying data
│   │   └── filter.py          # Filtering and searching functionality
│   ├── models
│   │   └── database.py        # Database connection and operations
│   ├── controllers
│   │   ├── form_controller.py  # Logic for handling form submissions
│   │   ├── table_controller.py # Manages data displayed in the table
│   │   └── filter_controller.py # Handles filtering logic
│   └── utils
│       └── export.py          # Utility functions for exporting data
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Files to ignore in version control
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd desktop-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to enter data, filter records, and export data as needed.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.