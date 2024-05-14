class Data:
    """
    Facade class providing a simple DSL for defining data using either Aristotelian or Rosch models.
    """

    def __init__(self):
        self._data = None

    def define_aristotelian_entity(self, entity_type: str, data_string: str) -> None:
        """
        Defines an Aristotelian entity using a simple key-value string format.

        Args:
            entity_type (str): The type of the entity.
            data_string (str): A comma-separated string of key-value pairs representing attributes.
                e.g., "material=wood,legs=4,backrest=yes"
        """
        attributes = dict(item.split("=") for item in data_string.split(","))
        self._data = AristotelianEntity(entity_type, attributes)

    def define_rosch_prototype(self, concept: str, core_attributes_string: str, variable_attributes_string: str) -> None:
        """
        Defines a Rosch prototype using simple strings for core and variable attributes.

        Args:
            concept (str): The concept represented by the prototype.
            core_attributes_string (str): Comma-separated string of core attribute names.
                e.g., "has_function,made_of_material"
            variable_attributes_string (str): A string in the format "attr1:val1,val2,...;attr2:val3,val4,...".
                e.g., "legs:0,2,4;material:wood,metal,plastic"
        """
        core_attributes = core_attributes_string.split(",")
        variable_attributes = {}
        for attr_data in variable_attributes_string.split(";"):
            attr, values = attr_data.split(":")
            variable_attributes[attr] = values.split(",")
        self._data = RoschPrototype(concept, core_attributes, variable_attributes)

    def get_data(self):
        """
        Returns the underlying data object (AristotelianEntity or RoschPrototype).
        """
        return self._data


# Example usage
data = Data()
data.define_aristotelian_entity("Chair", "material=wood,legs=4,backrest=yes")
entity = data.get_data()
print(entity)  # Output: Chair(material=wood, legs=4, backrest=yes)

data = Data()
data.define_rosch_prototype(
    "Furniture", "has_function,made_of_material", "legs:0,2,4;material:wood,metal,plastic"
)
prototype = data.get_data()
print(prototype)  # Output: Furniture prototype: Core: [has_function, made_of_material], Variable: [legs: 0, 2, 4, material: wood, metal, plastic]

