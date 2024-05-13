class EAVModel:
    def __init__(self):
        self.entities = {}  # Dictionary to store entities and their attributes

    def add_entity(self, entity_name):
        """Add a new entity to the model."""
        if entity_name not in self.entities:
            self.entities[entity_name] = {}

    def add_attribute(self, entity_name, attribute_name, value):
        """Add an attribute-value pair to an existing entity."""
        if entity_name in self.entities:
            self.entities[entity_name][attribute_name] = value

    def get_value(self, entity_name, attribute_name):
        """Get the value of an attribute for a given entity."""
        if entity_name in self.entities:
            return self.entities[entity_name].get(attribute_name)

    def list_entities(self):
        """List all entities in the model."""
        return list(self.entities.keys())

# Example usage:
eav_model = EAVModel()
eav_model.add_entity("Person")
eav_model.add_attribute("Person", "Name", "John Doe")
eav_model.add_attribute("Person", "Age", 30)

print('eav4.py:')
print(f"Entities: {eav_model.list_entities()}")
print(f"Name of Person: {eav_model.get_value('Person', 'Name')}")
print(f"Age of Person: {eav_model.get_value('Person', 'Age')}")

