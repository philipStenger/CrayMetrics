"""
Author: Corwin Broekhuizen
Date created: 25/07/2023
Last edit: 25/07/2023, Corwin Broekhuizen
Description: A module to define the catch class and all related functions to this class.

Note on code style. 
All upper case: GLOBAL_CONSTANT, 
Tile case: Class, 
Underscore seperation: local_varible, 
Camel case: functionOrFunctionDef
"""

# Imports



# Global constants

"""Define Catch class"""
class Catch(object):
    """Catch class defines a class to handle the details of a catch, including the species, the catch time
    total weight and every animal in the catch

    Attributes:
        .id
        .creatures
        .time
        .location
        .weight
        .num_creatures

     If addding/removing an attribute make sure to update __init__ AND __repr__
    """

    def __init__(self, *, id=None, creatures=None, time=None, location=None, weight=None, num_creatures=None):
        """Creates a new Catch object an assigns it to the current catch."""
        self.id = id
        self.creatures = [creatures]
        self.time = time
        self.location = location
        self.weight = weight
        self.num_creatures = num_creatures


    def __str__(self):
        """returns a string of a Catch object in the following form:"""
        return f'Object: Catch, ID: {self.id}'
    
    def __repr__(self):
        """Returns a string of a Catch object in the following form:"""
        return f'Cray(id={self.id}, creatures={self.self.creatures}, time={self.time}, location={self.location}, weight={self.weight}, \
            num_creatures={self.num_creatures})'
    
    def setId(self, *, time, location):
        """Generates an id for the Catch in the format 'C{location}{datetime}' no spaces in the id"""
        #self.id = f'C{location}{time}'

    def addCreature(self, new_creature):
        """Appends a new creature to the list of the creatures in the catch."""
        self.creatures.append(new_creature)

    def setTime(self, date_time):
        """Sets the time caught to the current time from GPS"""
        self.time_caught = date_time

    def setLocationCaught(self, location):
        """Sets the location caught to the current GPS location"""
        self.time_caught = location

    def calcWeight(self):
        """Calculates the total weight of the catch"""
        total_weight = 0
        for creature in self.creatures:
            total_weight += creature.weight

        self.weight = total_weight

    def calcNumCreatures(self):
        """Counts the number of creatures in the catch"""
        self.num_creatures = len(self.creatures)


