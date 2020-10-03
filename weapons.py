
sample = {
    'atk': 1,
    'crit': 1,
    'def': 0.4,
    'dual': False,
    'ev': 0.05,
    'g_type': 'sword',
    'lore': '''A sword made of sturdy iron,
        intended for short range combat.
        No knight should travel without one of these.''',
    'name': 'Iron Sword',
    'price': 0,
    'spe': 0.5,
    'type': 'sword'
}

weapons = {
    "200":{
        'name': 'Worker Hammer',
        'atk': 1.15,
        'crit': 1.4,
        'def': 0.5,
        'dual': False,
        'ev': 0.05,
        'g_type': 'hammer',
        'lore': str("Hammer of a worker, forged for the ironworks, can easely mould iron and steel. "
            +"Not intended for combat, but can easely break a common armor."
            +"\n\nWorkers of the heavy industry made possible the fast growth of their country, socially and"
            +"economically... One wonders, what could have possibly gone wrong in their society?"),
        'price': 0,
        'spe': 0.5,
        'type': 'hammer'
    },
    "201":{
        'name': 'Peasant Sickle',
        'atk': 1.0,
        'crit': 1.4,
        'def': 0.6,
        'dual': False,
        'ev': 0.05,
        'g_type': "dagger",
        'lore': str("Iron sickle intended for harvesting, not for the battle. "
            +"\n\nPeasants would work all day long under the harsh sunlight, to keep the food reserves full,"
            +" for the commonwealth."
            ),
        'price': 0,
        'spe': 0.8,
        'type': 'sickle'
    },
    "03":{
        'name': 'Silver Sword',
        'atk': 1.1,
        'crit': 1.45,
        'def': 0.4,
        'dual': False,
        'ev': 0.05,
        'g_type': "sword",
        'lore': str("Light and long silver plated sword, special for werewolf hunting.\n\nOn the ol' days, people at villages were often "
            +"aghast by werewolves, and because of that, hunters started plating their swords on silver, so they could kill them with ease."
            +"\nThis sword is a relic from those times, but is still suitable for short distance combat."),
        'price': 50,
        'spe': 0.65,
        'type': 'sword'
    },
    "04":{
        'name': 'Doppelhänder',
        'atk': 1.6,
        'crit': 1.4,
        'def': 0.7,
        'dual': True,
        'ev': 0.04,
        'g_type': "sword",
        'lore': str("An extremely large and heavy sword which requires both hands to be handled, most commonly used on ceremonies than combat due to it's tremendous weight."
            +"\n\nBeing the hallmark weapon for mercenaries long before, the Doppelhänder became famous due to it's extreme power, useful for breaking enemies bones and throwing them through the air, rather "
            +"than slicing them in half. But it eventually stopped being used due it's lack of practicality on the battlefield."),
        'price': 150,
        'spe': 0.2,
        'type': 'greatsword'
    },
    "05":{
        'name': 'Cutlass',
        'atk': 0.8,
        'crit': 1.8,
        'def': 0.3,
        'dual': False,
        'ev': 0.1,
        'g_type': "sword",
        'lore': str("A short curved sword, popular among pirates."
            +"\n\nA pirate would never leave harbor without one of these, for a Cutlass is always their best friend. Not a very strong weapon, "
            +"but due ti its light weight and shape, lets the user to connect many hits one after another, causing lots of damage on the foe in little time... "
            +"If the user has good dexterity, of course."),
        'price': 50,
        'spe': 1,
        'type': 'curved sword'
    },
    "39":{
        'name': 'Katana',
        'atk': 1.2,
        'crit': 1.5,
        'def': 0.4,
        'dual': True,
        'ev': 0.1,
        'g_type': "sword",
        'lore': str("Unique Katana, lightweight and a long curved single-edged blade, crafted with a peculiar yet refined technique. Must be held with both hands."
            +"\n\nThe finely-sharpened blade of a katana slices with unmistakable smoothness, but should be wielded with caution, as its delicate constitution means it's easily worn."),
        'price': 80,
        'spe': 1,
        'type': 'katana'
    },
    "06":{
        'name': "Bandit's Knife",
        'atk': 0.6,
        'crit': 1.7,
        'def': 0.05,
        'dual': False,
        'ev': 0.03,
        'g_type': "dagger",
        'lore': str("This wide single-edged shortsword is the favorite of lowly thieves and bandits."
            +"Primarily a slicing weapon, but highly effective when used for critical hits"),
        'price': 50,
        'spe': 0.6,
        'type': ''
    },
    "07":{
        'name': 'Parrying Dagger',
        'atk': 0.25,
        'crit': 2.5,
        'def': 0,
        'dual': False,
        'ev': 0,
        'g_type': "dagger",
        'lore': str("Dagger intended more for defense than attack. A counterattack with this dagger in perfect timing, lets the user stop attacks and "
            +"gives the opportunity to riposte with their main hand weapon. Otherwise, if the attack is not stopped, the user will remain vulnerable to their foe."),
        'price': 80,
        'spe': 1,
        'type': 'parrying dagger'
    },
    "08":{
        'name': "Dragon Claw",
        'atk': 1,
        'crit': 1.45,
        'def': 0.2,
        'dual': False,
        'ev': 0.02,
        'g_type': "dagger",
        'lore': str("Sharp curved dagger, one of the rare dragon weapons, was created from an everlasting dragon claw."
            +"\n\nDuring the Age of Ancients, the Dragons were the everlasting rulers of the world until the Lords rose and challenged them. "
            +"In the end, the Dragons were nearly driven to extinction, beginning a new era known as the Age of Fire"),
        'price': 100,
        'spe': 1,
        'type': 'karambit'
    },
    "09":{
        'name': 'Silver Axe',
        'atk': 1.20,
        'crit': 1.4,
        'def': 0.1,
        'dual': False,
        'ev': 0.01,
        'g_type': "axe",
        'lore': str("Silver plated hand axe, light weighted and does a respectable amount of damage."
            +"\n\nNot only the guards of the villages had to be aware of werewolves, but also lumberjacks, "
            +"who worked all day long in the woods, had to take action on the constant attacks of those damned beasts. "
            +"This tool is proof of those actions that were taken in this regard."),
        'price': 75,
        'spe': 0.3,
        'type': ''
    },
    "10":{
        'name': 'Executioner Greataxe',
        'atk': 1.70,
        'crit': 1.4,
        'def': 0.2,
        'dual': True,
        'ev': 0.001,
        'g_type': "axe",
        'lore': str("With a huge mass on its head, and a sharp edge by only one side, this axe is definitely not inteded for combat, but surely can deal a huge amount of damage."
            +"\n\nSometimes, when a crime is unforgivable, the punishment is death. And for this matters, the sharp edge and great weight of this axe can provide a clean and fast beheading."),
        'price': 150,
        'spe': 0.15,
        'type': 'greataxe'
    },
    "11":{
        'name': 'Battle Axe',
        'atk': 1.15,
        'crit': 1.4,
        'def': 0.4,
        'dual': False,
        'ev': 0.04,
        'g_type': "axe",
        'lore': str("Standard battle axe. Inflicts regular damage, making it effective in various situations. "
            +"Powerful attack due to its weight, but one wrong swing leaves the wielder wide open, so timing and proximity to the enemy must be judged carefully."),
        'price': 100,
        'spe': 0.6,
        'type': 'axe'
    },
    "12":{
        'name': 'Royal Halberd',
        'atk': 1.1,
        'crit': 1.45,
        'def': 0.7,
        'dual': True,
        'ev': 0.1,
        'g_type': "polearm",
        'lore': str("Long-hilted weapon mixing spear and axe is difficult to handle, requiring both strength and dexterity. Designed for the royal guard of a diistant kingdom. "
            +"The Halberd has two elementary attacks: Spear-like thrusting and large sweeping swings. However, one false swing and the wielder is left wide open."),
        'price': 100,
        'spe': 0.5,
        'type': 'halberd'
    },
    "13":{
        'name': 'Grand Lance',
        'atk': 1.5,
        'crit': 1.45,
        'def': 0.2,
        'dual': True,
        'ev': 0.03,
        'g_type': "polearm",
        'lore': str("It is customary to use in jousting, allowing the knight to rely on the strength of his horse to score accurate blows. However, a man of sufficient strength could make good use of this weapon, even on foot."),
        'price': 160,
        'spe': 0.15,
        'type': 'lance'
    },
    "14":{
        'name': 'Hunting Spear',
        'atk': 0.8,
        'crit': 2,
        'def': 0.4,
        'dual': False,
        'ev': 0.7,
        'g_type': "polearm",
        'lore': str("Primitive weapon, mainly used for hunting by the ancient nomads. Despite its simple aspect,"
            +" it could take over a sabertooth in just one accurate blow."),
        'price': 100,
        'spe': 0.7,
        'type': 'spear'
    },
    "15":{
        'name': 'Headhunter',
        'atk': 1.15,
        'crit': 1.65,
        'def': 0.6,
        'dual': True,
        'ev': 0.1,
        'g_type': "polearm",
        'lore': str(""),
        'price': 130,
        'spe': 0.9,
        'type': 'scythe'
    },
    "16":{
        'name': 'Frying Pan',
        'atk': 0.4,
        'crit': 1.1,
        'def': 0.8,
        'dual': False,
        'ev': 0.05,
        'g_type': "hammer",
        'lore': str("Intended as cookware, not as a weapon for combat."
            +" However, it provides decent protection against many weapons,"
            +" due to the sturdy material it is made of. \n\nAlso, it has been proven"
            +" to be quite effective for killing the undead." ),
        'price': 20,
        'spe': 0.5,
        'type': 'Cookware'
    },
    "17":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "hammer",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "18":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "hammer",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "19":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "whip",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "20":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "whip",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "21":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "whip",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "22":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "ranged",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "23":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "ranged",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "24":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "ranged",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "25":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "magic",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "26":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "magic",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "27":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "magic",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "28":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "shield",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "29":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "shield",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
    "30":{
        'name': '',
        'atk': 1,
        'crit': 1,
        'def': 1,
        'dual': False,
        'ev': 1,
        'g_type': "shield",
        'lore': str(""),
        'price': 0,
        'spe': 1,
        'type': ''
    },
}
