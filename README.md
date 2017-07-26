# Loot 2D
2D RPG game using pygame. Let's see where this goes.

TODO
(1) Implement Main Menu
    - Move Main Menu creation code into class or function definition
    - 3 Layer Sprites
    - Front - Character Selection
        * Make character position dynamically calculated
        * Implement Character Selection
    - Front - Additional Options
        * Add Options Label Below Character Selection
    - Middle - Static Castle Sprite
    - Back - Moving Enviroment Background
        * Make Translations smoother
        * Use RNG to generate random transformation on a set number of clouds for the background
            - size, speed, transparency, location etc
            - when scaling we need to keep the aspect ratio

(2) Clear surface buffer at the beginning of every loop
    - Look into python memory managment

Implement Loading Screen
    - Display Percentage and Errors in loading

Implement Heads Up Display
    - HEALTH, MP
    - Wallet (Currency count)

Implement Basic Inventory Interface
    - Backpack / Held Items

Implement Quick Use Slots
    - Abilities and Actions

Implement Menus
    - Shop Menus
    - Inventory
    - Pause Menu

Implement Clothing (overlay other sprites ontop of character / relative to character position)

Implement Attack and Defend Sprite Motion

Dynamic Character Collision Points in a List / Array
Character Size Transformation

Implement Window Resize (Possibly just static and predefined sizes in options menu)

Bugs
Collision Detection is a little off
Maps are rendered with non visible tiles from the adjacent rooms