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

