from typing import Dict, Optional

class AristotelianEAV:
    def __init__(self) -> None:
        self.data: Dict[str, Dict[str, Optional[str]]] = {}

    def add_fact(self, entity: str, attribute: str, value: str) -> None:
        if entity not in self.data:
            self.data[entity] = {}
        self.data[entity][attribute] = value

    def get_value(self, entity: str, attribute: str) -> Optional[str]:
        return self.data.get(entity, {}).get(attribute)

# Example usage:
eav_model = AristotelianEAV()
eav_model.add_fact("Person1", "Age", "30")
eav_model.add_fact("Person2", "Age", "25")
print(eav_model.get_value("Person1", "Age"))  # Output: "30"

