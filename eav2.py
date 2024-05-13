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

  def __str__(self):
    """
    Returns a string representation of the entity.
    """
    attributes = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if k != "name")
    return f"Entity(name='{self.name}', {attributes})"

  def get(self, key):
    """
    Retrieves the value of an attribute.

    Args:
      key: The attribute name.

    Returns:
      The value of the attribute or None if not found.
    """
    return getattr(self, key, None)

  def set(self, key, value):
    """
    Sets the value of an attribute.

    Args:
      key: The attribute name.
      value: The value to set.
    """
    setattr(self, key, value)

if __name__ == '__main__':
    
    print('eav2.py:')
    # Create a dictionary of attributes
    attributes = {"age": 30, "city": "New York", "interests": ["music", "reading"]}

    # Create an entity using the dictionary
    customer = Entity("John Doe", **attributes)

    # Print the entity details
    print(customer)


    import json

    # Load the data from the JSON file
    with open("customer.json", "r") as f:
      data = json.load(f)

    # Create the Entity object
    customer = Entity(**data)  # Unpack the dictionary using double asterisk

    # Print the entity details
    print(customer)
