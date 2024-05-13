import sqlite3
import json

class Entity:
  """
  A class representing an entity with attributes.
  """

  def __init__(self, name, **kwargs):
    """
    Initializes an Entity object.

    Args:
      name: The name of the entity.
      kwargs: A dictionary of key-value pairs representing attributes.
    """
    self.name = name
    self.__dict__.update(kwargs)
    self.storage = None  # Initialize storage flag

  def __str__(self):
    """
    Returns a string representation of the entity.
    """
    attributes = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if k != "name")
    return f"Entity(name='{self.name}', {attributes})"

  @classmethod
  def connect(cls, db_file):
    """
    Establishes a connection to the SQLite database (if enabled).

    Args:
      db_file: The path to the database file (optional).
    """
    if db_file:
      cls.conn = sqlite3.connect(db_file)
      cls.conn.row_factory = sqlite3.Row
      cls.create_table("entities")  # Create the table on connection

  @classmethod
  def create_table(cls, table_name):
    """
    Creates a table for entities in the database (if connected).

    Args:
      table_name: The name of the table to create.
    """
    if hasattr(cls, 'conn'):
      cursor = cls.conn.cursor()
      cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
          name TEXT PRIMARY KEY,
          data TEXT NOT NULL
        )
      """)
      cls.conn.commit()  # Commit table creation

  def save(self):
    """
    Saves the entity to the database (if connected).
    """
    if self.storage and hasattr(self, 'conn'):
      data = json.dumps(self.__dict__)  # Convert entity to JSON string
      cursor = self.conn.cursor()
      cursor.execute(f"""
        INSERT OR REPLACE INTO entities (name, data)
        VALUES (?, ?)
      """, (self.name, data))
      self.conn.commit()  # Commit the insert/replace operation

  @classmethod
  def load(cls, name):
    """
    Loads an entity from the database (if connected).

    Args:
      name: The name of the entity to load.

    Returns:
      An Entity object or None if not found.
    """
    if hasattr(cls, 'conn'):
      cursor = cls.conn.cursor()
      cursor.execute(f"""
        SELECT data FROM entities WHERE name = ?
      """, (name,))
      data = cursor.fetchone()
      if data:
        entity_data = json.loads(data[0])  # Convert JSON string to dictionary
        return Entity(**entity_data)
      else:
        return None
    else:
      return None  # No database connection, return None

  def update(self, **kwargs):
    """
    Updates the entity attributes.
    """
    for key, value in kwargs.items():
      setattr(self, key, value)  # Update entity attributes
    self.save()  # Save changes to storage (if enabled)
    self.conn.commit()  # Commit the update operation

  def delete(self):
    """
    Deletes the entity from the database (if connected).
    """
    if self.storage and hasattr(self, 'conn'):
      cursor = self.conn.cursor()
      cursor.execute(f"""
        DELETE FROM entities WHERE name = ?
      """, (self.name,))
      self.conn.commit()  # Commit the delete operation

# Example usage (in-memory mode)
if __name__ == "__main__":
  print('eav3.py:')
  entity1 = Entity("Item1", value=42)
  print(entity1)

  # Example usage (disk-backed mode)
  Entity.connect("entities.db")  # Connect to the database
  entity2 = Entity("Item2", data="This is some data")
  entity2.storage = True  # Enable storage for this entity
  entity2.save()

  # Load entity from disk
  loaded_entity = Entity
