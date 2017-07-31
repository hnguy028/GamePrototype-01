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
    - Backpack / Held Items

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