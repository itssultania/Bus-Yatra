import sqlite3
import datetime


class BookingDetails:
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS booking_details (passanger_name TEXT NOT NULL,\
                passanger_gender TEXT NOT NULL, seat_count INTEGER NOT NULL,\
                passanger_mobile_no INTEGER NOT NULL, passanger_age INTEGER NOT NULL,\
                operator_name TEXT NOT NULL, source TEXT NOT NULL, destination TEXT NOT NULL,\
                bus_fare INTEGER NOT NULL, running_date TEXT NOT NULL, booking_date TEXT NOT NULL)"
        )

    def add_passanger(
        self,
        passanger_name,
        passanger_gender,
        seat_count,
        passanger_mobile_no,
        passanger_age,
        operator_name,
        source,
        destination,
        bus_fare,
        running_date,
        availability,
    ):
        if not all(
            [
                passanger_name,
                passanger_gender,
                seat_count,
                passanger_mobile_no,
                passanger_age,
            ]
        ):
            raise Exception("All fields are required")
        if seat_count < 1:
            raise Exception("Seat count must be greater than 0")
        if int(seat_count) > int(availability):
            raise Exception(
                f"Seat count must be less than or equal to availability i.e {availability}"
            )
        if passanger_age < 0 and passanger_age > 100:
            raise Exception("Age must be greater than 0 and less than 100")
        if len(str(passanger_mobile_no)) != 10:
            raise Exception("Mobile number must be 10 digits long")
        self.cursor.execute(
            "INSERT INTO booking_details VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                passanger_name,
                passanger_gender,
                seat_count,
                passanger_mobile_no,
                passanger_age,
                operator_name,
                source,
                destination,
                float(bus_fare) * seat_count,
                running_date,
                datetime.datetime.now().strftime("%Y-%m-%d"),
            ),
        )
        self.cursor.execute(
            "UPDATE running_details SET seats_available = seats_available - ? WHERE running_date = ? AND bus_id = (SELECT bus_id FROM bus_details WHERE bus_fare = ? AND route_id = (SELECT route_id FROM route_details WHERE route_station_name = ?))",
            (seat_count, running_date, bus_fare, source),
        )
        self.connection.commit()

    def get_booking_details(self, passanger_mobile_no):
        self.cursor.execute(
            "SELECT * FROM booking_details WHERE passanger_mobile_no = ?",
            (passanger_mobile_no,),
        )
        return self.cursor.fetchall()
