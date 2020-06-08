from ast import literal_eval as l_eval

def nameFormat(classes,castles,from_user):
    pl_name = from_user.first_name
    for clas in classes:
        if("first_name" in l_eval(str(from_user))):
            if(clas in from_user.first_name):
                pl_name = pl_name.replace(clas,"")
                pl_name += " {}".format(classes[clas])
        if("last_name" in l_eval(str(from_user))):
            if(clas in from_user.last_name):
                pl_name += " {}".format(classes[clas])

    for castle in castles:
        if("first_name" in l_eval(str(from_user))):
            if(from_user.first_name != None):
                if(castle in from_user.first_name):
                    pl_name = pl_name.replace(castle,"")
                    pl_name += " {}".format(castles[castle])
        if("last_name" in l_eval(str(from_user))):
            if(from_user.last_name != None):
                if(castle in from_user.last_name):
                    pl_name += " {}".format(castles[castle])
    try:
        pl_name = pl_name.replace("  "," ")
    except KeyError as e:
        #logger.error(e);raise
        print(str(e))

    return pl_name

sign =    {
                    "a":"atk",
                    "d":"def",
                    "h":"Head",
                    "b":"Body",
                    "f":"Feet"
                }
counter = 0

i_codes =    {
                "thread":"01",
                "stick":"02",
                "pelt":"03",
                "bone":"04",
                "coal":"05",
                "charcoal":"06",
                "powder":"07",
                "iron ore":"08",
                "cloth":"09",
                "silver ore":"10",
                "bauxite":"11",
                "cord":"12",
                "magic stone":"13",
                "wooden shaft":"14",
                "sapphire":"15",
                "solvent":"16",
                "ruby":"17",
                "hardener":"18",
                "steel":"19",
                "leather":"20",
                "bone powder":"21",
                "string":"22",
                "coke":"23",
                "purified powder":"24",
                "silver alloy":"25",
                "steel mold":"27",
                "silver mold":"28",
                "blacksmith frame":"29",
                "artisan frame":"30",
                "rope":"31",
                "silver frame":"32",
                "metal plate":"33",
                "metallic fiber":"34",
                "crafted leather":"35",
                "resurrection mix":"36",
            }

