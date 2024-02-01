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
def do_action(player: Player, user_choice: str) -> str:
    """
    Do the action of user's choice and return the action done.
    """
    action_done = ''
    if user_choice.lower() == 'east':
        player.x += 1
        action_done = 'east'
    elif user_choice.lower() == 'west':
        player.x -= 1
        action_done = 'west'
    elif user_choice.lower() == 'north':
        player.y -= 1
        action_done = 'north'
    elif user_choice.lower() == 'south':
        player.y += 1
        action_done = 'south'
    return action_done


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


# w and choice are not yet defined here so there is an issue
def check_valid_action(w: World, choice: str, location: Location, player: Player) -> bool:
    """
    Return whether if the player's next action is valid
    """
    prep_action = do_action(player, choice)
    if w.get_location(player.x, player.y) is None or location.location_number == -1:
        undo_action(p, prep_action)
        return False
    else:
        undo_action(p, prep_action)
        return True


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    total_steps_count = 0
    menu = ["look", "inventory", "score", "quit", "back"]

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
            if check_valid_action(w, choice, location, p):
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

        # Reset all the data if the player's choice is 'quit'.
        if choice.lower() == 'quit':
            print('You exit the game. You can reload the page to start a new game.')
            break

        if total_steps_count > 25:
            print('Times up! You failed to make it to the test. Try again!')
            break





    p.cond_of_victory()
    if p.victory:
        print("Congratulations! You have everything you need before the exam starts and You \
        came to the Exam Centre on time! Good luck on your test!")
    else:
        print("You failed to make it to the test. Try again!")
