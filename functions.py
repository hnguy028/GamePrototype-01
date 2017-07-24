from includes import *
from constants import *

# load map subsection defined by the portal location
def checkPortal(player, room, world):
    # TODO : need to check if a portal exists in the first place (currently assuming that there is a portal on each map)
    # TODO : should work anyways, the for loop should handle null (need to test)
    portals = world.gameMap.get_layer_by_name("portals")

    for portal in portals:
        # check if player is within the bounds of the portal
        if (((player.x + (room.xRoom * world.widthPixels)) >= portal.x)
                and ((player.y + (room.yRoom * world.heightPixels)) >= portal.y)
                and ((player.x + (room.xRoom * world.widthPixels)) <= (portal.x + portal.width))
                and ((player.y + (room.yRoom * world.heightPixels)) <= (portal.y + portal.height))):

            world.gameMap = load_pygame('TileGameResources\\' + portal.worldName + '.tmx')

            world.playerSpawn = world.gameMap.get_object_by_name("SpawnPoint")

            room.xRoom = int(world.playerSpawn.x // world.widthPixels)
            room.yRoom = int(world.playerSpawn.y // world.heightPixels)

            player.x = world.playerSpawn.x % world.widthPixels
            player.y = world.playerSpawn.y % world.heightPixels

            # reload tmx of new world
            world.loadMap(room)

            # draw new world
            world.drawMap(TILESIZE, ROOMWIDTH, ROOMHEIGHT)
