from db import cursor, conn

class Category:
    TABLE_NAME = "categories"

    def __init__(self, name) -> None:
        self.id = None
        self.name = name

    def save(self):
        sql = f"""
        INSERT INTO {self.TABLE_NAME} (name)
        VALUES (?)
        """
        cursor.execute(sql, (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        print(f"{self.name} saved")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    @classmethod
    def find_all(cls):
        sql = f"""
        SELECT * FROM {cls.TABLE_NAME}
        """
        rows = cursor.execute(sql).fetchall()
        return [
            cls.row_to_instance(row).to_dict() for row in rows
        ]

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None
        
        category = cls(row[1])
        category.id = row[0]
        return category

    @classmethod
    def create_table(cls):
        sql = f"""
             CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()
        print(f"Category table created")

Category.create_table()


# category_names = ["Engine", "Powertrain", "Transmission", "Driveshaft", "Axles", "Wheel", "Suspension", "Steering", "Brakes", "Body", "Interior"]

# for name in category_names:
#     category = Category(name)
#     category.save()
