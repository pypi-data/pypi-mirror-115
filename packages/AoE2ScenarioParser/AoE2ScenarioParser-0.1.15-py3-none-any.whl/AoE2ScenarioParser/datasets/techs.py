from __future__ import annotations
from enum import Enum


class TechInfo(Enum):

    """

    This enum class provides information about most of the techs in the game. Information about the
    following properties of a tech is found in this class:
     - Tech ID
     - Icon ID

    **Methods**

    >>> TechInfo.from_id()
    >>> TechInfo.from_icon_id()
    >>> TechInfo.unique_techs()
    >>> TechInfo.unique_unit_upgrades()

    **Examples**

    >>> TechInfo.LOOM.ID
    >>> 22

    >>> TechInfo.LOOM.ICON_ID
    >>> 6

    """

    @property
    def ID(self):

        """

        Returns:
            The ID of the specified tech

        """

        return self.value[0]

    @classmethod
    def from_id(cls, tech_id: int) -> TechInfo:

        """

        Get the TechInfo object from its ID

        Args:
            tech_id: The ID of the tech to get the TechInfo of

        Returns:
            A TechInfo object of the specified tech ID

        """

        if tech_id < 0:
            raise ValueError(f"{tech_id} is not a valid tech id value")
        for x in cls._member_map_.values():
            if x.value[0] == tech_id:
                return x

        raise KeyError(f"A technology with ID '{tech_id}' was not found in the dataset")

    @property
    def ICON_ID(self):

        """

        Returns:
            The icon ID of the specified tech

        """

        return self.value[1]

    @classmethod
    def from_icon_id(cls, tech_icon_id):

        """

        Get the TechInfo object from its icon ID

        Args:
            tech_icon_id: The icon ID of the tech to get the TechInfo of

        Returns:
            A TechInfo object of the tech with the specified icon ID

        """

        if tech_icon_id == -1:
            raise ValueError("-1 is not a valid icon_id value")
        for x in cls._member_map_.values():
            if x.value[1] == tech_icon_id:
                return x

        raise KeyError(f"A technology with icon id '{tech_icon_id}' was not found in the dataset")

    @staticmethod
    def unique_techs(exclude_castle_techs: bool = True, exclude_imp_techs: bool = True) -> list[TechInfo]:

        """

        Get the list of all the unique techs in the game

        Args:
            exclude_castle_techs: if set to True, exclude the castle age techs
            exclude_imp_techs: if set to True, exclude the imperial age techs

        Returns:
            A list of TechInfo objects which are all the unique techs in the game

        """

        unique_techs = {
            "castle_age": [
                TechInfo.ANARCHY,
                TechInfo.ANDEAN_SLING,
                TechInfo.ATLATL,
                TechInfo.BEARDED_AXE,
                TechInfo.CARRACK,
                TechInfo.CHATRAS,
                TechInfo.CHIEFTAINS,
                TechInfo.CORVINIAN_ARMY,
                TechInfo.FIRST_CRUSADE,
                TechInfo.GREAT_WALL,
                TechInfo.GREEK_FIRE,
                TechInfo.HILL_FORTS,
                TechInfo.HOWDAH,
                TechInfo.HULCHE_JAVELINEERS,
                TechInfo.INQUISITION,
                TechInfo.IRONCLAD,
                TechInfo.KAMANDARAN,
                TechInfo.KASBAH,
                TechInfo.NOMADS,
                TechInfo.MADRASAH,
                TechInfo.MARAUDERS,
                TechInfo.ORTHODOXY,
                TechInfo.PANOKSEON,
                TechInfo.PAVISE,
                TechInfo.ROYAL_HEIRS,
                TechInfo.SHATAGNI,
                TechInfo.SILK_ARMOR,
                TechInfo.SIPAHI,
                TechInfo.STEPPE_HUSBANDRY,
                TechInfo.STIRRUPS,
                TechInfo.STRONGHOLD,
                TechInfo.SULTANS,
                TechInfo.THALASSOCRACY,
                TechInfo.TIGUI,
                TechInfo.TUSK_SWORDS,
                TechInfo.YASAMA,
                TechInfo.YEOMEN,
            ],
            "imp_age": [
                TechInfo.ARQUEBUS,
                TechInfo.ARTILLERY,
                TechInfo.ATHEISM,
                TechInfo.BAGAINS,
                TechInfo.BERSERKERGANG,
                TechInfo.BURGUNDIAN_VINEYARDS,
                TechInfo.CHIVALRY,
                TechInfo.CRENELLATIONS,
                TechInfo.COURIERS,
                TechInfo.CUMAN_MERCENARIES,
                TechInfo.DOUBLE_CROSSBOW,
                TechInfo.DRILL,
                TechInfo.DRUZHINA,
                TechInfo.EL_DORADO,
                TechInfo.FARIMBA,
                TechInfo.FLEMISH_REVOLUTION,
                TechInfo.FORCED_LEVY,
                TechInfo.FUROR_CELTICA,
                TechInfo.GARLAND_WARS,
                TechInfo.KATAPARUTO,
                TechInfo.LOGISTICA,
                TechInfo.MAGHRABI_CAMELS,
                TechInfo.MAHOUTS,
                TechInfo.MANIPUR_CAVALRY,
                TechInfo.PAPER_MONEY,
                TechInfo.PERFUSION,
                TechInfo.RECURVE_BOW,
                TechInfo.ROCKETRY,
                TechInfo.SCUTAGE,
                TechInfo.SHINKICHON,
                TechInfo.SILK_ROAD,
                TechInfo.SUPREMACY,
                TechInfo.TIMURID_SIEGECRAFT,
                TechInfo.TORSION_ENGINES,
                TechInfo.TOWER_SHIELDS,
                TechInfo.WARWOLF,
                TechInfo.ZEALOTRY
            ]
        }

        techs_to_return = []

        if not exclude_castle_techs:
            techs_to_return.extend(unique_techs["castle_age"])
        if not exclude_imp_techs:
            techs_to_return.extend(unique_techs["imp_age"])

        return techs_to_return

    @staticmethod
    def unique_unit_upgrades(
        exclude_castle_techs: bool = False,
        exclude_non_castle_techs: bool = False
    ) -> list[TechInfo]:

        """

        Args:
            exclude_castle_techs: if set to false, excludes the castle unique unit techs from the list of techs returned
            exclude_non_castle_techs: if set to false, excludes the non castle unique unit techs from the list of techs returned

        Returns:
            A list of unique unite upgrade tech IDs

        """

        args = locals()
        params = TechInfo.unique_unit_upgrades.__annotations__
        params.pop("return")
        for param, param_type in params.items():
            provided = type(args[param])
            if provided is not param_type:
                raise TypeError(f"Parameter '{param}' can only be of type {param_type} but provided type: {provided}")

        unique_techs = {
            "castle": [
                TechInfo.ELITE_ARAMBAI,
                TechInfo.ELITE_BALLISTA_ELEPHANT,
                TechInfo.ELITE_BERSERK,
                TechInfo.ELITE_BOYAR,
                TechInfo.ELITE_CAMEL_ARCHER,
                TechInfo.ELITE_CATAPHRACT,
                TechInfo.ELITE_CHU_KO_NU,
                TechInfo.ELITE_CONQUISTADOR,
                TechInfo.ELITE_COUSTILLIER,
                TechInfo.ELITE_ELEPHANT_ARCHER,
                TechInfo.ELITE_GBETO,
                TechInfo.ELITE_GENOESE_CROSSBOWMAN,
                TechInfo.ELITE_HUSKARL,
                TechInfo.ELITE_JAGUAR_WARRIOR,
                TechInfo.ELITE_JANISSARY,
                TechInfo.ELITE_KAMAYUK,
                TechInfo.ELITE_KARAMBIT_WARRIOR,
                TechInfo.ELITE_KESHIK,
                TechInfo.ELITE_KIPCHAK,
                TechInfo.ELITE_KONNIK,
                TechInfo.ELITE_LEITIS,
                TechInfo.ELITE_LONGBOWMAN,
                TechInfo.ELITE_MAGYAR_HUSZAR,
                TechInfo.ELITE_MAMELUKE,
                TechInfo.ELITE_MANGUDAI,
                TechInfo.ELITE_ORGAN_GUN,
                TechInfo.ELITE_PLUMED_ARCHER,
                TechInfo.ELITE_RATTAN_ARCHER,
                TechInfo.ELITE_SAMURAI,
                TechInfo.ELITE_SERJEANT,
                TechInfo.ELITE_SHOTEL_WARRIOR,
                TechInfo.ELITE_TARKAN,
                TechInfo.ELITE_TEUTONIC_KNIGHT,
                TechInfo.ELITE_THROWING_AXEMAN,
                TechInfo.ELITE_WAR_ELEPHANT,
                TechInfo.ELITE_WAR_WAGON,
                TechInfo.ELITE_WOAD_RAIDER
            ],
            "non_castle": [
                TechInfo.ELITE_CARAVEL,
                TechInfo.ELITE_GENITOUR,
                TechInfo.ELITE_LONGBOAT,
                TechInfo.ELITE_TURTLE_SHIP,
                TechInfo.IMPERIAL_CAMEL_RIDER,
                TechInfo.IMPERIAL_SKIRMISHER
            ]
        }

        techs_to_return = []

        if not exclude_castle_techs:
            techs_to_return.extend(unique_techs["castle"])
        if not exclude_non_castle_techs:
            techs_to_return.extend(unique_techs["non_castle"])

        return techs_to_return

    ANARCHY = 16, 33
    ANDEAN_SLING = 516, 33
    ARBALESTER = 237, 54
    ARCHITECTURE = 51, 14
    ARQUEBUS = 573, 107
    ARROWSLITS = 608, 119
    ARSON = 602, 118
    ARTILLERY = 10, 107
    ATHEISM = 21, 107
    ATLATL = 460, 33
    ATONEMENT = 319, 93
    AZTECS = 543, -1
    BAGAINS = 686, 107
    BALLISTICS = 93, 25
    BANKING = 17, 3
    BEARDED_AXE = 83, 107
    BERBERS = 583, -1
    BERSERKERGANG = 49, 107
    BLAST_FURNACE = 75, 21
    BLOCK_PRINTING = 230, 82
    BLOODLINES = 435, 110
    BODKIN_ARROW = 200, 35
    BOMBARD_CANNON = 188, -1
    BOMBARD_TOWER = 64, 47
    BOW_SAW = 203, 71
    BRACER = 201, 37
    BRITONS = 529, -1
    BULGARIANS = 673, -1
    BURMESE = 652, -1
    BYZANTINES = 535, -1
    CANNON_GALLEON = 37, 9
    CAPPED_RAM = 96, 27
    CARAVAN = 48, 113
    CAREENING = 374, 98
    CARRACK = 572, 33
    CARTOGRAPHY = 19, 4
    CASTLE_AGE = 102, 31
    CAVALIER = 209, 78
    CELTS = 541, -1
    CHAIN_BARDING_ARMOR = 82, 23
    CHAIN_MAIL_ARMOR = 76, 22
    CHAMPION = 264, 44
    CHATRAS = 628, 33
    CHEMISTRY = 47, 12
    CHINESE = 534, -1
    CHIVALRY = 493, 33
    COINAGE = 23, 7
    CONSCRIPTION = 315, 91
    CORVINIAN_ARMY = 514, 33
    COURIERS = 517, 107
    CRENELLATIONS = 11, 107
    CROP_ROTATION = 12, 0
    CROSSBOWMAN = 100, 29
    CHINESE_50_PERCENT_HP_DEMOS = 396, -1
    CUMAN_MERCENARIES = 690, 107
    CUMANS = 675, -1
    DARK_AGE = 104, -1
    DOUBLE_CROSSBOW = 623, 107
    FRANKS_FREE_FARMING_1 = 287, -1
    DOUBLE_BIT_AXE = 202, 70
    DRILL = 6, 107
    DRUZHINA = 513, 107
    DRY_DOCK = 375, 99
    EAGLE_WARRIOR = 384, 75
    EL_DORADO = 4, 107
    ELITE_ARAMBAI = 619, 105
    ELITE_BALLISTA_ELEPHANT = 615, 105
    ELITE_BATTLE_ELEPHANT = 631, 121
    ELITE_BERSERK = 398, 105
    ELITE_BOYAR = 504, 105
    ELITE_CAMEL_ARCHER = 565, 105
    ELITE_CANNON_GALLEON = 376, 100
    ELITE_CARAVEL = 597, 105
    ELITE_CATAPHRACT = 361, 105
    ELITE_COUSTILLIER = 751, 105
    ELITE_CHU_KO_NU = 362, 105
    ELITE_CONQUISTADOR = 60, 105
    ELITE_EAGLE_WARRIOR = 434, 115
    ELITE_ELEPHANT_ARCHER = 481, 105
    ELITE_GBETO = 567, 105
    ELITE_GENITOUR = 599, 105
    ELITE_GENOESE_CROSSBOWMAN = 468, 105
    ELITE_HUSKARL = 365, 105
    ELITE_JAGUAR_WARRIOR = 432, 105
    ELITE_JANISSARY = 369, 105
    ELITE_KAMAYUK = 509, 105
    ELITE_KARAMBIT_WARRIOR = 617, 105
    ELITE_KESHIK = 680, 105
    ELITE_KIPCHAK = 682, 105
    CHIEFTAINS = 463, 33
    ELITE_KONNIK = 678, 105
    ELITE_LEITIS = 684, 105
    ELITE_LONGBOAT = 372, 105
    ELITE_LONGBOWMAN = 360, 105
    ELITE_MAGYAR_HUSZAR = 472, 105
    ELITE_MAMELUKE = 368, 105
    ELITE_MANGUDAI = 371, 105
    ELITE_ORGAN_GUN = 563, 105
    ELITE_PLUMED_ARCHER = 27, 105
    ELITE_RATTAN_ARCHER = 621, 105
    ELITE_SAMURAI = 366, 105
    ELITE_SERJEANT = 753, 105
    ELITE_SHOTEL_WARRIOR = 569, 105
    ELITE_SKIRMISHER = 98, 28
    ELITE_STEPPE_LANCER = 715, 123
    ELITE_TARKAN = 2, 105
    ELITE_TEUTONIC_KNIGHT = 364, 105
    ELITE_THROWING_AXEMAN = 363, 105
    ELITE_TURTLE_SHIP = 448, 105
    ELITE_WAR_ELEPHANT = 367, 105
    ELITE_WAR_WAGON = 450, 105
    ELITE_WOAD_RAIDER = 370, 105
    ENABLE_COWS = 557, 94
    ENABLE_LLAMAS = 556, 94
    ENABLE_SHEEP = 555, 94
    ENABLE_TURKEYS = 558, 94
    ETHIOPIANS = 581, -1
    FAITH = 45, 11
    FARIMBA = 577, 107
    FAST_FIRE_SHIP = 246, 40
    FERVOR = 252, 73
    FEUDAL_AGE = 101, 30
    FIRE_TOWER = 527, -1
    FLETCHING = 199, 34
    FORCED_LEVY = 625, 107
    FORGING = 67, 17
    FORTIFIED_WALL = 194, 46
    FRANKS = 530, -1
    FREE_CARTOGRAPHY = 600, -1
    FUROR_CELTICA = 5, 107
    GALLEON = 35, 59
    GARLAND_WARS = 24, 107
    BONFIRE = 65, 41
    GOLD_MINING = 55, 15
    GOLD_SHAFT_MINING = 182, 62
    GOTHS = 531, -1
    GREAT_WALL = 462, 33
    GREEK_FIRE = 464, 33
    GUARD_TOWER = 140, 76
    GUILDS = 15, 58
    HALBERDIER = 429, 106
    HAND_CANNON = 85, -1
    HAND_CART = 249, 42
    HEATED_SHOT = 380, 104
    HEAVY_CAMEL_RIDER = 236, 55
    HEAVY_CAV_ARCHER = 218, 52
    HEAVY_DEMOLITION_SHIP = 244, 39
    HEAVY_PLOW = 13, 1
    HEAVY_SCORPION = 239, 38
    HERBAL_MEDICINE = 441, 114
    HERESY = 439, 108
    HILL_FORTS_2 = 394, -1
    HILL_FORTS = 691, 33
    HOARDINGS = 379, 103
    HORSE_COLLAR = 14, 2
    HOWDAH = 626, 33
    HUNS = 545, -1
    HUNTING_DOGS = 526, 94
    HUSBANDRY = 39, 10
    HUSSAR = 428, 122
    ILLUMINATION = 233, 84
    IMPERIAL_AGE = 103, 32
    IMPERIAL_CAMEL_RIDER = 521, 74
    IMPERIAL_SKIRMISHER = 655, 120
    INCAS = 549, -1
    INDIANS = 548, -1
    INQUISITION = 492, 33
    IRON_CASTING = 68, 18
    IRONCLAD = 489, 33
    ITALIANS = 547, -1
    JAPANESE = 533, -1
    KAMANDARAN = 488, 33
    KASBAH = 578, 33
    KATAPARUTO = 59, 107
    KEEP = 63, 16
    KHMER = 650, -1
    KOREANS = 546, -1
    LEATHER_ARCHER_ARMOR = 212, 50
    LIGHT_CAVALRY = 254, 43
    LITHUANIANS = 676, -1
    LOGISTICA = 61, 107
    LONG_SWORDSMAN = 207, 48
    LOOM = 22, 6
    MADRASAH = 490, 33
    MAGHRABI_CAMELS = 579, 107
    MAGYARS = 550, -1
    MAHOUTS = 7, 107
    MALAY = 651, -1
    MALIANS = 582, -1
    MAN_AT_ARMS = 222, 85
    MANIPUR_CAVALRY = 627, 107
    MARAUDERS = 483, 33
    MASONRY = 50, 13
    MAYANS = 544, -1
    MONGOLS = 540, -1
    MURDER_HOLES = 322, 61
    NOMADS = 487, 33
    HULCHE_JAVELINEERS = 485, 33
    ONAGER = 257, 57
    ORTHODOXY = 512, 33
    PADDED_ARCHER_ARMOR = 211, 49
    PALADIN = 265, 45
    PANOKSEON = 486, 33
    PAPER_MONEY = 629, 107
    PARTHIAN_TACTICS = 436, 111
    PAVISE = 494, 33
    PERFUSION = 457, 107
    PERSIANS = 536, -1
    PIKEMAN = 197, 36
    PLATE_BARDING_ARMOR = 80, 65
    PLATE_MAIL_ARMOR = 77, 64
    PORTUGUESE = 580, -1
    RECURVE_BOW = 515, 107
    REDEMPTION = 316, 92
    REVETMENTS = 525, -1
    RING_ARCHER_ARMOR = 219, 51
    ROCKETRY = 52, 107
    ROYAL_HEIRS = 574, 33
    SANCTITY = 231, 83
    SAPPERS = 321, 5
    SARACENS = 537, -1
    SCALE_BARDING_ARMOR = 81, 66
    SCALE_MAIL_ARMOR = 74, 63
    SCORPION = 94, -1
    SET_MAXIMUM_POPULATION_NO_HOUSES = 658, -1
    SHATAGNI = 507, 107
    SHINKICHON = 445, 107
    SHIPWRIGHT = 373, 97
    SIEGE_ENGINEERS = 377, 101
    SIEGE_ONAGER = 320, 96
    SIEGE_RAM = 255, 86
    SILK_ARMOR = 687, 33
    SILK_ROAD = 499, 107
    SIPAHI = 491, 33
    SLAVS = 551, -1
    SPANISH = 542, -1
    SPIES_AND_TREASON = 408, 19
    SQUIRES = 215, 80
    STEPPE_HUSBANDRY = 689, 33
    STIRRUPS = 685, 33
    STONE_MINING = 278, 87
    STONE_SHAFT_MINING = 279, 88
    STRONGHOLD = 482, 33
    SULTANS = 506, 33
    SUPPLIES = 716, 124
    SUPREMACY = 440, 107
    TATARS = 674, -1
    TEUTONS = 532, -1
    THALASSOCRACY = 624, 33
    THEOCRACY = 438, 109
    THUMB_RING = 437, 112
    TIGUI = 576, 33
    TIMURID_SIEGECRAFT = 688, 107
    TORSION_ENGINES = 575, 107
    TOWER_SHIELDS = 692, 107
    TOWN_CENTER_SPAWN = 639, -1
    TOWN_PATROL = 280, 89
    TOWN_WATCH = 8, 69
    TRACKING = 90, 67
    TREADMILL_CRANE = 54, 60
    TURKS = 538, -1
    TUSK_SWORDS = 622, 33
    TWO_HANDED_SWORDSMAN = 217, 53
    TWO_MAN_SAW = 221, 81
    VIETNAMESE = 653, -1
    VIETNAMESE_VISION = 665, -1
    VIKINGS = 539, -1
    WAR_GALLEY = 34, 8
    WARWOLF = 461, 107
    WHEELBARROW = 213, 79
    YASAMA = 484, 33
    YEOMEN = 3, 33
    ZEALOTRY = 9, 107
    SICILIANS = 749, -1
    BURGUNDIANS = 748, -1
    BURGUNDIAN_VINEYARDS = 754, 33
    FLEMISH_REVOLUTION = 755, 107
    FIRST_CRUSADE = 756, 33
    SCUTAGE = 757, 107
    CONVERSION_ENABLER = 243, -1
