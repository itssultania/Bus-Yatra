import sqlite3
import re


class OperatorTable:
    EMAIL_REGEX = re.compile(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$")

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS operator_details (operator_id INTEGER PRIMARY KEY,\
                            operator_name TEXT NOT NULL, operator_address TEXT NOT NULL, operator_phone TEXT NOT NULL,\
                            operator_email TEXT NOT NULL)"
        )

    def add_operator(
        self,
        operator_id,
        operator_name,
        operator_address,
        operator_phone,
        operator_email,
        edit_operator: bool = False,
    ):
        if not all(
            [
                operator_id,
                operator_name,
                operator_address,
                operator_phone,
                operator_email,
            ]
        ):
            raise Exception("All fields are required")
        if len(operator_phone) != 10:
            raise Exception("Invalid Phone Number")
        if not re.search(OperatorTable.EMAIL_REGEX, operator_email):
            raise Exception("Invalid Email")
        if not edit_operator:
            self.cursor.execute(
                "INSERT INTO operator_details VALUES (?, ?, ?, ?, ?)",
                (
                    operator_id,
                    operator_name,
                    operator_address,
                    operator_phone,
                    operator_email,
                ),
            )
        else:
            if not self.get_operator(operator_id):
                raise Exception("Operator ID does not exist")
            self.cursor.execute(
                "UPDATE operator_details SET operator_name=?, operator_address=?, operator_phone=?,\
                            operator_email=? WHERE operator_id=?",
                (
                    operator_name,
                    operator_address,
                    operator_phone,
                    operator_email,
                    operator_id,
                ),
            )
        self.connection.commit()

    def get_operator(self, operator_id):
        self.cursor.execute(
            "SELECT * FROM operator_details WHERE operator_id=?", (operator_id,)
        )
        return self.cursor.fetchone()


if __name__ == "__main__":
    db = sqlite3.connect("bus.db")
    cursor = db.cursor()
    operator = OperatorTable(db, cursor)
    # operator.add_operator(3, "SRS Travels", "Bangalore", 12345678, "srs@gmail.com")
    print(operator.get_operator(43))
