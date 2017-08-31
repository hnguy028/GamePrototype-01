# Loot 2D
2D RPG game using pygame. Let's see where this goes.

TODO
- function.py
check_portal()
    - Redo player-portal collision, using player.get_center()
    - move the check_portal() method
    - possible combine portal and spawn_point? - add property to portal for spawn_point offset

Load NPCs into defined positions in tmx file

Item Types
    - determine how to implement item type heiarchy
    - gear will be upgraded (in terms of stats)
    - imlpement weapon types
    - coins and potions will be the only other item types
        * should still implement a dynamic item heiarchy so it can be easily changed

Implement a map page (and minimap?)

Implement Character Creation Page
    - Transition from main menu to character creation

Add Audio
    - Sound effects
    - Background Music

Implement Loading Screen
    - Display Percentage and Errors in loading

Implement Menus
    - Shop Menus
    - Inventory
    - Pause Menu

Implement Clothing (overlay other sprites ontop of character / relative to character position)

Implement Attack and Defend Sprite Motion

Character Size Transformation

Implement Window Resize (Possibly just static and predefined sizes in options menu)

Bugs
Need to clean up variables and images that are not used
Player class methods don't require reference to a world object ??? (only a surface to draw on?)
Updates are a little laggy --> need to speed up game loop