import sqlite3

class EAVModel:
    def __init__(self, db_file="eav_database.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.create_eav_table()

    def create_eav_table(self):
        create_eav_table_sql = '''
            CREATE TABLE IF NOT EXISTS eav_data (
                entity_name TEXT,
                attribute_name TEXT,
                value TEXT
            );
        '''
        self.conn.execute(create_eav_table_sql)
        self.conn.commit()

    def add_entity(self, entity_name):
        # Check if the entity already exists
        if not self.get_entity(entity_name):
            self.conn.execute("INSERT INTO eav_data (entity_name) VALUES (?)", (entity_name,))
            self.conn.commit()

    def add_attribute(self, entity_name, attribute_name, value):
        # Check if the entity exists
        entity_id = self.get_entity(entity_name)
        if entity_id:
            self.conn.execute(
                "INSERT INTO eav_data (entity_name, attribute_name, value) VALUES (?, ?, ?)",
                (entity_name, attribute_name, value),
            )
            self.conn.commit()

    def get_value(self, entity_name, attribute_name):
        # Retrieve the value for a given entity and attribute
        result = self.conn.execute(
            "SELECT value FROM eav_data WHERE entity_name = ? AND attribute_name = ?",
            (entity_name, attribute_name),
        ).fetchone()
        return result[0] if result else None

    def get_entity(self, entity_name):
        # Check if the entity exists
        result = self.conn.execute(
            "SELECT rowid FROM eav_data WHERE entity_name = ?", (entity_name,)
        ).fetchone()
        return result[0] if result else None

    def list_entities(self):
        # List all entities
        result = self.conn.execute("SELECT DISTINCT entity_name FROM eav_data")
        return [row[0] for row in result]

    def close_connection(self):
        self.conn.close()

# Example usage:
if __name__ == "__main__":
    print('eav5.py:')
    eav_model = EAVModel()
    eav_model.add_entity("Person")
    eav_model.add_attribute("Person", "Name", "John Doe")
    eav_model.add_attribute("Person", "Age", "30")

    print(f"Entities: {eav_model.list_entities()}")
    print(f"Name of Person: {eav_model.get_value('Person', 'Name')}")
    print(f"Age of Person: {eav_model.get_value('Person', 'Age')}")

    eav_model.close_connection()

