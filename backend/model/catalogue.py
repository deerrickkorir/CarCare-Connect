from db import cursor, conn  # Assuming these are correctly imported

class Category:
    TABLE_NAME = "categories"

    def __init__(self, name, description, image, supplier, price):
        self.id = None
        self.name = name
        self.description = description
        self.image = image
        self.supplier = supplier
        self.price = price

    def save(self):
        sql = f"""
        INSERT INTO {self.TABLE_NAME} (name, description, image, supplier, price)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.description, self.image, self.supplier, self.price))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    def update(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET name = ?, description = ?, image = ?, supplier = ?, price = ?
            WHERE id = ? 
        """
        cursor.execute(sql, (self.name, self.description, self.image, self.supplier, self.price, self.id))
        conn.commit()
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "supplier": self.supplier,
            "price": self.price
        }

    @classmethod
    def find_one(cls, id):
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE id = ?
        """
        row = cursor.execute(sql, (id,)).fetchone()
        return cls.row_to_instance(row)

    @classmethod
    def find_all(cls):
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.row_to_instance(row) for row in rows]

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None
        category = cls(row[1], row[2], row[3], row[4], row[5])
        category.id = row[0]
        return category

    @classmethod
    def create_table(cls):
        sql = f"""
             CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             description VARCHAR NOT NULL,
             image VARCHAR NOT NULL,
             supplier TEXT NOT NULL,
             price INTEGER NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()
        print(f"{cls.TABLE_NAME} table created")

    @classmethod
    def alter_table(cls):
        sql = f"""
            ALTER TABLE {cls.TABLE_NAME}
            ADD COLUMN is_booked BOOLEAN DEFAULT false
        """
        cursor.execute(sql)
        conn.commit()
        print(f"{cls.TABLE_NAME} table altered")

# Example usage:
if __name__ == "__main__":
    Category.create_table()  # Create the table if it doesn't exist
    Category.alter_table()   # Alter the table to add a new column if needed