"""    "39" Stinky Sumac
"40" Mercy Sassafras
"41" Cliff Rue
"42" Love Creeper
"43" Wolf Root
"44" Swamp Lavender
"45" White Blossom
"46" Ilaves
"47" Ephijora
"48" Storm Hyssop
"49" Cave Garlic
"50" Yellow Seed
"51" Tecceagrass
"52" Spring Bay Leaf
"53" Ash Rosemary
"54" Sanguine Parsley
"55" Sun Tarragon
"56" Maccunut
"57" Dragon Seed
"58" Queen's Pepper
"59" Plasma of abyss
"60" Ultramarine dust
"61" Ethereal bone
"62" Itacory
"63" Assassin Vine
"64" Kloliarway
"65" Astrulic
"66" Flammia Nut
"67" Plexisop
"68" Mammoth Dill
"69" Silver dust
"501" Wrapping
"502" Leash
"504" Wooden arrow
"505" Wooden arrows pack
"506" Bottle of Remedy
"507" Remedy pack
"508" Bottle of Poison
"509" Poison pack
"511" Steel arrows pack
"513" Silver arrows pack
"614" 🎟Gift Coupon 'Pig'
"615" 🎟Gift Coupon 'Horse'
"616" 🎟Gift Coupon 'Owl'
"617" 🎟Gift Coupon 'Mouse'
"618" Hay
"619" Corn
"620" Hamsters
"621" Cheese
"622" 🎟Gift Coupon 'Gopher'
"623" 🎟Gift Coupon 'Ants'
"624" 🎟Gift Coupon 'Spider'
"625" 🎟Gift Coupon 'Haunted'
"626" 🎟Gift Coupon 'Camel'
"ch2" Ancient Chest
"est" 👹Evil Spirits Totem
"p01" Vial of Rage
"p02" Potion of Rage
"p03" Bottle of Rage
"p04" Vial of Peace
"p05" Potion of Peace
"p06" Bottle of Peace
"p07" Vial of Greed
"p08" Potion of Greed
"p09" Bottle of Greed
"p10" Vial of Nature
"p11" Potion of Nature
"p12" Bottle of Nature
"p13" Vial of Mana
"p14" Potion of Mana
"p15" Bottle of Mana
"p16" Vial of Twilight
"p17" Potion of Twilight
"p18" Bottle of Twilight
"p19" Vial of Morph
"p20" Potion of Morph
"p21" Bottle of Morph
"pap" Accuracy Pill
"pgs" Garlic Stew
"phw" Holy Water
"pl1" Vial of Оblivion
"pmp" Monster Pheromones
"psb" Silver Blood
"pvd" Vial of Defiance
"s01" 📕Scroll of Rage
"s02" 📕Scroll of Peace
"s03" 📗Scroll of Rage
"s04" 📗Scroll of Peace
"s05" 📘Scroll of Rage
"s06" 📘Scroll of Peace
"s11" 📕Rare scroll of Rage
"s12" 📕Rare scroll of Peace
"s13" 📗Rare scroll of Rage
"s14" 📗Rare scroll of Peace
"s15" 📘Rare scroll of Rage
"s16" 📘Rare scroll of Peace
"a01" Cloth jacket
"a02" Leather shirt
"a03" Chain mail
"a05" Mithril armor
"a06" Hat
"a07" Leather hood
"a08" Steel helmet
"a09" Silver helmet
"a10" Mithril helmet
"a11" Sandals
"a12" Leather shoes
"a13" Steel boots
"a14" Silver boots
"a15" Mithril boots
"a16" Gloves
"a17" Leather gloves
"a18" Steel gauntlets
"a19" Silver gauntlets
"a20" Mithril gauntlets
"a21" Wooden shield
"a22" Skeleton Buckler
"a23" Bronze shield
"a24" Silver shield
"a25" Mithril shield
"a26" Royal Guard Cape
"a27" Order Armor
"a28" Order Helmet
"a29" Order Boots
"a30" Order Gauntlets
"a31" Order Shield
"a32" Hunter Armor
"a33" Hunter Helmet
"a34" Hunter Boots
"a35" Hunter Gloves
"a36" Clarity Robe
"a37" Clarity Circlet
"a38" Clarity Shoes
"a39" Clarity Bracers
"a41" Bard's Cape
"a45" Crusader Armor
"a46" Crusader Helmet
"a47" Crusader Boots
"a48" Crusader Gauntlets
"a49" Crusader Shield
"a50" Royal Armor
"a51" Royal Helmet
"a52" Royal Boots
"a53" Royal Gauntlets
"a54" Royal Shield
"a55" Ghost Armor
"a56" Ghost Helmet
"a57" Ghost Boots
"a58" Ghost Gloves
"a59" Lion Armor
"a60" Lion Helmet
"a61" Lion Boots
"a62" Lion Gloves
"a63" Demon Robe
"a64" Demon Circlet
"a65" Demon Shoes
"a66" Demon Bracers
"a67" Divine Robe
"a68" Divine Circlet
"a69" Divine Shoes
"a70" Divine Bracers
"a71" Storm Cloak
"a72" Durable Cloak
"a73" Blessed Cloak
"a74" Hiking Jar
"a75" Hiking Bag
"a78" Council Armor
"a79" Council Helmet
"a80" Council Boots
"a81" Council Gauntlets
"a82" Council Shield
"a83" Griffin Armor
"a84" Griffin Helmet
"a85" Griffin Boots
"a86" Griffin Gloves
"a87" Celestial Armor
"a88" Celestial Helmet
"a89" Celestial Boots
"a90" Celestial Bracers
"k03" Hunter shaft
"k04" War hammer head
"k06" Order Armor piece
"k15" Clarity Robe piece
"k25" Composite Bow shaft
"k26" Lightning Bow shaft
"k27" Hailstorm Bow shaft
"k28" Imperial Axe head
"k29" Skull Crusher head
"k30" Dragon Mace head
"k33" Crusader Armor piece
"k38" Royal Armor piece
"k51" Demon Robe piece
"k55" Divine Robe piece
"key" 🗝Key
"td1 "Colorless shard
"w01" Wooden sword
"w02" Short sword
"w03" Long sword
"w04" Widow sword
"w05" Knight's sword
"w06" Elven sword
"w07" Rapier
"w08" Short spear
"w09" Long spear
"w10" Lance
"w11" Elven spear
"w12" Halberd
"w13" Kitchen knife
"w14" Battle knife
"w15" Steel dagger
"w16" Silver dagger
"w17" Mithril dagger
"w18" Short Bow
"w19" Wooden Bow
"w21" Elven Bow
"w22" Forest Bow
"w23" Club
"w24" Bone club
"w26" Steel axe
"w27" Mithril axe
"w28" Champion Sword
"w29" Trident
"w30" Hunter Bow
"w31" War hammer
"w32" Hunter dagger
"w33" Thundersoul Sword
"w35" Eclipse
"w36" Guard's Spear
"w37" King's Defender
"w38" Raging Lance
"w39" Composite Bow
"w41" Hailstorm Bow
"w42" Imperial Axe
"w44" Dragon Mace
"w45" Ghost dagger
w46 Lion Knife
w91 Griffin Knife
w92 Minotaur Sword
w93 Phoenix Sword
w94 Heavy Fauchard
w95 Guisarme
w96 Meteor Bow
w97 Nightfall Bow
w98 Black Morningstar
w99 Maiming Bulawa
a100 Assault Cape
a101 Craftsman Apron
a102 Stoneskin Cloak"""



turns = {
            "null":"null",
        }
