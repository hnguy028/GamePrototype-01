from includes import *

# TODO : move function into Room class
# load map subsection defined by the portal location
def checkPortal(player, room, world):
    portals = room.gameMap.get_layer_by_name("portals")

    # if portal == None?
    for portal in portals:
        # check if player is within the bounds of the portal
        if (((player.x + (room.xRoom * room.pixelWidth)) >= portal.x)
                and ((player.y + (room.yRoom * room.pixelHeight)) >= portal.y)
                and ((player.x + (room.xRoom * room.pixelWidth)) <= (portal.x + portal.width))
                and ((player.y + (room.yRoom * room.pixelHeight)) <= (portal.y + portal.height))):

            print(portal.worldName)
            room.changeMap(portal.worldName)


            player.x = room.playerSpawn.x % room.pixelWidth
            player.y = room.playerSpawn.y % room.pixelHeight

            # draw new world
            room.drawMap(world.surface)

#######################################################################################################################
#                                          Global Functions
#######################################################################################################################

# sureface, image, (x,y), alpha
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

# calculates resizing of rectangle, while keeping aspect ratio
def scale_aspect(width, height, x, y, maximum=True):
    new_width = y * width / height
    new_height = x * height / width
    if maximum ^ (new_width >= x):
        return new_width or 1, y
    return x, new_height or 1