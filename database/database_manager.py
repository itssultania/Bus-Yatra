import sqlite3
from .tables.bus_details import BusTable
from .tables.running_details import RunningTable
from .tables.operator_details import OperatorTable
from .tables.route_details import RouteTable
from .tables.booking_details import BookingDetails


class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.operator_table = OperatorTable(self.connection, self.cursor)
        self.route_table = RouteTable(self.connection, self.cursor)
        self.bus_table = BusTable(self.connection, self.cursor)
        self.running_table = RunningTable(self.connection, self.cursor)
        self.booking_table = BookingDetails(self.connection, self.cursor)

    def get_buses(self, from_place, to_place, journey_date):
        return self.cursor.execute(
            "select op.operator_name, b.bus_type, d.seats_available || '/' || b.bus_capacity availability,\
         b.bus_fare from operator_details op, route_details r1 , route_details r2,\
         running_details d , bus_details b where d.running_date = ? and\
         d.seats_available <> 0 and r1.route_id = r2.route_id and r1.route_station_name = ? and r2.route_station_name = ?",
            (journey_date, from_place, to_place),
        ).fetchall()


if __name__ == "__main__":
    db = DatabaseManager("bus.db")
    # print(db.get_buses("Guna", "Mumbai", "2021-05-10"))
    # print(db.bus_table.get_bus(1))
