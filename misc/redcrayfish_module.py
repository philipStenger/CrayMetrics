"""
Author: Corwin Broekhuizen
Date Created: 12/07/2023
Last Edit: 25/07/2023, Corwin Broekhuizen
Description: A module to define the  red crayfish class and all related functions to this class.

Note on code style. 
All upper case: GLOBAL_CONSTANT, 
Tile case: Class, 
Underscore seperation: local_varible, 
Camel case: functionOrFunctionDef
"""

# Imports



# Global constants
MALE = 1
FEMALE = 2
SOFT = 1
EGGS = 1
LEGAL_SIZE_MALE = 54 #The minimum legal width of the primary spine on the second segament of a male red lobster in mm
LEGAL_SIZE_FEMALE = 60 #The minimum legal width of the primary spine on the second segament of a female red lobster in mm

"""Define crayfish class"""
class RedCray(object):
    """
    RedCray class defines an object associated with a single crayfish, it will be used to store infomation about that crayfish. 
    Attributes:
        .weight
        .length
        .area
        .time_caught
        .location_caught
        .id
        .catch_id
        .sex
        .species
        .is_legal
        .has_eggs
        .is_soft

    If addding/removing an attribute make sure to update __init__ AND __repr__
    """

    def __init__(self, *, id=None, catch_id=None, weight=None, length=None, second_segment_width=None, area=None, time_caught=None, \
                 location_caught=None, sex=None, is_legal=None, has_eggs=None, is_soft=None):
        """Creates a new cray object an assigns it to the current catch."""
        self.id = id
        self.catch_id = catch_id
        self.weight = weight
        self.length = length
        self.second_segment_width = second_segment_width
        self.area = area
        self.time_caught = time_caught
        self.location_caught = location_caught
        self.sex = sex
        self.is_legal = is_legal
        self.has_eggs = has_eggs
        self.is_soft = is_soft

    def __str__(self):
        """returns a string of a Cray object in the following form:"""
        return f'Object: RedCray, ID: {self.id}, Catch ID: {self.catch_id}'
    
    def __repr__(self):
        """Returns a string of a Cray object in the following form:"""
        return f'RedCray(id={self.id}, catch_id={self.catch_id}, weight={self.weight}, length={self.length}, second_segment_width={self.second_segment_width}, \
            area={self.area}, time_caught={self.time_caught}, location_caught={self.location_caught}, sex={self.sex}, is_legal={self.is_legal}, \
            has_eggs={self.has_eggs}, is_soft={self.is_soft})'
    
    #psodo code, needs updating once format of time and date are set/understood
    def setId(self, *, time, location):
        """Generates an id for the Cray in the format 'C{location}{datetime}' no spaces in the id"""
        #self.id = f'C{location}{time}'

    def setCatchId(self, catch_id):
        """Sets the catch id attribute of the cray object.
        N.B. Not sure this is a required function."""
        self.catch_id = catch_id

    def calcLength(self):
        """this is for Philip to calculate using computer vision and ai learning"""

    def calcArea(self):
        """this is for Philip to calculate using computer vision and ai learning"""

    def calcWeight(self):
        """this is for Philip to calculate using computer vision and ai learning"""

    #may change this to require no inputs and instead poll the GPS module
    def setTimeCaught(self, date_time):
        """Sets the time caught to the current time from GPS"""
        self.time_caught = date_time

    #may change this to require no inputs and instead poll the GPS module
    def setLocationCaught(self, location):
        """Sets the location caught to the current GPS location"""
        self.time_caught = location

    def checkHasEggs(self):
        """Determined whether the cray has eggs
        N.B. Not sure this is a required function."""

        #for philip
        pass

    def setSex(self, sex):
        """Sets the sex attribute of the cray object.
        N.B. Not sure this is a required function."""
        if sex == MALE or sex == FEMALE:
            self.sex = sex
        else:
            #raise exception
            pass

        if self.sex == FEMALE:
            checkHasEggs()

    def checkIsSoft(self):
        """Determines if the cray has a soft shell.
        N.B. Not sure this is a required function."""

        # For philip to finish
        pass

    def checkLegality (self):
        """Determines if the cray is legal size, based on size, eggs and soft shell."""
        if (self.sex == MALE):
            self.is_legal = ((self.second_segment_width >= LEGAL_SIZE_MALE) and (self.is_soft == SOFT))

        elif (self.sex == FEMALE):
            self.is_legal = ((self.second_segment_width >= LEGAL_SIZE_MALE) and (self.is_soft != SOFT) and (self.has_eggs != EGGS))

        else:
            # raise exception
            pass