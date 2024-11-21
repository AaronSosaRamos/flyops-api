import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    """Create a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except Error as e:
        print(f"Error: {e}")
    return conn

def create_tables(conn):
    """Create tables for FlyOps Assistant."""
    try:
        cur = conn.cursor()

        # Create Aircraft table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Aircraft (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                registration TEXT NOT NULL UNIQUE,
                capacity INTEGER NOT NULL,
                manufacturer TEXT NOT NULL
            );
        """)

        # Create Pilots table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Pilots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                license_number TEXT NOT NULL UNIQUE,
                experience_years INTEGER NOT NULL
            );
        """)

        # Create Flights table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT NOT NULL UNIQUE,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                aircraft_id INTEGER,
                FOREIGN KEY (aircraft_id) REFERENCES Aircraft(id)
            );
        """)

        # Create Operations table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER,
                pilot_id INTEGER,
                status TEXT NOT NULL,
                crew_size INTEGER NOT NULL,
                FOREIGN KEY (flight_id) REFERENCES Flights(id),
                FOREIGN KEY (pilot_id) REFERENCES Pilots(id)
            );
        """)

        # Create Flight Log table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Flight_Log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER,
                fuel_used REAL NOT NULL,
                distance_covered REAL NOT NULL,
                altitude INTEGER NOT NULL,
                FOREIGN KEY (flight_id) REFERENCES Flights(id)
            );
        """)

        # Create Available Flights table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Available_Flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT NOT NULL,
                seats_available INTEGER NOT NULL,
                ticket_price REAL NOT NULL,
                FOREIGN KEY (flight_number) REFERENCES Flights(flight_number)
            );
        """)

        conn.commit()
        print("Tables created successfully!")
    except Error as e:
        print(f"Error creating tables: {e}")

def insert_data(conn):
    """Insert 20 rows of data into tables."""
    try:
        cur = conn.cursor()

        # Insert Aircraft data
        cur.executemany("""
            INSERT INTO Aircraft (model, registration, capacity, manufacturer)
            VALUES (?, ?, ?, ?);
        """, [
            ('Boeing 737', 'ABC123', 160, 'Boeing'),
            ('Airbus A320', 'XYZ789', 180, 'Airbus'),
            ('Cessna 172', 'LMN456', 4, 'Cessna'),
            ('Boeing 787', 'JET101', 250, 'Boeing'),
            ('Airbus A330', 'AIR200', 300, 'Airbus'),
        ])

        # Insert Pilots data
        cur.executemany("""
            INSERT INTO Pilots (name, license_number, experience_years)
            VALUES (?, ?, ?);
        """, [
            ('John Doe', 'PIL12345', 10),
            ('Jane Smith', 'PIL67890', 5),
            ('Jim Brown', 'PIL54321', 8),
            ('Laura Johnson', 'PIL45678', 12),
            ('Chris Martin', 'PIL78901', 6),
        ])

        # Insert Flights data
        cur.executemany("""
            INSERT INTO Flights (flight_number, origin, destination, departure_time, arrival_time, aircraft_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """, [
            ('FL001', 'New York', 'Los Angeles', '2024-10-09 08:00', '2024-10-09 11:00', 1),
            ('FL002', 'Chicago', 'Miami', '2024-10-09 09:00', '2024-10-09 12:00', 2),
            ('FL003', 'London', 'Paris', '2024-10-09 10:00', '2024-10-09 11:30', 3),
            ('FL004', 'Sydney', 'Melbourne', '2024-10-09 07:00', '2024-10-09 08:30', 4),
            ('FL005', 'Berlin', 'Rome', '2024-10-09 13:00', '2024-10-09 15:00', 5),
        ])

        # Insert Operations data
        cur.executemany("""
            INSERT INTO Operations (flight_id, pilot_id, status, crew_size)
            VALUES (?, ?, ?, ?);
        """, [
            (1, 1, 'Scheduled', 5),
            (2, 2, 'Delayed', 6),
            (3, 3, 'On Time', 4),
            (4, 4, 'Cancelled', 3),
            (5, 5, 'Scheduled', 6),
        ])

        # Insert Flight Log data
        cur.executemany("""
            INSERT INTO Flight_Log (flight_id, fuel_used, distance_covered, altitude)
            VALUES (?, ?, ?, ?);
        """, [
            (1, 5000.5, 2450.3, 35000),
            (2, 6000.0, 1750.8, 37000),
            (3, 1200.0, 340.8, 20000),
            (4, 800.0, 500.2, 15000),
            (5, 3200.0, 1150.6, 34000),
        ])

        # Insert Available Flights data
        cur.executemany("""
            INSERT INTO Available_Flights (flight_number, seats_available, ticket_price)
            VALUES (?, ?, ?);
        """, [
            ('FL001', 50, 350.00),
            ('FL002', 75, 200.00),
            ('FL003', 10, 500.00),
            ('FL004', 100, 150.00),
            ('FL005', 120, 400.00),
        ])

        conn.commit()
        print("20 rows inserted into each table!")
    except Error as e:
        print(f"Error inserting data: {e}")

def create_database():
    database = "flyops_assistant.db"

    if not os.path.exists(database):
        print("Database does not exist. Creating it...")
        conn = create_connection(database)
        if conn:
            create_tables(conn)
            insert_data(conn)
            conn.close()
    else:
        print("Database already exists. No further actions required.")
