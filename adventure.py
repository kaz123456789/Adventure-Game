"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player


# Note: You may add helper functions, classes, etc. here as needed
def do_action(world: World, player: Player, user_choice: str) -> Location:
    """
    Return the location of the current position of the player.
    """
    if user_choice.lower() == 'east':
        player.y += 1
    elif user_choice.lower() == 'west':
        player.y -= 1
    elif user_choice.lower() == 'north':
        player.x += 1
    elif user_choice.lower() == 'south':
        player.x -= 1
    return world.get_location(player.x, player.y)


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "restart", "back"]

    while not p.victory:
        location = w.get_location(p.x, p.y)

        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION

        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        # Print initial words and instructions
        print('Welcome to Kathleen & Yanting\'s adventure world! \n')
        print('Your adventure starts here! \n')
        print("What to do? \n")
        print("[menu]")
        for action in location.actions:
            print(action)
        choice = input("\nEnter action: ")

        # Check if the player's choice is in the available actions and ask the player to
        # make another choice if needed.
        while choice not in location.actions and choice not in menu:
            print("This is not a valid action\n")
            print("[menu]")
            for action in location.actions:
                print(action)
            choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

        # Add the item in player's inventory if the player's choice is 'pick'.
        if choice.lower() == 'pick':
            for item in w.items:
                if location.location_number == item.start_position:
                    p.inventory += [item.name]
                    p.score += 5

        # Print the brief description if the player's choice is 'look'.
        if choice.lower() == 'look':
            print(location.brief_description)

        # Print the inventory list if the player's choice is 'inventory'.
        if choice.lower() == "inventory":
            print(p.inventory)

        # Print the player's score if their choice is 'score'.
        if choice.lower() == 'score':
            print(p.score)

        # Reset all the data if the player's choice is 'quit'.
        # 我有点不太懂这个restart要怎么去把所有已经有的data全部归零

        if choice.lower() not in menu or choice.lower() not in location.actions:
            do_action(w, p, choice)
            if not location.visited:
                print(location.long_description)
                p.score += 1

        if choice.lower() == 'restart':
            p = Player(0, 0)
            p.inventory = []
            p.score = 0



        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
