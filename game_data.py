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
import textwrap
from typing import Optional, TextIO


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


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - location_number: An integer that represents the location
        - location_name: the name of the location
        - brief_description: A brief description of the location, or None if the location has not been visited
        - long_description: A full description of the location, or None if the location has been visited
        - visited: A boolean value indicates whether the location has been visited or not

    Representation Invariants:
        - 0 <= self.x_cord
        - 0 <= self.y_cord
        - 0 <= self.location_number

    """
    location_number: int
    location_name: str
    brief_description: str
    long_description: str
    visited: bool

    def __init__(self, location_number: int, location_name: str,
                 brief_description: str, long_description: str) -> None:
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

        self.location_number = location_number
        self.location_name = location_name
        self.brief_description = brief_description
        self.long_description = long_description
        self.visited = False

    def look(self) -> str:
        """
        Return the full description for the location.
        """
        return self.long_description


class Player:
    """
    A Player in the text adventure game.

    Instance Attributes:
        - x_cord: The x-coordinate of the player's current location
        - y_cord: The y-coordinate of the player's current location
        - inventory: The player's list of found Item
        - victory: A boolean value indicates whether the player had won or not
        - score: a record of the player's current score

    Representation Invariants:
        - 0 <= self.x_cord
        - 0 <= self.y_cord
    """
    x: int
    y: int
    inventory: list[str]
    victory: bool
    score: int
    got_cheatsheet_from_sadia: bool

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
        self.score = 0
        self.got_cheatsheet_from_sadia = False

    def cond_of_victory(self) -> None:
        """
        The 2 conditions of winning:
        - The player's final position is (3, 5), where the Exam Centre is,
        - The player has all the academic weapons prepared for the exam.
        """
        all_items = all(item in self.inventory for item in ['Cheat Sheet', 'T-card', 'Lucky pen'])
        if (self.x == 2 and self.y == 6) and all_items:
            self.victory = True


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

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """
        Return a list of locations in the location_data.
        """
        locations = []
        line = location_data.readline().strip()
        while line != '':
            if line.startswith('LOCATION'):
                data = line.split(',')
                location_name, location_num = [item for item in data]
                short = location_data.readline().strip()
                long = location_data.readline().strip()
                curr = ''
                while curr != 'END':
                    long += curr
                    curr = location_data.readline().strip()

                locations.append(Location(int(location_num), location_name,
                                          textwrap.fill(short, 100), textwrap.fill(long, 100)))

            line = location_data.readline().strip()

        return locations

    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Return a list of items in the items_data.
        """
        items = []
        line = items_data.readline().strip()
        while line != '':
            data = line.strip().split(',')
            start_position, target_position, target_points, name = [item for item in data]
            items.append(Item(str(name), int(start_position), int(target_position), int(target_points)))
            line = items_data.readline().strip()

        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[0]) and self.map[y][x] != -1:
            for location in self.locations:
                if self.map[y][x] == location.location_number:
                    return location
        return None

    def available_actions(self, location: Location, player: Player) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        actions = ['[menu]', 'score', 'north', 'south', 'west', 'east']
        for item in self.items:
            if location.location_number == item.start_position and not player.got_cheatsheet_from_sadia:
                actions.append('pick')
        if 'Backpack' in player.inventory:
            actions.append('open')
        if player.x == 6 and player.y == 5:
            actions.append('say hi')

        return actions

    def pick(self, location: Location, player: Player) -> str:
        """
        Pick up the item and store in player's inventory and return item name.
        The item is also removed from this location.
        """
        item_name = ''
        for item in self.items:
            if item.start_position == location.location_number:
                player.inventory.append(item.name)
                item_name = item.name
                item.start_position = -1

        return item_name

    def open_backpack(self, player: Player) -> None:
        """
        Open the backpack and get the lucky pen that is inside the bag.
        """
        for item in self.items:
            if item.name == 'Backpack':
                item.name = 'Lucky pen'
        player.inventory.remove('Backpack ')
        player.inventory.append('Lucky pen')

