# Loot 2D
2D RPG game using pygame. Let's see where this goes.

TODO
(1) Implement Main Menu
    X Move Main Menu creation code into class or function definition
    X 3 Layer Sprites
    X Front - Character Selection
        X Make character position dynamically calculated
        X Implement Character Selection
            X Need to handle if savefiles dont exist
    X Front - Additional Options
        X Add Options Button (Should most likely be sprites)
        X If character is chosen --> give option to [LoadGame | DeleteGame -> [Confirmation]]
        X If blank character is chosen --> query [NewGame]
    X Middle - Static Castle Sprite
    X Back - Moving Enviroment Background
        X Make Translations smoother
        X Use RNG to generate random transformation on a set number of clouds for the background
            X size, speed, transparency, location etc
            X when scaling we need to keep the aspect ratio

X Clear surface buffer at the beginning of every loop
    X Look into python memory managment

Implement Basic Inventory Interface
    Inventory (set static size)
        - Add currency counter
        - Inventory.add method needs to be able to handle all item/currency/power types
        - Implement panel navigation with cursor sprite
        - Implement equiping item from backpack (depending on types)
            * Equiping item from backpack needs to check if backpack space is required
            * Same with unequiping
        - Implement backpack scrolling
        - Implement equipment slot type lock
    Inventory Overview Page
        - Display currency (implement coin for now)
        - Implement toggle between inventory tabs

Item Types
    - determine how to implement item type heiarchy
    - gear will be upgraded (in terms of stats)
    - imlpement weapon types
    - coins and potions will be the only other item types
        * should still implement a dynamic item heiarchy so it can be easily changed


Implement Character Creation Page
    - Transition from main menu to character creation

Implement a Better Collision Detection Method

Add Audio
    - Sound effects
    - Background Music

Implement Loading Screen
    - Display Percentage and Errors in loading

Implement Heads Up Display
    - HEALTH, MP
    - Wallet (Currency count)

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
Need to clean up variables and images that are not used