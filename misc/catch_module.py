"""
Author: Corwin Broekhuizen & Philip Stenger
Date created: 25/07/2023
Description: A module to define the Catch class and all related functions.

Note on naming conventions:
    - GLOBAL_CONSTANTS: All uppercase, separated by underscores.
    - Classes: TitleCase (also known as CamelCase).
    - local_variables: snake_case, all lowercase, separated by underscores.
    - functions: snake_case, all lowercase, separated by underscores.
"""

class Catch:
    """
    The Catch class defines a container for details about a catch, including the species, catch time, 
    total weight and count of the creatures.

    Attributes:
        - id (str): Identifier for the Catch object.
        - creatures (list): List of creatures in the catch.
        - time (str): The time when the catch was made.
        - location (str): The location where the catch was made.
        - weight (float): The total weight of the catch.
        - num_creatures (int): The count of creatures in the catch.

    Note: If adding/removing an attribute, ensure to update both __init__ and __repr__ methods accordingly.
    """

    def __init__(self, id=None, creatures=None, time=None, location=None, weight=None, num_creatures=None):
        """Initialize a new Catch instance."""
        self.id = id
        self.creatures = [creatures] if creatures is not None else []
        self.time = time
        self.location = location
        self.weight = weight
        self.num_creatures = num_creatures

    def __str__(self):
        """Return a string representation of a Catch instance."""
        return f'Object: Catch, ID: {self.id}'

    def __repr__(self):
        """Return a comprehensive string representation of a Catch instance."""
        return f'Catch(id={self.id}, creatures={self.creatures}, time={self.time}, location={self.location}, weight={self.weight}, num_creatures={self.num_creatures})'

    def set_id(self, time, location):
        """Generate an identifier for the Catch instance in the format 'C{location}{datetime}', ensuring no spaces."""
        self.id = f'C{location}{time}'

    def add_creature(self, new_creature):
        """Add a new creature to the catch."""
        self.creatures.append(new_creature)

    def set_time(self, date_time):
        """Set the time the catch was made."""
        self.time = date_time

    def set_location(self, location):
        """Set the location where the catch was made."""
        self.location = location

    def calculate_weight(self):
        """Calculate the total weight of the catch."""
        self.weight = sum(creature.weight for creature in self.creatures)

    def count_creatures(self):
        """Count the number of creatures in the catch."""
        self.num_creatures = len(self.creatures)



