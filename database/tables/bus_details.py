import sqlite3


class BusTable:
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS bus_details (bus_id INTEGER NOT NULL,\
                            bus_type TEXT NOT NULL, bus_capacity INTEGER NOT NULL,\
                            bus_fare REAL NOT NULL, operator_id INTEGER NOT NULL,route_id INTEGER NOT NULL,\
                            PRIMARY KEY (bus_id, route_id))"
        )

    def add_bus(
        self,
        bus_id,
        bus_type,
        bus_capacity,
        bus_fare,
        operator_id,
        route_id,
        edit_bus: bool = False,
    ):
        if not all([bus_id, bus_type, bus_capacity, bus_fare, operator_id, route_id]):
            raise Exception("All fields are required")
        if bus_capacity < 0:
            raise Exception("Invalid Capacity")
        if bus_fare < 0:
            raise Exception("Invalid Fare")
        if not edit_bus:
            self.cursor.execute(
                "INSERT INTO bus_details VALUES (?, ?, ?, ?, ?, ?)",
                (bus_id, bus_type, bus_capacity, bus_fare, operator_id, route_id),
            )
        else:
            if not self.get_bus(bus_id):
                raise Exception("Bus ID does not exist")
            self.cursor.execute(
                "UPDATE bus_details SET bus_type=?, bus_capacity=?, bus_fare=?,\
                            operator_id=?, route_id=? WHERE bus_id=?",
                (bus_type, bus_capacity, bus_fare, operator_id, route_id, bus_id),
            )
        self.connection.commit()

    def get_bus(self, bus_id):
        self.cursor.execute("SELECT * FROM bus_details WHERE bus_id=?", (bus_id,))
        return self.cursor.fetchone()


if __name__ == "__main__":
    db = sqlite3.connect("bus.db")
    cursor = db.cursor()
    bus = BusTable(db, cursor)
    bus.add_bus(1, "AC 2x2", 40, 1000.00, 1, 1)
    # bus.add_bus(1, "AC 2x2", 40, 1000.00, 1, 5)
    # bus.add_bus(2, "AC 2x2", 40, 1000.00, 1, 6)
    print(bus.get_bus(1))
