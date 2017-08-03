#######################################################################################################################
#                                          Item Types
#######################################################################################################################
class ItemDirectory:

    Currency = ""
    Item = ""
    Magic = ""

    class Potions:
        small_health = "health_small"
        medium_health = "health_medium"
        large_health = "health_large"

    class Weapons:
        sword = "sword"

class ItemTypes:
    potion = "potion"


Currency_Gold = "Gold"
Currency_Silver = "Silver"
Currency_Copper = "Copper"

CurrencyTypes = [Currency_Gold, Currency_Silver, Currency_Copper]