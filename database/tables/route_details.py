import sqlite3


class RouteTable:
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS route_details (route_id INTEGER,\
                            route_station_name TEXT NOT NULL, route_station_id INTEGER NOT NULL,\
                            PRIMARY KEY (route_id, route_station_id));"
        )

    def add_route(self, route_id, route_station_name, route_station_id):
        if not all([route_id, route_station_name, route_station_id]):
            raise Exception("All fields are required")
        self.cursor.execute(
            "INSERT INTO route_details VALUES (?, ?, ?)",
            (route_id, route_station_name, route_station_id),
        )
        self.connection.commit()

    def delete_route(self, route_id, route_station_id):
        if not self.get_route(route_id, route_station_id):
            raise Exception("Route ID does not exist")
        query_result = self.cursor.execute(
            "SELECT bus_id FROM bus_details WHERE route_id=?", (route_id,)
        ).fetchone()
        if query_result:
            for bus_id in query_result:
                self.cursor.execute(
                    "DELETE FROM running_details WHERE bus_id=?", (bus_id,)
                )
                self.cursor.execute(
                    "DELETE FROM bus_details WHERE route_id=?", (route_id,)
                )
        self.cursor.execute("DELETE FROM route_details WHERE route_id=?", (route_id,))
        self.connection.commit()

    def get_route(self, route_id, route_station_id):
        self.cursor.execute(
            "SELECT * FROM route_details WHERE route_id=? AND route_station_id=?",
            (route_id, route_station_id),
        )
        return self.cursor.fetchone()


if __name__ == "__main__":
    db = sqlite3.connect("bus.db")
    cursor = db.cursor()
    route = RouteTable(db, cursor)
    route.add_route(1, "Bangalore", 1)
    print(route.get_route(1))
