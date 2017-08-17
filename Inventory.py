from Inventory_Equipment import *
from Inventory_Backpack import *
from Inventory_Wallet import *
from Controls import *
from resource_loader import *

class Inventory:

    def __init__(self, frame_surface):
        self.frame = frame_surface

        # padding between each slot
        self.slotPadding = 10

        # padding between frame and item grids
        self.gridtoframe_padding = 20

        # inventory surfaces
        self.surface = pygame.Surface((FRAMEPIXELWIDTH, FRAMEPIXELHEIGHT))
        self.surface.set_alpha(MAX_ALPHA)

        # Tab configurations
        self.tabs_width = (FRAMEPIXELWIDTH - (4 * self.gridtoframe_padding)) // 3
        self.tabs_height = 30

        self.tabs_surface = pygame.Surface((FRAMEPIXELWIDTH - self.gridtoframe_padding, self.tabs_height + 2))

        tab_padding = (self.tabs_surface.get_width() - 3 * self.tabs_width) // 4

        self.tab_images = [Sprite(imageLibrary.load(imageDirectory.blankButton, self.tabs_width, self.tabs_height),
                                  (tab_padding, 0)),
                           Sprite(imageLibrary.load(imageDirectory.blankButton, self.tabs_width, self.tabs_height),
                                  (self.tabs_width + 2 * tab_padding, 0)),
                           Sprite(imageLibrary.load(imageDirectory.blankButton, self.tabs_width, self.tabs_height),
                                  (2 * self.tabs_width + 3 * tab_padding, 0))]


        # icon size configurations
        self.icon_width = (FRAMEPIXELWIDTH - ( DEFAULT_INV_GRID_WIDTH + 1) * self.slotPadding - self.gridtoframe_padding) // DEFAULT_INV_GRID_WIDTH
        self.icon_height = self.icon_width
        self.slot_icon = imageLibrary.load(imageDirectory.slotIcon, self.icon_width, self.icon_height)

        # backpack
        self.backpack = InventoryBackpack(FRAMEPIXELWIDTH - self.gridtoframe_padding,
                                          self.slot_icon, self.icon_width, self.icon_height, self.slotPadding,
                                          (self.gridtoframe_padding // 2, self.gridtoframe_padding // 2 + self.tabs_surface.get_height()))

        # initialize and load equipment
        self.equipment = InventoryEquipment(FRAMEPIXELWIDTH - self.gridtoframe_padding, self.icon_height*2 + self.slotPadding*3 ,
                                   self.slot_icon, self.icon_width, self.icon_height, self.slotPadding,
                                            (self.gridtoframe_padding // 2, FRAMEPIXELHEIGHT - (
                                            self.icon_height * 2 + self.slotPadding * 3 + self.gridtoframe_padding)))

        self.wallet = InventoryWallet(FRAMEPIXELWIDTH - self.gridtoframe_padding, 300,
                                      (self.gridtoframe_padding // 2, self.gridtoframe_padding // 2))

        # reference to the selected slot, to either move, equip, or swap
        self.selectedSlot = None

        # cursor position
        self.cursor_x = 0
        self.cursor_y = 0
        self.hoverSlot = None


        tab_panels = [InventoryPanel.OVERVIEW_TAB, InventoryPanel.ITEMS_TAB, InventoryPanel.MAGIC_TAB]
        self.inventory_panels = [[tab_panels, [InventoryPanel.PANEL01]],
                                 [tab_panels, [InventoryPanel.PANEL01], [InventoryPanel.PANEL02]],
                                 [tab_panels, [InventoryPanel.PANEL01]]]

        self.current_tab = InventoryTabs.ITEMS
        self.panel_focused = False

        # load images
        self.load()

    # load in inventory images
    def load(self):
        self.background_image = Sprite(
            imageLibrary.staticLoad(imageDirectory.inventoryFrame,
                              FRAMEPIXELWIDTH,
                              FRAMEPIXELHEIGHT))

        self.inventory_cursor = Sprite(imageLibrary.load(imageDirectory.inventory_cursor, 20, 20))

    def draw(self):
        # draw inventory surface to frame
        self.frame.blit(self.surface, (0, 0))

        # draw background image to inventory surface
        self.background_image.draw(self.surface)

        # draw tab surface to inventory surface
        self.frame.blit(self.tabs_surface, (self.gridtoframe_padding // 2, self.gridtoframe_padding // 2))

        # draw tabs surface background
        self.tabs_surface.fill((144, 144, 144))

        # draw the inventory tabs
        for tab in self.tab_images:
            tab.draw(self.tabs_surface)


        # draw the respective panels
        if self.current_tab == InventoryTabs.OVERVIEW:
            # draw contents of wallet
            self.wallet.draw(self.surface)

            # draw inventory capacities

            # draw equiped items and powers

        elif self.current_tab == InventoryTabs.ITEMS:
            # draw inventory grid to inventory surface
            self.backpack.draw(self.surface)

            # draw equipment
            self.equipment.draw(self.surface)
        elif self.current_tab == InventoryTabs.MAGIC:
            None

        # draw the panel or tab currently selected
        # if focused then dont draw the selected option

    def handleEvent(self, event):
        if self.panel_focused:
            if event.key == C_UP:
                self.moveCursor(0, -1)
            elif event.key == C_DOWN:
                self.moveCursor(0, 1)
            elif event.key == C_LEFT:
                self.moveCursor(-1, 0)
            elif event.key == C_RIGHT:
                self.moveCursor(1, 0)
            elif event.key == K_x:
                self.selectSlot()
            elif event.key == K_j:
                # equip
                if self.selectedSlot:

                    if self.current_tab == InventoryTabs.OVERVIEW:
                        pass
                    elif self.current_tab == InventoryTabs.ITEMS:
                        if self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL01:
                            # inventory

                            # check if the equiped item is not in inventory, and if we can add it to inventory
                            if not self.equipment.equipmentMap[self.selectedSlot.item.type].isEmpty:
                                if not self.backpack.can_add(self.equipment.equipmentMap[self.selectedSlot.item.type].item):
                                    return

                            rtn_item, rtn_amount = self.equipment.equip(self.selectedSlot.item)
                            self.backpack.remove(item=self.selectedSlot.item)
                            self.backpack.releaseSelect()
                            self.selectedSlot = None

                            if rtn_item:
                                self.backpack.add(rtn_item, rtn_amount)

                        elif self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL02:
                            # equipment
                            if self.backpack.can_add(self.selectedSlot.item):
                                rtn_item, rtn_amount = self.equipment.unequip()
                                self.backpack.add(rtn_item, rtn_amount)
                                self.selectedSlot = None
                    elif self.current_tab == InventoryTabs.MAGIC:
                        # handles equiping and unequiping spells
                        pass

            elif event.key == C_ESCAPE:
                self.panel_focused = False
                if self.current_tab == InventoryTabs.OVERVIEW:
                    self.wallet.unfocus()
                elif self.current_tab == InventoryTabs.ITEMS:
                    self.backpack.unfocus()
                    self.equipment.unfocus()
                elif self.current_tab == InventoryTabs.MAGIC:
                    None
        else:
            self.navigateInventory(event)

    def navigateInventory(self, event):
        if not self.panel_focused:
            if event.key == C_UP:
                self.cursor_y = max(0, self.cursor_y - 1)
                self.cursor_x = max(0, min(self.cursor_x, len(self.inventory_panels[self.current_tab][self.cursor_y]) - 1))
            elif event.key == C_DOWN:
                self.cursor_y = min(len(self.inventory_panels) - 1, self.cursor_y + 1)
                self.cursor_x = max(0, min(self.cursor_x, len(self.inventory_panels[self.current_tab][self.cursor_y]) - 1))
            elif event.key == C_LEFT:
                self.cursor_x = max(0, self.cursor_x - 1)
            elif event.key == C_RIGHT:
                self.cursor_x = min(len(self.inventory_panels[self.current_tab][self.cursor_y]) - 1, self.cursor_x + 1)
            elif event.key == K_x:
                if self.cursor_y == 0:
                    # TODO : implement better ? (self.cursor xy should be set to panels if they exist)
                    self.current_tab = self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x]
                    self.cursor_x, self.cursor_y = 0, 1 if len(self.inventory_panels[self.current_tab]) >= 2 else 0
                else:
                    self.panel_focused = True
                    if self.current_tab == InventoryTabs.OVERVIEW:
                        # TODO
                        self.panel_focused = False
                        None
                    elif self.current_tab == InventoryTabs.ITEMS:
                        if self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL01:
                            self.backpack.isFocused = self.panel_focused
                        elif self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL02:
                            self.equipment.isFocused = self.panel_focused
                    elif self.current_tab == InventoryTabs.MAGIC:
                        None
            elif event.key == C_ESCAPE:
                None

    def moveCursor(self, left=0, down=0):
        if self.panel_focused:
            if self.current_tab == InventoryTabs.OVERVIEW:
                None
            elif self.current_tab == InventoryTabs.ITEMS:
                if self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL01:
                    self.backpack.moveCursor(left, down)
                elif self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL02:
                    self.equipment.moveCursor(left, down)
            elif self.current_tab == InventoryTabs.MAGIC:
                None

    def changeTabs(self, tab):
        self.current_tab = tab

    def increaseBackpack(self, amount):
        self.backpack.increaseCapacity()

    def selectSlot(self):
        # check which panel, and tab we are in
        if self.current_tab == InventoryTabs.OVERVIEW:
            pass
        elif self.current_tab == InventoryTabs.ITEMS:
            if self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL01:
                # inventory
                self.selectedSlot = self.backpack.selectSlot()
            elif self.inventory_panels[self.current_tab][self.cursor_y][self.cursor_x] == InventoryPanel.PANEL02:
                # equipment
                self.selectedSlot = self.equipment.hoverSlot
        elif self.current_tab == InventoryTabs.MAGIC:
            pass

    # add item to backpack
    def add(self, item, type, amount=1):
        return self.backpack.add(item)

    # TODO : remove from backpack or equipment???
    def remove(self, itemName=None, item=None, amount=1):
        return self.backpack.remove(itemName, item, amount)

    def removeSelected(self, amount=1):
        if not self.selectedSlot.isEmpty:
            if self.selectedSlot.remove(amount):
                del self.itemMap[self.selectedSlot.item.name]

    # Getter methods mainly for the hud to get equiped items
    def getEquiped(self):
        return self.equipment.equipmentMap["left_hand"]

class InventoryTabs:
    size = 3
    OVERVIEW, ITEMS, MAGIC = range(size)

class InventoryPanel:
    OVERVIEW_TAB, ITEMS_TAB, MAGIC_TAB, PANEL01, PANEL02, PANEL03 = range(6)