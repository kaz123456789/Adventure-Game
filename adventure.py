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
    temp_x, temp_y = 0, 2  # a copy of player's most recent move
    total_steps_count = 0
    menu = ["look", "inventory", "score", "steps", "quit", "back"]

    print('[BACKGROUND STORY]')
    print('You, Kathleen, is having your final tonight, but your campus study spree from last night has \n'
          'turned into a wild mystery! This morning, you\'re missing three vital things – your T-card, \n'
          'your lucky pen, and the packed cheat sheet. The clock is ticking, and your academic fate hangs \n'
          'in the balance. You\'ve got to backtrack, find your stuff scattered around campus before the \n'
          'exam starts tonight. It\'s a race against time and academic obstacles. Can you conquer the \n'
          'unexpected hurdles and meet your CS buddy Yanting at the Exam Centre on time? Hurry up and \n'
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
            if p.x != temp_x or p.y != temp_y:
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
            print('You: Hi Sadia! I really need your help! I pulled a all-nighter yesterday to study and \n'
                  'I can\'t find my cheat sheet for the final right now. I really don\'t know what to do... \n')
            print('Saida:\'Awww, that sounds awful... Here, (hands a cheatsheet written by *HERSELF*) \n'
                  'good luck on your exam and have a wonderful summer break.')
            print('\nYou thanked Sadia for her kindness of helping you.')
            get_cheatsheet_from_sadia = True

            # Use temp_x and temp_y as temporary variables to store the player's most recent
            # x, y coordinates after each action except for the Go [direction] commands
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()

        # Add the item in player's inventory if the player's choice is 'pick'.
        if choice.lower() == 'pick':
            item = w.pick(location, p)
            print('\nYou\'ve picked up ' + item)
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # Allow the player to drop item (in their inventory) at any location
        if choice.lower() == 'drop':
            if location.location_number == 17:
                print('\nLittering is not permitted on the lawn!!')
            else:
                item_dropped = input('\nWhich item do you want to drop?')
                if item_dropped not in p.inventory:
                    print('\nYou can\'t drop something you don\'t have')
                else:
                    w.drop_item(location, p, item_dropped)
                    print('\nYou\'ve dropped ' + item_dropped)
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # Print the inventory list if the player's choice is 'inventory'.
        if choice.lower() == "inventory":
            print('\n[inventory]')
            for item in p.inventory:
                print(item)
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # Checks if the next action is valid, if yes, then make the move
        directions = {'east', 'west', 'south', 'north'}
        if choice.lower() in directions:
            # Update temp_x and temp_y so that line 101 will be True after 'do_action' executed
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()
            if check_valid_action(w, choice, location, p):
                do_action(p, choice)
                print('')
            else:
                print('\nThis way is blocked.')
                print('You cannot go this way.')

        # Player can enter the Robarts Library if they've pick up their T-Card,
        # otherwise, they have to go back and get the T-Card before entering the library.
        if p.x == 2 and p.y <= 1:
            if 'T-Card' not in p.inventory:
                undo_action(p, choice)
                print('You cannot get in the Robarts Library without your T-Card. \n'
                      'Get your T-Card and come back again! Hurry up!')

        # Print the player's score if their choice is 'score'.
        if choice.lower() == 'score':
            print('\nYour current score is: ' + str(p.score) + '\n')
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # Print the player's total steps count if their choice is 'steps'.
        if choice.lower() == 'steps':
            print('\nYour total steps count is: ' + str(total_steps_count) + '\n')
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # Print the long description if the player's choice is 'look'.
        if choice.lower() == 'look':
            print(location.look())
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

        # The player can open their backpack if this action is valid
        if choice.lower() == 'open':
            w.open_backpack(p)
            print('\nYou\'ve opened backpack' + '\n')
            p.score += 5
            temp_x, temp_y = p.get_x_cord(), p.get_y_cord()  # same as line 144

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
                p.score += item.target_points
            print('\nYou\'re total score is: ' + str(p.score) + '\n')

    if p.victory:
        print('You finally arrived at EX100.\n'
              'Congratulations! You have everything you need before the exam starts '
              'and You came to the Exam Centre on time! \n'
              'Yanting has been waiting for you for a while. Good luck on your final exam Kathleen!')
    else:
        print("You failed to make it to the test. Try again!")
