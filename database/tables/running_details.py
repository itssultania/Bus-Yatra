import sqlite3
import re


class RunningTable:
    DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS running_details (bus_id INTEGER NOT NULL,\
                            running_date TEXT NOT NULL, seats_available INTEGER NOT NULL,\
                            PRIMARY KEY (bus_id, running_date))"
        )

    def add_running(self, bus_id, running_date, seats_available):
        if not all([bus_id, running_date, seats_available]):
            raise Exception("All fields are required")
        if not re.search(RunningTable.DATE_REGEX, running_date):
            raise Exception("Invalid Date [YYYY-MM-DD]")
        query_result = self.cursor.execute(
            "SELECT bus_capacity FROM bus_details WHERE bus_id=?", (bus_id,)
        ).fetchone()
        if not query_result:
            raise Exception("Bus ID does not exist")
        bus_capacity = query_result[0]
        if seats_available > bus_capacity:
            raise Exception("Seats Available cannot be greater than Bus Capacity")
        self.cursor.execute(
            "INSERT INTO running_details VALUES (?, ?, ?)",
            (bus_id, running_date, seats_available),
        )
        self.connection.commit()

    def delete_running(self, bus_id, running_date):
        if not self.get_running(bus_id):
            raise Exception("Bus ID does not exist")
        self.cursor.execute(
            "DELETE FROM running_details WHERE bus_id=? AND running_date=?",
            (
                bus_id,
                running_date,
            ),
        )
        self.connection.commit()

    def get_running(self, bus_id):
        self.cursor.execute("SELECT * FROM running_details WHERE bus_id=?", (bus_id,))
        return self.cursor.fetchone()


if __name__ == "__main__":
    db = sqlite3.connect("bus.db")
    cursor = db.cursor()
    running = RunningTable(db, cursor)
    # running.add_running(1, "2021-01-01", 40)
    # running.add_running(1, "2021-01-02", 40)
    # running.add_running(2, "2021-01-01", 40)
    print(running.get_running(2))
