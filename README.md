# Taxi Booking CLI System

This is a command-line taxi booking system implemented in Python. It allows users to register, login, book taxi rides, see estimated costs, view ride history, rate drivers, and submit complaints. The system also includes an admin panel to manage cars, drivers, complaints, and ride data.

This project was developed as part of a unit project to simulate a working taxi booking system entirely in the terminal environment.

---

## Project Features

✅ **User Account System**  
- Register as a passenger or driver
- Login and manage profile

✅ **Ride Booking**  
- Select car category (standard, medium, VIP)
- Estimate distance, time, and fare using geolocation
- Book rides and choose payment method (cash, visa, mada)
- Simulated driver arrival messages:
    ```
    Looking for a driver...
    Driver is on the way...
    Driver is outside waiting!
    ```
- Animated ASCII art showing the taxi moving to the destination

✅ **Ride History**  
- View all previous rides and details

✅ **Driver Ratings**  
- Rate a driver after completing a ride
- Admin can view average driver ratings

✅ **Complaints System**  
- Passengers can file complaints linked to specific rides

✅ **Admin Panel**  
- View drivers and their average ratings
- View list of cars and their status (ready/busy)
- Edit car status
- Delete rides
- View all complaints submitted

---

## Technologies Used

- **Python 3.8+**
- **geopy** — For geocoding locations and calculating distances
- **colorama** — For colored terminal output
- **asciimatics** — For ASCII animations

---

## Installation

1. **Clone the repository:**

    ```bash
    git clone <your_repo_url>
    cd taxi_booking_system
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - Windows PowerShell:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    - macOS / Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

Once your environment is ready, run:

```bash
python -m src.Taxi_Booking.py
