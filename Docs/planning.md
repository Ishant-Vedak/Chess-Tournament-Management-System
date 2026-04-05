# Project Planning — Chess Tournament System

- This is just for planning the current feature I want to address. 

Organizer pipeline (?): 

Creating Tournament:

1. Visit landing page, 
2. click on create tournament in hero, 
3. login/create account (although many find it annoying, but will deal with this later), 
4. fill out tournament form, 
5. receive confirmation email, 
6. gain access to tournament admin page and control participants, staff, be able to link a google forms for participant registration (and probably confirm if fee is paid), 
7. host tournament.

This tournament logic will vary based on type, and I will figure this out later.

Ending Tournament:

1. End tournament, 
2. show final results will all points, 
3. create a file (probably pdf or json or both) containing all data,
4. delete it in 14 days (seems like good amount of time). OR save every tournament until it becomes an issue.


## Current Issues:

1. Frontend.

2. Bulk Import of Participants through CSV. (Google forms has an option to export data as a .csv file)

3.  Managing Color Balance for players. (In a tournament, a player alternates between playing as white and black, so I have to implement a system to do this.)

## Ongoing Solutions:

1. For Managing Color Balance, I am putting 2 fields in the Participant model: color_history and color_balance. 
    - Color history will be a string show the order in which a player has played the colors. For example, 'WBW' will show that the player played White, then Black, and White. 
    - Color balance will be an integer value, starting a 0. If the player plays White, then it increases by 1, and decreases by 1 if the players plays Black. It cannot exceed +2 or -2.




