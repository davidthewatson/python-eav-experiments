from peewee import *
from playhouse.shortcuts import model_to_dict

# Database connection
db = SqliteDatabase('eav.db')

class Entity(Model):
    name = CharField(unique=True)

    def __str__(self):
        return self.name  # Return just the name for printing

    class Meta:
        database = db


class Attribute(Model):
    name = CharField(unique=True)

    def __str__(self):
        return self.name  # Return just the name for printing

    class Meta:
        database = db


class Value(Model):
    entity = ForeignKeyField(Entity, backref='values')
    attribute = ForeignKeyField(Attribute, backref='values')
    value = TextField()

    def __str__(self):
        return f"{self.attribute}: {self.value}"  # Format attribute:value pair

    class Meta:
        database = db


def create_tables():
    """Create the Entity, Attribute, and Value tables in the database."""
    db.create_tables([Entity, Attribute, Value])


def add_entity(name):
    """Add a new entity to the database."""
    entity, created = Entity.get_or_create(name=name)
    return entity


def add_attribute(name):
    """Add a new attribute to the database."""
    attribute, created = Attribute.get_or_create(name=name)
    return attribute


def add_value(entity, attribute, value):
    """Add a value for a specific entity and attribute."""
    Value.create(entity=entity, attribute=attribute, value=value)


def set_entities_attributes_values(entities):
    """
    Set entities, attributes, and values in one function call.

    Args:
        entities (list): A list of dictionaries representing entities.
            Each dictionary should have a 'name' key and an 'attributes' key.
            The 'attributes' key should be a list of dictionaries, where
            each inner dictionary has an 'attribute' key (attribute name)
            and a 'value' key (attribute value).
    """
    for entity_data in entities:
        entity_name = entity_data['name']
        entity = add_entity(entity_name)
        for attribute_data in entity_data['attributes']:
            attribute_name = attribute_data['attribute']
            attribute = add_attribute(attribute_name)
            add_value(entity, attribute, attribute_data['value'])


def get_entity_attributes(entity_name):
    """Get all attributes and their values for a specific entity."""
    entity = Entity.get(Entity.name == entity_name)
    values = Value.select().join(Attribute).where(Value.entity == entity)
    return [str(value) for value in values]  # Use __str__ of Value for formatting


def get_entities():
    """Get all entities along with their attribute-value pairs."""
    entities = [entity for entity in Entity.select()]
    for entity in entities:
        attributes = get_entity_attributes(entity.name)
        entity.attributes = list(set(attributes))  # Remove duplicates
    return entities


if __name__ == '__main__':
    print('eav1.py:')
    create_tables()

    # Example usage
    entities = [
        {
            'name': 'Customer',
            'attributes': [
                {'attribute': 'name', 'value': 'John Doe'},
                {'attribute': 'email', 'value': 'john.doe@example.com'},
            ]
        },
        {
            'name': 'Product',
            'attributes': [
                {'attribute': 'name', 'value': 'T-Shirt'},
                {'attribute': 'price', 'value': '19.99'},
            ]
        },
    ]

    set_entities_attributes_values(entities)

    stored_entities = get_entities()
    for entity in stored_entities:
        print(entity)  # Print entity name using __str__ of Entity
        for attribute_value_pair in entity.attributes:
            print(f"\t{attribute_value_pair}")  # Print attribute:value pair


