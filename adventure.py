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


def check_valid_action(world: World, player_choice: str,
                       curr_location: Location, player: Player) -> bool:
    """
    Return whether if the player's next action is valid.
    """
    prep_action = do_action(player, player_choice)
    if world.get_location(player.x, player.y) is None or curr_location.location_number == -1:
        undo_action(p, prep_action)
        return False
    else:
        undo_action(p, prep_action)
        return True


if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 2)  # set starting location of player; you may change the x, y coordinates here as appropriate\
    temp = Player(0, 2)  # a copy of player's location
    total_steps_count = 0
    menu = ["look", "inventory", "score", "steps", "quit", "back"]

    print('[BACKGROUND STORY]')
    print('You, Kathleen, is having your final tonight, but your campus study spree from last night has \n' +
          'turned into a wild mystery! This morning, you\'re missing three vital things – your T-card, \n' +
          'your lucky pen, and the packed cheat sheet. The clock is ticking, and your academic fate hangs \n' +
          'in the balance. You\'ve got to backtrack, find your stuff scattered around campus before the \n' +
          'exam starts tonight. It\'s a race against time and academic obstacles. Can you conquer the \n' +
          'unexpected hurdles and meet your CS buddy Yanting at the Exam Centre on time? Hurry up and \n' +
          'start your adventure! \n')

    while not p.victory:
        location = w.get_location(p.x, p.y)

        if not location.visited:
            location.visited = True
            print(location.location_name)
            print(location.long_description)
            p.score += 1
        else:
            # Only print the location name and brief description when the player's location
            # changes after executing the player's <choice>.
            if p.x != temp.x or p.y != temp.y:
                print(location.location_name)
                print(location.brief_description)

        # Depending on whether it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        # Print initial words and instructions

        print("\nWhat to do? \n")
        for action in w.available_actions(location, p):
            print(action)
        choice = input("\nEnter action: ")
        total_steps_count += 1

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            total_steps_count += 1

        # Check if the player's choice is in the available actions and ask the player to
        # make another choice if needed.
        while choice.lower() not in w.available_actions(location, p) and choice not in menu:
            print("\nThis is not a valid action\n")
            for action in w.available_actions(location, p):
                print(action)
            choice = input("\nEnter action: ")
            print('')
            total_steps_count += 1

        # Greet and ask Sadia for a cheatsheet if the player has arrived at LOCATION 26
        if choice.lower() == 'say hi':
            print('You: Hi Sadia! I really need your help! I pulled a all-nighter yesterday to study and \n' +
                  'I can\'t find my cheat sheet for the final right now. I really don\'t know what to do... \n')
            print('Saida:\'Awwww, that sounds awful... Here, (hands a cheatsheet written by *HERSELF*) \n' +
                  'good luck on your exam and have a wonderful summer break.')
            print('\nYou thanked Sadia for her kindness of helping you.')
            get_cheatsheet_from_sadia = True
            p.inventory.append('Sadia\'s Cheatsheet')
            temp.x, temp.y = p.x, p.y

        # Add the item in player's inventory if the player's choice is 'pick'.
        if choice.lower() == 'pick':
            item = w.pick(location, p)
            print('\nYou\'ve picked up ' + item)
            temp.x, temp.y = p.x, p.y

        # Allow the player to drop item (in their inventory) at any location
        if choice.lower() == 'drop':
            if location.location_number == 17:
                print('Littering is not premitted on the lawn!!')
            else:
                item_dropped = input('Which item do you want to drop?')
                if item_dropped not in p.inventory:
                    print('You can\'t drop something you don\'t have')
                else:
                    w.drop_item(location, p, item_dropped)
                    print('You\'ve dropped ' + item_dropped)

        # Print the inventory list if the player's choice is 'inventory'.
        if choice.lower() == "inventory":
            print('\n[inventory]')
            for item in p.inventory:
                print(item)
            temp.x, temp.y = p.x, p.y

        # Checks if the next action is valid, if yes, then make the move
        if choice.lower() == 'east' or 'west' or 'south' or 'north':
            if check_valid_action(w, choice, location, p):
                do_action(p, choice)
                print('')
            else:
                print('\nThis way is blocked.')
                print('You cannot go this way.')

        # Player can enter the Robarts Library if they've pick up their T-Card,
        # otherwise, they have to go back and get the T-Card before entering the library.
        if p.x == 2 and p.y == 1:
            if 'T-Card' not in p.inventory:
                undo_action(p, choice)
                print('You cannot get in the Robarts Library without your T-Card. \n' +
                      'Get your T-Card and come back again! Hurry up!')

        # Print the player's score if their choice is 'score'.
        if choice.lower() == 'score':
            print('\nYour current score is: ' + str(p.score) + '\n')
            temp.x, temp.y = p.x, p.y

        # Print the player's total steps count if their choice is 'steps'.
        if choice.lower() == 'steps':
            print('\nYour total steps count is: ' + str(total_steps_count) + '\n')
            temp.x, temp.y = p.x, p.y

        # Print the long description if the player's choice is 'look'.
        if choice.lower() == 'look':
            print(location.look())
            temp.x, temp.y = p.x, p.y

        # The player can open their backpack if this action is valid
        if choice.lower() == 'open':
            w.open_backpack(p)
            print('\nYou\'ve opened backpack' + '\n')
            p.score += 5
            temp.x, temp.y = p.x, p.y

        # Reset all the data if the player's choice is 'quit'.
        if choice.lower() == 'quit':
            print('You exit the game. You can reload the page to start a new game.\n')
            break

        if total_steps_count > 40:
            print('Times up! You failed to make it to the test. Try again!\n')
            break

        if p.x == 2 and p.y == 6:
            p.cond_of_victory()
            for item in w.items:
                if item in p.inventory and location.location_number == item.target_position:
                    p.score += item.target_points

    if p.victory:
        print('You finally arrived at EX100.\n'
              'Congratulations! You have everything you need before the exam starts '
              'and You came to the Exam Centre on time! \n' +
              'Yanting has been waiting for you for a while. Good luck on your final exam Kathleen!')
    else:
        print("You failed to make it to the test. Try again!")
