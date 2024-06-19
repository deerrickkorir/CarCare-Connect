from db import conn, cursor

class Bought:
    TABLE_NAME = "bought"

    def __init__(self, bought_from, bought_to, bought_fee, catalogue_id, user_id):
        self.id = None
        self.bought_from = bought_from
        self.bought_to = bought_to
        self.bought_fee = bought_fee
        self.catalogue_id = catalogue_id
        self.user_id = user_id

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (bought_from, bought_to, bought_fee, catalogue_id, user_id)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.bought_from, self.bought_to, self.bought_fee, self.catalogue_id, self.user_id))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bought_from DATE NOT NULL,
                bought_to DATE NOT NULL,
                bought_fee INTEGER NOT NULL,
                catalogue_id INTEGER NOT NULL REFERENCES categories (id),
                user_id INTEGER NOT NULL REFERENCES users (id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(sql)
        conn.commit()
        print(f"{cls.TABLE_NAME} table created")

# Example usage for Booking
if __name__ == "__main__":
    Bought.create_table()  # Create the table if it doesn't exist

    # Example: Inserting a booking
    bought = Bought("2024-06-20", "2024-06-25", 200, 1, 1)  # Assuming catalogue_id and user_id exist
    bought.save()
    print(f"Booking ID: {bought.id}")
