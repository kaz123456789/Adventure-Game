"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - _x: The x-coordinate of the current location
        - _y: The y-coordinate of the current location
        - _location_number: An integer that represents the location
        - _brief_description: A brief description of the location, or None if the location has not been visited
        - _long_description: A full description of the location, or None if the location has been visited
        - _actions: A list of available actions in the current location
        - _visited: A boolean value indicates whether the location has been visited or not

    Representation Invariants:
        - 0 <= self._x <= 10
        - 0 <= self._y <= 10

    """
    _x: int
    _y: int
    _location_number: int
    _brief_description: Optional[str]
    _long_description: Optional[str]
    _actions: list[str]
    _visited: bool

    def __init__(self, x: int, y: int, location_number: int, brief_description: str,
                 long_description: str, actions: list[str]) -> None:
        """Initialize a new location."""

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        self._x = x
        self._y = y
        self._location_number = location_number
        self._brief_description = brief_description
        self._long_description = long_description
        self._actions = actions
        self._visited = False

    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        # TODO: Complete this method, if you'd like or remove/replace it if you're not using it


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - start_position: The number position of where the item is located.
        - target_position: The number of position of where the item is to be deposited for credit.
        - target_points: The number of point rewarded if the item has been successfully delivered to the credit place.

    Representation Invariants:
        - self.name != ''
        - self.start_position >= 0
        - self.target_position >= 0
    """
    name: str
    start_position: int
    target_position: int
    target_points: int

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - _x: The x-coordinate of the player's current location
        - _y: The y-coordinate of the player's current location
        - _inventory: The player's list of found Item 
        - _victory: A boolean value indicates whether the player had won or not

    Representation Invariants:
        - 0 <= self._x <= 10
        - 0 <= self._y <= 10
    """
    _x: int
    _y: int
    _inventory: list[str]
    _victory: bool

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a list of Location of this world's map
        - items: a list of Item that are available on the map

    Representation Invariants:
        - self.map != [[]]
    """
    map: list[list[int]]
    locations = list[Location]
    items = list[Item]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(items_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map_lst = [list(map(int, row.split())) for row in map_data]
        return map_lst

    # TODO: Complete this method as specified. Do not modify any of this function's specifications.

    # TODO: Add methods for loading location data and item data (see note above).
    def load_locations(self, location_data: TextIO) -> list[Location]:
        """
        Return a list of locations in the location_data.
        """
        locations = []
        for line in location_data:
            if line.startswith('LOCATION'):
                data = line.strip().split()
                location_num, x, y = [item for item in data[1:]]
                locations.append(Location(int(x), int(y), int(location_num)))
        return locations
    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Return a list of items in the items_data.
        """
        items = []
        for line in items_data:
            data = line.strip().split()
            start_position, target_position, target_points, name = [item for item in data]
            items.append(Item(str(name), int(start_position), int(target_position), int(target_points)))

        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]) and self.map[x][y] != -1:
            return self.locations[self.map[x][y]]
        return None
