# Hotel Management System 🏨

This project is a **Hotel Management System** developed as a university project using **Python**. It provides functionality to manage rooms, guests, reservations, and generate reports through a text-based interface. Data is stored in a JSON file, and the system includes features like table sorting, chart displays, and input validation.

## Features
- **Room Management**:
  - Add, edit, and delete rooms
  - View all rooms or available rooms only
  - Display guest information for occupied rooms
- **Guest Management**:
  - Add, edit, and delete guests
  - Search guests by name or national ID
  - View all guests
- **Reservation Management**:
  - Book rooms, check-in, check-out, and cancel reservations
  - View active reservations, reservations by guest, or by room
- **Reporting**:
  - Room status report (available, reserved, occupied) with a bar chart
  - Active reservations report for a specific date
  - Income report for a given date range with a timeline visualization
- **User Interface**:
  - Text-based menus with color-coded outputs and formatted tables
  - Notification messages (success, error, warning)
  - Table sorting by column
- **Data Storage**:
  - Data persistence in a JSON file
  - Automatic room status updates based on reservation dates

## Prerequisites
To run this project, you need:
- **Python 3.6 or higher**
- Python libraries:
  - `colorama` (for colored terminal output)

  Install the required library:
  ```bash
  pip install colorama


## How to Run

  **Clone the repository:**

       ```bash
      git clone https://github.com/<your-username>/hotel-management-system.git


## Navigate to the project directory:

    ```bash
       cd hotel-management-system


## Run the main script:
    ```bash
    python hotel_management_system.py

Use the text-based menu to interact with the system.


**Project Structure:**

hotel_management_system.py: The main project file containing all code, classes, and menus.
hotel_data.json: Generated file for storing room, guest, and reservation data.

#Usage Examples:

**Add a Room:**

From the room management menu, select the add option.
Enter room type (e.g., single) and price (e.g., 5,000,000 IRR).

**Book a Room:**

From the reservations menu, select a guest and an available room.
Enter check-in and check-out dates (e.g., 2025-04-01).

**Generate Reports:**

From the reports menu, view room status or income for a specific period.


# Notes

**Input Validation:**

National ID must be 10 digits.

Phone numbers must be 11 digits starting with 09.

Dates must be in the format YYYY-MM-DD.


**Room Status Updates:**

Room statuses are automatically updated based on reservation dates and the current date.


**Data Persistence:**

All changes are automatically saved to the hotel_data.json file.
