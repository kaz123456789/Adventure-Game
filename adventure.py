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
def do_action(player: Player, user_choice: str) -> None:
    """
    Do the action of user's choice and return the action done.
    """
    if user_choice.lower() == 'east':
        player.x += 1
    elif user_choice.lower() == 'west':
        player.x -= 1
    elif user_choice.lower() == 'north':
        player.y -= 1
    elif user_choice.lower() == 'south':
        player.y += 1
    return


def undo_action(player: Player, user_choice: str) -> None:
    """
    Undo the action that was made by the player.
    """
    if user_choice.lower() == 'east':
        player.x -= 1
    elif user_choice.lower() == 'west':
        player.x += 1
    elif user_choice.lower() == 'north':
        player.y += 1
    elif user_choice.lower() == 'south':
        player.y -= 1
    return


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    total_steps_count = 0
    menu = ["look", "inventory", "score", "restart", "back"]

    print('Welcome to Kathleen & Yanting\'s adventure world! \n')
    print('Your adventure starts here! \n')
    print('It is 10am right now.')

    while not p.victory:
        location = w.get_location(p.x, p.y)
        temp = location.item

        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        # Print initial words and instructions

        print("What to do? \n")
        for action in w.available_actions(location, p):
            print(action)
        choice = input("\nEnter action: ")
        total_steps_count += 1

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

        # Check if the player's choice is in the available actions and ask the player to
        # make another choice if needed.
        while choice.lower() not in w.available_actions(location, p) and choice not in menu:
            print("This is not a valid action\n")
            for action in w.available_actions(location, p):
                print(action)
            choice = input("\nEnter action: ")
            total_steps_count += 1

        # Add the item in player's inventory if the player's choice is 'pick'.
        if choice.lower() == 'pick':
            p.inventory += temp
            location.item = ''

        # Print the inventory list if the player's choice is 'inventory'.
        if choice.lower() == "inventory":
            print('[inventory:]')
            for item in p.inventory:
                print(item)

        # Print the player's score if their choice is 'score'.
        if choice.lower() == 'score':
            print(p.score)

        pre_action = None
        if choice.lower() == 'east' or 'west' or 'south' or 'north':

            if (0 <= p.x + 1 <= 5) and (0 <= p.y + 1 <= 5):
                do_action(p, choice)
                if not location.visited:
                    location.visited = True
                    print(location.location_name)
                    print(location.long_description)
                    p.score += 1
                else:
                    print(location.location_name)
                    print(location.brief_description)
            else:
                print('You cannot go this way.')
                print('You\'ve reached the boarder of the school')

        # Print the long description if the player's choice is 'look'.
        if choice.lower() == 'look':
            print(location.look())

        # Reset all the data if the player's choice is 'restart'.
        if choice.lower() == 'restart':
            total_steps_count = 0
            p = Player(0, 0)
            p.inventory = []
            p.score = 0
            location.item = temp



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

    p.cond_of_victory()
    if p.victory:
        print("Congratulations! You won the game! Good luck on your test!")
