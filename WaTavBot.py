#!/usr/bin/env python
# -*- coding: utf-8 -*-
#5176 puntos
#Logging, para empezar a monitorear el desmadre desde el principio
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
#TOKEN = "688638504:AAEInD-EFrYbKkw6tlJBIIpRmQsBJRbpTio" #TavernKeeperBot
TOKEN = "1184989658:AAFZfzq2y-lV29GjpVJfiXaH01qQBhdwyRI" #WaTavBot
# Create the Updater and pass it your bot's token.
updater = Updater(TOKEN, use_context=True)
(ME,    MEINFO,     MEWEAPONS,
BR,     BRNO1,      BRS1,       BRTALK,     BRNOTALK,
DC,     DCNO1,      DCS1,       DCDUEL,
BS,     BSWEAPONS,  BSPECIAL,   BSSBUY,
L7,     L7NO1,      L7S1,       L7PLAY,
HELP,   HME,        HBR,        HDC,        HBS,        HL7,
BACK
) = range(27)


#Librerías de utilidades
from random import randint as rng,choice
from time import sleep
import miscellaneous as misc
import Braile as br
import FullWidth as fw
from tree import tree as tree
import math

#Manejo de Base de Datos
import json
from firebase import firebase
fire = firebase.FirebaseApplication("https://watavbot.firebaseio.com",None)

#Otras librerías para el desarrollo
from uuid import uuid4
import sys, os
import threading
import multiprocessing
from html import escape

PlayerDB = fire.get("/players",None)
#print(str(PlayerDB))
WeaponDB = fire.get("/weapons",None)
#print(str(WeaponDB))
categories = ["dagger","sword","axe",
            "hammer","polearm","whip",
            "ranged","magic","shield"]
tmpPlayers = {'0':'null'}
ArenaList = {'0':'null'}

class kb:
    def kb(op = None, args = None):
        IKB = InlineKeyboardButton
        if(op == 'data'):
            keyboard = [[IKB("Join", callback_data = args)]]
        elif(op == 'dice'):
            keyboard = [[IKB("Roll", callback_data = args)]]
        elif(op == 'start'):
            keyboard = [
                [
                    IKB("🎫 Traveller Card"),
                    IKB("🍻 Beer"),
                    IKB("⚔️ Duelling Court")
                ],
                [
                    IKB("⚒ Blacksmith"),
                    IKB("🎲 Lucky Seven"),
                    IKB("📝 Help")
                ]
            ]
        elif(op == 'hits'):
            keyboard = [
                [
                    IKB("🗡Head", callback_data="{\"op\":\"batt|mov:ah\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Head", callback_data="{\"op\":\"batt|mov:dh\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],

                [
                    IKB("🗡Body", callback_data="{\"op\":\"batt|mov:ab\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Body", callback_data="{\"op\":\"batt|mov:db\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],

                [
                    IKB("🗡Legs", callback_data="{\"op\":\"batt|mov:al\",\"room\":\"%s\",\"host\":\"%s\"}"%(args)),
                    IKB("🛡Legs", callback_data="{\"op\":\"batt|mov:dl\",\"room\":\"%s\",\"host\":\"%s\"}"%(args))
                ],
            ]
        elif(op == 'wtypes'):
            keyboard = [
                [
                    IKB("Sword",    callback_data="{\"op\":\"%s\",\"d1\":\"sword\",\"d2\":\"%s\"}"%(args)),
                    IKB("Dagger",   callback_data="{\"op\":\"%s\",\"d1\":\"dagger\",\"d2\":\"%s\"}"%(args)),
                    IKB("Axe",      callback_data="{\"op\":\"%s\",\"d1\":\"axe\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Polearm",  callback_data="{\"op\":\"%s\",\"d1\":\"polearm\",\"d2\":\"%s\"}"%(args)),
                    IKB("Hammer",   callback_data="{\"op\":\"%s\",\"d1\":\"hammer\",\"d2\":\"%s\"}"%(args)),
                    IKB("Whip",     callback_data="{\"op\":\"%s\",\"d1\":\"whip\",\"d2\":\"%s\"}"%(args))
                ],
                [
                    IKB("Ranged",   callback_data="{\"op\":\"%s\",\"d1\":\"ranged\",\"d2\":\"%s\"}"%(args)),
                    IKB("Magic",    callback_data="{\"op\":\"%s\",\"d1\":\"magic\",\"d2\":\"%s\"}"%(args)),
                    IKB("Shield",   callback_data="{\"op\":\"%s\",\"d1\":\"shield\",\"d2\":\"%s\"}"%(args))
                ],
            ]
        else:
            keyboard = [[IKB("╔"),IKB("╗")],[IKB("╚"),IKB("╝")]]
        return keyboard

class Player:
    def __init__(self,name,last_name,id):
        self.name = name
        self.last_name = last_name
        self.id = id
        self.link = ('<a href="tg://user?id={}">{}</a>'.format(id,escape(name))).strip()
        self.hp = 100
        self.Atk = None
        self.Def = None
        self.ready = False
        self.time = None
        self.pron = ''
        self.mainW = {}
        self.offHW = {}
        self.registered = False
        self.regCheck()
        self.genAssign()
        self.weapAssign()
        return

    def regCheck(self):
        global PlayerDB
        if(str(self.id) in list(PlayerDB.keys())):
            self.registered = True
        else:
            self.registered = False

    def weapAssign(self):
        global PlayerDB
        if(str(self.id) in list(PlayerDB.keys())):
            self.mainW = WeaponDB[PlayerDB[str(self.id)]["mainW"]]
            self.offHW = WeaponDB[PlayerDB[str(self.id)]["offHW"]]
        else:
            self.mainW = WeaponDB['01']
            self.offHW = WeaponDB['02']
        return

    def genAssign(self):
        pronouns = {
            'he':{
                'nomin':'he',
                'object':'him',
                'possAdj':'his',
                'possPro':'his',
                'reflex':'himself'
            },
            'she':{
                'nomin':'she',
                'object':'her',
                'possAdj':'her',
                'possPro':'hers',
                'reflex':'herself'
            },
            'it':{
                'nomin':'it',
                'object':'it',
                'possAdj':'its',
                'possPro':'its',
                'reflex':'itself'
            },
            'we':{
                'nomin':'we',
                'object':'us',
                'possAdj':'our',
                'possPro':'ours',
                'reflex':'ourself'
            },
            'they':{
                'nomin':'they',
                'object':'them',
                'possAdj':'their',
                'possPro':'theirs',
                'reflex':'themself'
                }
            }
        if(str(self.id) in list(PlayerDB.keys())):
            self.pron = pronouns[PlayerDB[str(self.id)]['pron']]
        else:
            self.pron = pronouns['it']
        return

    def texts(self):
        txt = """
{}, seguro de su poder y habilidad sobre {} no se imagino el salvajismo indescriptible e inimaginable de lo que este era capaz,quedando así a merced de su espada al haber subestimao a su oponente...

Tras horas de arduo e intenso combate {} logró descubrir una apertura en la legendaria defensa de su oponente, y con movimientos dignos de un gran guerrero logró someter a su fiero rival

En esta ocasion su espada ha encontrado un adversario digno, con el cual ha sostenido uno de los encuentros mas emocionantes pues su adversario al igual que él no planeaba rendirse hasta que su sed de sangre fuese satisfecha

Con dolor y dificultad levanta su espada con manchas de sangre enemiga, transformando así el dolor y sangre que recorre su cuerpo en gritos de gloria, pues su oponente ha encontrado en sus manos una muerte gloriosa como aquellas de antaño"""
        return ''

    def to_dict(self):
        data = {}
        data["name"] = self.name
        data["last_name"] = self.last_name
        data["id"] = self.id
        data["link"] = self.link
        data["hp"] = self.hp
        data["atk"] = self.Atk
        data["def"] = self.Def
        data["ready"] = self.ready
        data["time"] = self.time
        data["pron"] = self.pron
        data["mainW"] = self.mainW
        data["offHW"] = self.offHW
        data["registered"] = self.registered
        return data

    def chrono(self):
        time = 0
        while((self.ready == False) and (time < 30000)):
                sleep(.00085)
                time += 1
        #print('stop -> {t} seconds'.format(t=str(time/1000)))
        if(time >= 30000):
            if(self.Atk == None):
                self.Atk = "nop"
            if(self.Def == None):
                self.Def = "nop"
        self.time = time/1000
        return

class ArenaObject:
    def __init__(self,room,P1,P2,text):
        self.room = room
        self.Players = {}
        self.Players[P1.id]=P1
        self.Players[P2.id]=P2
        self.round = 0
        self.text = text
        self.alive = False
        return

    def playersInfo(self):
        prs = {}
        for p in self.Players.keys():
            prs[p] = {**self.Players[p].to_dict()}
        return prs

    def movAssign(self,Pid,mov):
        if(mov[0] == 'a'):
            if(self.Players[Pid].Atk == None):
                self.Players[Pid].Atk = mov[1]
            else:
                return False
        else:
            if(self.Players[Pid].Def == None):
                self.Players[Pid].Def = mov[1]
            else:
                return False
        return True

    def movCheck(self):
        p1,p2 = list(self.Players.keys())

        if((self.Players[p1].Atk != None) and (self.Players[p1].Def != None)):
            self.Players[p1].ready = True

        if((self.Players[p2].Atk != None) and (self.Players[p2].Def != None)):
            self.Players[p2].ready = True

        sleep(0.0002)
        if((self.Players[p1].time != None) and (self.Players[p2].time != None)):
            return True
        else:
            return False

    def movClear(self):
        prs = list(self.Players.keys())
        for p in prs:
            self.Players[p].Atk = None
            self.Players[p].Def = None
            self.Players[p].ready = False
            self.Players[p].time = None
        return

    def dmgCalc(self):
        prs = list(self.Players.keys())
        part = {'h':'Head','b':'Body','l':'Legs'}
        crit = 1
        critxt = ""
        text = "\n<b>Round: %i</b>"%(self.round+1)
        t1 = self.Players[prs[0]].time
        t2 = self.Players[prs[1]].time

        if(t1 > t2):
            prs.reverse()
            if((t1-3) > t2):
                crit = (int(self.Players[prs[0]].mainW["crit"])+int(self.Players[prs[0]].offHW["crit"]))/2
                critxt = "<b>(*CRIT*💀)</b>"
        else:
            if((t2-3) > t1):
                crit = 1.5
                critxt = "<b>(*CRIT*💀)</b>"

        atk = self.Players[prs[0]].Atk
        df = self.Players[prs[1]].Def
        dam = self.atkdef(atk,df,crit)

        if(dam == 0):
            critxt = ""


        if(dam < 0):
            if(dam == -10):
                if(self.Players[prs[1]].hp >= 100):
                    self.Players[prs[1]].hp += dam
                text += '\n%s seems to tired to do something, giving %s time to recover some health(+%i❤️)'%(
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    -dam
                )
            elif(dam == -100):
                text = '\nBoth warriors seem so bored, so they decided to leave the battle and go for a walk...'
                self.Players[prs[0]].hp = 0
                self.Players[prs[1]].hp = 0
                return text
        else:
            if(dam == 100):
                text += '\n%s got caught totally unaware by %s, allowing %s to deal a <code>%s</code> on %s (%i).'%(
                    self.Players[prs[1]].name,
                    self.Players[prs[0]].name,
                    self.Players[prs[0]].name,
                    fw.toFullWidth("FATAL BLOW"),
                    self.Players[prs[1]].pron['object'],
                    dam

                )
            else:
                text += "\n%s attacked %s's %s with %s %s"%(
                    self.Players[prs[0]].name,
                    self.Players[prs[1]].name,
                    part[atk].lower(),
                    self.Players[prs[0]].pron['possAdj'],
                    self.Players[prs[0]].mainW["name"]
                    )

                if(dam > 0):
                    text += ', dealing %s%s damage.'%(
                        str(dam),
                        critxt
                    )

                else:
                    text += ', but %s managed to defend %s using %s %s.'%(
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].pron['reflex'],
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].offHW['name']
                    )
        self.Players[prs[1]].hp -= dam

        if(self.Players[prs[1]].hp > 0):
            atk = self.Players[prs[1]].Atk
            df = self.Players[prs[0]].Def
            dam = self.atkdef(atk,df,crit)

            if(dam < 0):
                if(dam == -10):
                    if(self.Players[prs[0]].hp >= 100):
                        self.Players[prs[0]].hp += dam
                    text += '\n%s seems to tired to do something, giving %s time to recover some health(+%i❤️)'%(
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        -dam
                    )
                elif(dam == -100):
                    text = '\nBoth warriors seem so bored, so they decided to leave the battle and go for a walk...'
                    self.Players[prs[1]].hp = 0
                    self.Players[prs[0]].hp = 0
                    return text
            else:
                if(dam == 100):
                    text += '\n%s got caught totally unaware by %s, allowing %s to deal a <code>%s</code> on %s.'%(
                        self.Players[prs[0]].name,
                        self.Players[prs[1]].name,
                        self.Players[prs[1]].name,
                        fw.toFullWidth("FATAL BLOW"),
                        self.Players[prs[0]].pron['object']

                    )
                else:
                    text += "\n%s attacked %s's %s with %s %s"%(
                        self.Players[prs[1]].name,
                        self.Players[prs[0]].name,
                        part[atk].lower(),
                        self.Players[prs[1]].pron['possAdj'],
                        self.Players[prs[1]].mainW["name"]
                        )

                    if(dam > 0):
                        text += ', dealing %s damage.'%(
                            str(dam)
                        )

                    else:
                        text += ', but %s managed to defend %s using %s %s.'%(
                            self.Players[prs[0]].name,
                            self.Players[prs[0]].pron['reflex'],
                            self.Players[prs[0]].pron['possAdj'],
                            self.Players[prs[0]].offHW['name']
                        )
            self.Players[prs[0]].hp -= dam
        else:
            self.Players[prs[1]].hp = 0
            text += "\n%s was too weak to keep fighting."%(self.Players[prs[1]].name)
        if(self.Players[prs[0]].hp < 0):
            self.Players[prs[0]].hp = 0
        return text+'\n'

    def atkdef(self,atk,df,crit):#Dam (== -100), (-10), (== 0), (> 0), (== 100)
        if(atk == df):
            if(atk == 'nop'):
                return -100
            else:
                return 0
        elif(df == 'nop'):
            return 100
        else:
            if(atk == 'h'):
                return rng(15,25)*crit
            elif(atk == 'b'):
                return rng(12,20)*crit
            elif(atk == 'l'):
                return rng(5,10)*crit
            else:#atk == 'nop'
                return -10

    def throwChronos(self):
        prs = list(self.Players.keys())
        for p in prs:
            threading.Thread(target=self.Players[p].chrono).start()
        return

    def lifeCheck(self):
        text = ''
        prs = list(self.Players.keys())
        if(self.Players[prs[0]].hp > self.Players[prs[1]].hp):
            win = self.Players[prs[0]].id
            lose = self.Players[prs[1]].id
        elif(self.Players[prs[1]].hp > self.Players[prs[0]].hp):
            win = self.Players[prs[1]].id
            lose = self.Players[prs[0]].id
        else:
            text = "What a boring battle... What a waste of time..."
            return "<b>⚔Duel⚔</b>"+self.text+'\n'+text

        if(self.Players[win].hp > 100):
            status = [
                "One can feel heavy nausea from what just hapened here...",
                ", just like a vampire just sucked dry ",
                "'s life... May the gods save us from such an abomination!"
                ]
        elif(self.Players[win].hp == 100):
            status = [
                "Against all odds, the warrior",
                "got a flawless victory against {possAdj} opponent".format(possAdj=self.Players[win].pron["possAdj"]),
                "Ladies and gentleman, this is the face of a true champion!!!"
                ]
        elif(self.Players[win].hp > 66):
            status = [
                "Like it was a child's play,",
                "easely vanquished",
                "in combat."]
        elif(self.Players[win].hp > 33):
            if(self.round > 5):
                length = "long"
            else:
                length = "short"
            status = [
                "After a {} heated battle,".format(length),
                "was able to overtake",
                "in what it seemed a paired match."
                ]
        else:
            status = [
                "The fight was bloody and brutal, but in the end",
                "could barely surpass {possAdj} opponent".format(possAdj=self.Players[win].pron["possAdj"]),
                "in the last second."
                ]

        text += "\n{}❤️{}\n\t\t\t<b>VS</b>\n{}❤️{}".format(
            self.Players[prs[0]].hp,
            self.Players[prs[0]].link,
            self.Players[prs[1]].hp,
            self.Players[prs[1]].link,)

        text += "<i>\n\n{} </i>{}<i> {} </i>{}<i> {}</i> \n<b>🎊 🎉 Congrats {}!!! 🎉 🎊</b>".format(
                                        status[0],
                                        self.Players[win].name,
                                        status[1],
                                        self.Players[lose].name,
                                        status[2],
                                        self.Players[win].name)

        return "<b>⚔Duel⚔</b>"+self.text+'\n'+text

def keepAlive(update:Update,context:CallbackContext,arena:ArenaObject):
    query = update.callback_query
    data = json.loads(query.data)
    room = data['room']
    host = int(data['host'])
    counter = 0
    while(counter < 4):
        sleep(1)
        counter += 1
        if(arena.alive):
            arena.alive = False
            counter = 0
            #print("Reset!")
    #print("Time's up!")
    if(arena.movCheck()):
        arena.text += arena.dmgCalc()
        prs = list(arena.Players.keys())
        if((arena.Players[prs[0]].hp > 0) and (arena.Players[prs[1]].hp > 0)):
            text = "<b>⚔Duel⚔</b>"+arena.text+"\n%s❤️ %s\nVs\n%s❤️ %s\n"%(
                arena.Players[prs[0]].hp,
                arena.Players[prs[0]].name,
                arena.Players[prs[1]].hp,
                arena.Players[prs[1]].name,
            )
            rpmkup = InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host)))
            arena.movClear()
            arena.throwChronos()
            arena.round += 1
            threading.Thread(target=keepAlive,args=(update,context,arena,)).start()
        else:
            text = arena.lifeCheck()
            rpmkup = None
        context.bot.edit_message_text(
            text=text,
            inline_message_id=query.inline_message_id,
            reply_markup=rpmkup,
            parse_mode=ParseMode.HTML
        )
        return
    else:
        #print('retrying...')
        keepAlive(update,context,arena)
    return

def battle(update:Update,context:CallbackContext):
    global ArenaList,tmpPlayers
    query = update.callback_query
    data = json.loads(query.data)

    option,phase = data["op"].split("|")
    if("mov:" in phase):
        phase,mov = phase.split(":")
    room = data['room']
    host = int(data['host'])
    try:
        host_link = ('<a href="tg://user?id={}">{}</a>'.format(host,escape(tmpPlayers[host]['first_name']))).strip()
    except KeyError as e:
        context.bot.answerCallbackQuery(query.id,"This session has expired.",True)
        context.bot.edit_message_text(
                                        text="<b>⚔Duel</b>\n<i>A heavy thunderstorm has started... Both combatants have decided to postpone their fight until the storm ceases... </i>",
                                        inline_message_id=query.inline_message_id,
                                        parse_mode=ParseMode.HTML)
        #error(update,e)
        return

    presser = update.effective_user
    presser_link = ('<a href="tg://user?id={}">{}</a>'.format(presser.id,escape(presser.first_name))).strip()

    if(phase == 'p2'):
        if(host == presser.id):
            quotes = ['The most difficult struggles are the ones you fight with yourself...',
                'A fight with yourself to win the battle for yourself is the biggest and most important one.',
                'Fight with yourself to get the best from yourself.',
                'When you fight yourself to discover the real you, there\'s only one winner.',
                'You don\'t realize how strong you are until you\'re fighting yourself.',
                'It isn\'t ever the world you fight. Always, always, it\'s yourself.',
                'The toughest battle you\'ll ever fight in your life is the battle within yourself.',
                'Fight with others doesn\'t make you sleepless; fighting with yourself is what makes you restless.']
            context.bot.answerCallbackQuery(query.id,'“'+choice(quotes)+'”',True)
            return
        else:
            text = '<b>⚔Duel</b>\nBoth opponents are set! \n%s will face %s on the arena! \n<i>May the gods be with you, warriors...</i>\n\nWaiting for the host to start the duel...'%(host_link,presser_link)
            ArenaList[room] = ArenaObject(
                                            room = room,
                                            P1 = Player(tmpPlayers[host]['first_name'],tmpPlayers[host]['last_name'],host),
                                            P2 = Player(presser.first_name,presser.last_name,presser.id),
                                            text = '')
            context.bot.edit_message_text(
                                            text=text,
                                            inline_message_id=query.inline_message_id,
                                            reply_markup = InlineKeyboardMarkup (
                                                                                    [
                                                                                        [
                                                                                            InlineKeyboardButton(
                                                                                                text = "Start the match!",
                                                                                                callback_data = "{\"op\":\"batt|start\",\"room\":\"%s\",\"host\":\"%s\"}"%(room,host)
                                                                                            )
                                                                                        ]
                                                                                    ]
                                                                                ),
                                            parse_mode=ParseMode.HTML)
            return
    try:
        arena = ArenaList[room]#From here on, there's only blood and glory!
    except KeyError as e:
        context.bot.answerCallbackQuery(query.id,"This session has expired.",True)
        context.bot.edit_message_text(
                                        text="<b>⚔Duel</b>\n<i>A heavy thunderstorm has started... Both combatants have decided to postpone their fight until the storm ceases... </i>",
                                        inline_message_id=query.inline_message_id,
                                        parse_mode=ParseMode.HTML)
        #error(update,e)
        return

    if(presser.id not in list(arena.Players.keys())):
        context.bot.answerCallbackQuery(query.id,"What are you doing? This is not your Fight!",True)
        return
    elif(phase == 'start'):
        if(presser.id != host):
            context.bot.answerCallbackQuery(query.id,"You have to wait for the host to start the match.",True)
            return
        P1,P2 = arena.Players.keys()
        text = "<b>⚔Duel</b>\nThe match has started!\n%s❤️ %s\nVs\n%s❤️ %s\n\nRound: %s\nWhat will you do?\n<b>Choose attack and defense points.</b>"%(
            str(int(arena.Players[P1].hp)),
            arena.Players[P1].name,
            str(int(arena.Players[P2].hp)),
            arena.Players[P2].name,
            arena.round+1)
        context.bot.edit_message_text(
                                        text=text,
                                        inline_message_id=query.inline_message_id,
                                        reply_markup=InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host))),
                                        parse_mode=ParseMode.HTML)
        arena.throwChronos()
        threading.Thread(target=keepAlive,args=(update,context,arena,)).start()
        return

    elif(phase == 'mov'):
        act = {'a':'Attack','d':'Defend'}
        part = {'h':'Head','b':'Body','l':'Legs'}
        mc = arena.movAssign(presser.id,mov)
        if(mc):
            context.bot.answerCallbackQuery(query.id,act[mov[0]]+' '+part[mov[1]],False)
            arena.alive = True
        else:
            context.bot.answerCallbackQuery(query.id,"Sorry, you already chose what to %s"%(act[mov[0]]),True)
            return
        if(arena.movCheck()):
            battletext = arena.dmgCalc()
            arena.round += 1
            p1,p2 = list(arena.Players.keys())
            p1n = arena.Players[p1].link
            p1h = arena.Players[p1].hp

            p2n = arena.Players[p2].link
            p2h = arena.Players[p2].hp
            arena.text += battletext
            text = str("<b>⚔Duel⚔</b>\n"
                +"{btext}".format(btext=arena.text)
                +"\n\n{health}❤️ {name}".format(health=str(math.ceil(p1h)),name=p1n)
                +"\n\t\t\t\tVs"
                +"\n{health}❤️ {name}\n".format(health=str(math.ceil(p2h)),name=p2n)
            )
            if(p1h > 0 and p2h > 0 ):
                arena.movClear()
                arena.throwChronos()
                rpmkup = InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host)))
            else:
                arena.movClear()
                text = arena.lifeCheck()
                rpmkup = None
            try:
                context.bot.edit_message_text(
                                                text=text,
                                                inline_message_id=query.inline_message_id,
                                                reply_markup=rpmkup,
                                                parse_mode=ParseMode.HTML)
            except Exception as e:
                error(update,e)
            return

    return

def start(update: Update, context: CallbackContext):
    query = update.message.from_user
    text = """You approach and see a sign at the door:\n
<i>Excuse us, by the moment we\'re under maintenance...
However you can always use our dueling court that is in the back. Just write: \n\"@WanderersTavernBot + <code>space</code>\"\n and press \"⚔Duel\" on any chat window to access to it.
<s>(random stuff may happen due to quantum physics.)</s>
We\'ll be on business in a couple of days...</i>
\n"""
    update.message.reply_text(
                                text,
                                reply_markup = None,
                                parse_mode=ParseMode.HTML
                            )

    return

def register(update: Update, context: CallbackContext):
    user = update.message.from_user
    IKB = InlineKeyboardButton
    if(str(user.id) in list(PlayerDB.keys())):
        welcometext = "Welcome back, {name}! \nHow may I serve you today?".format(name=user.first_name)
        reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)
        update.message.reply_text(
            text=welcometext,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        return ConversationHandler.END
    else:
        text = str("Well, well, well... What do we have here? You seem to be new around here, aren't ya?"
            +" Welcome to the <i>Wanderers' Tavern</i>, traveller, where you can find the best beer you will ever find all across the continent."
            +"\nName's Mickey, and I'm the one who serves around here."
            +"\nBefore anything else, please, traveller, let me know your gender... ")
        reply_markup = InlineKeyboardMarkup([
                                                [
                                                    IKB("♀ Lady",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='she',d2=str(user.id))+'}'),
                                                    IKB("♂ Gentleman",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='he',d2=str(user.id))+'}')
                                                ],
                                                [
                                                    IKB("🕈 Undead",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='it',d2=str(user.id))+'}'),
                                                    IKB("☭ Comrade",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='we',d2=str(user.id))+'}')
                                                ],
                                                [IKB("▣ Other",callback_data = '{'+"\"op\":\"reg|gen\",\"d1\":\"{d1}\",\"d2\":\"{d2}\"".format(d1='they',d2=str(user.id))+'}')]
                                            ]
                                          )
        update.message.reply_text(
                                    text,
                                    reply_markup = reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
        return

def reg(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option,next = data["op"].split("|")
    user = query.from_user
    if(next == 'gen'):
        if(data["d1"] == "we"):
            namename = "Comrade"
        else:
            namename = user.first_name
        text = str('<i>Ah, worderful! And your name is... I see. Nice to meet you, {name}!\n\n'.format(name=namename)
            +"Here, have a drink, courtesy of the house! If you like it, you can always come back and have one 🍻 Beer for just 5💰."
            +" Who knows? Maybe you can make some new friends while drinking..."
            +"\n\nWe also have a ⚔️ Duellng Court in the back, you can always come and take a challenge with another traveller,"
            +" or you can just fight with a friend, all you have to do is to write: </i>\n\n@WanderersTavernBot + <code>space</code>\n\n<i>On any chat window,"
            +" and pressing the ⚔Duel button, then you'll be able to challenge any friend you want, even if they haven't even visited the tavern before..."
            +"\nHuh! What is a chat window, by the way?"
            +"\n\nAnyway, you can also play 🎲 Lucky Seven in our gambling tables. Also with a stranger, or call it via inline message the same way as the duels with friends:"
            +"</i>\n\n@WanderersTavernBot + <code>space</code>\n\n<i> and pressing the 🎲Dice button."
            +"\n\nFinally, on the back, next to the duelling court, there's a blacksmith, who forges and sells weapons of the finest quality."
            +" There you can buy anything that fits better your combat style."
            +"\n\nWith nothing more to say, make yourself comfortable, and enjoy the atmosphere and the company with a good drink!</i>")
        try:
            context.bot.edit_message_reply_markup(
                chat_id=user.id,
                message_id=query.message.message_id,
                #inline_message_id=query.inline_message_id,
                reply_markup=None
            )
            reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard=True)
            context.bot.send_message(
                chat_id=user.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup)
            threading.Thread(target=newUser,args=(user,data["d1"],)).start()
        except Exception as e:
            error(update,e)
    return

def newUser(user,pron):
    global PlayerDB
    money = 0
    for l in str(user.id):
        money += int(l)

    info = {
        "username":user.username,
        "exp":0,
        "mainW":"01",
        "money":money,
        "offHW":"02",
        "pron":pron,
        "weapons":["01","02"],
        "rank":0
    }
    fire.put("/players",user.id,info)
    PlayerDB[str(user.id)] = info
    #print(PlayerDB[str(user.id)])
    return

def reload(update: Update, context: CallbackContext):
    user = update.message.from_user
    if(user.id == 184075777):
        def reloadTask():
            global PlayerDB,WeaponDB
            PlayerDB = fire.get("/players",None)
            WeaponDB = fire.get("/weapons",None)
            context.bot.send_message(
                chat_id = user.id,
                text="<code>Reloaded!</code>",
                parse_mode = ParseMode.HTML
                )
            return
        threading.Thread(target = reloadTask).start()
    return


def upload(player,concept,value):
    threading.Thread(target=manualupload,args=("/players/{id}".format(id=player),concept,value,)).start()
    return

def manualupload(player,concept,value):
    global PlayerDB
    if(type(concept) in [list,tuple]):
        for c in range(len(concept)):
            try:
                fire.put(player,concept[c],value[c])
            except:
                e = "{}/{} = {}".format(player,concept[c],value[c])
                error("At manualupload",e)
    else:
        fire.put(player,concept,value)
    PlayerDB = fire.get("/players",None)
    return

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    option,next = data["op"].split("|")
    #print(tree(update.to_dict(),HTML=False))
    ##print("Acá elijo qué se va a hacer :9")
    if(option == "batt"):
        threading.Thread(target = battle, args = (update,context,)).start()
        ##print("Acá fue battle!")
    if(option == "dice"):
        threading.Thread(target = dice, args = (update,context,)).start()
        ##print("Acá fue dado!")
    if(option == "reg"):
        threading.Thread(target = reg, args = (update,context,)).start()
    if(option == "owned"):
        threading.Thread(target = owned, args = (update,context,)).start()
    if(option == "bsmith"):
        threading.Thread(target = shopcat, args = (update,context,)).start()
    return

def dice(update: Update, context: CallbackContext):
    query = update.callback_query
    data = json.loads(query.data)
    d1 = rng(1,6)
    d2 = rng(1,6)
    dir = "/utils/dice"
    Dices = [ "⚀", "⚁", "⚂", "⚃", "⚄", "⚅" ]
    D1 = Dices[d1-1]
    D2 = Dices[d2-1]
    add = ""
    if(d1+d2 == 7):
        add = " Lucky Seven!!"
    text = "{} threw the dices, and...\nThe dices show {}({}) and {}({})...\n<b>{} got {}{}!</b>\n\n".format(
                                    query.from_user.first_name,
                                    D1,d1,
                                    D2,d2,
                                    query.from_user.first_name,
                                    d1+d2,
                                    add
                                    )
    ##print(text)
    context.bot.edit_message_text(
                            text=text,
                            inline_message_id=query.inline_message_id,
                            parse_mode=ParseMode.HTML
                        )
    return

def inlinequery(update: Update, context: CallbackContext):
    #Handle the inline query.
    global tmpPlayers
    query = update.inline_query
    target = update.inline_query.from_user
    target_name = ('<a href="tg://user?id={}">{}</a>'.format(target.id,escape(target.first_name))).strip()
    reply_markup = None
    tmpPlayers[target.id] = {
        'first_name':target.first_name,
        'last_name':target.last_name,
        'username':target.username}
    #print(tree(update.to_dict()))

    results = [
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="⚔Duel",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "data",args = "{\"op\":\"batt|p2\",\"room\":\"%s\",\"host\":\"%s\"}"%(str(int(list(ArenaList.keys())[-1])+1),str(target.id)))),
                                            input_message_content= InputTextMessageContent(
                                                                                            message_text = "<b>⚔Duel</b>\n{} is looking for a worthy opponent...{}".format(target_name,"\n\n<code>You can also register at </code>@WanderersTavernBot<code> to customize yourself...</code>"),
                                                                                            parse_mode=ParseMode.HTML,
                                                                                            reply_markup = reply_markup,
                                                                                         )
                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🎲Dice",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "dice",args = "{\"op\":\"dice|dice\",\"next\":\"dice\",\"room\":\"%s\"}"%(target.username))),
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "Press <i>\"Roll\"</i> to roll the dices...",
                                                                                            parse_mode=ParseMode.HTML,
                                                                                            reply_markup = reply_markup
                                                                                        ),

                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🍺Beer",
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "You are given a jar full frothy beer🍺.\n{}: <i>Let's toast for the pleasure of being here and now!</i>".format(target_name),
                                                                                            parse_mode=ParseMode.HTML
                                                                                        )
                                        )
              ]
    if("&Codify" in query.query):
        txt = query.query.replace("&Codify ","")
        txt = br.toBraile(txt)
        results.append(
                        InlineQueryResultArticle(
                                                    id=uuid4(),
                                                    title="⠨⠉⠕⠝⠧⠑⠗⠞⠖",
                                                    input_message_content= InputTextMessageContent(
                                                                                                    message_text = txt,
                                                                                                    parse_mode=ParseMode.HTML
                                                                                                    #reply_markup = reply_markup,
                                                                                                 )
                                                )
                        )
    if(False):
        results.append(
                        InlineQueryResultArticle(
                                                    id=uuid4(),
                                                    title="🎖{} Tournament🏅".format(query.query.title()),
                                                    input_message_content= InputTextMessageContent(
                                                                                                    message_text = "<b>Join the {} Tournament!</b>\n\nPlayers:\n".format(query.query.title()),
                                                                                                    parse_mode=ParseMode.HTML
                                                                                                    #reply_markup = reply_markup,
                                                                                                 )
                                                )
                        )
    context.bot.answer_inline_query(
                        update.inline_query.id,results=results,
                        cache_time = 1,
                        is_personal=True,
                        switch_pm_text='Enter the Tavern',
                        switch_pm_parameter='register')
    #update.inline_query.answer(results)
    return

def error(update,error="Unexpected Error!"):
    """Log Errors caused by Updates."""
    global updater
    bot=updater.bot
    Mickey = 184075777
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        update = update.to_dict()
    except:
        update = str(update)
    #print(str(fname))
    message = "Update: \n{} \n...Caused error: \n\n<code>{}:{}</code> in <code>{}</code> at line <code>{}</code>\n\nNotes: {}".format(
                tree(update,HTML=True),
                escape(str(exc_type)),
                escape(str(exc_obj)),
                escape(str(fname)),
                escape(str(exc_tb.tb_lineno)),
                escape(str(error)))
    bot.send_message(Mickey,message,parse_mode=ParseMode.HTML)
    message = message.replace("<code>","")
    message = message.replace("</code>","")
    logger.warning(message)
    return

def fallback(update: Update, context: CallbackContext):
  context.update_queue.put(update)
  return ConversationHandler.END

def connect(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.bot.send_message(
        chat_id = user.id,
        text="Connected!",
        parse_mode = ParseMode.HTML
        )
    return

def me(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    def rank(num):
        if(num < 33):
            return '🥉'
        elif(num < 67):
            return '🥈'
        elif(num < 100):
            return '🥇'
        else:
            return '🎖'
    offhw = '[Two-Handed]'
    if(player["mainW"] != player["offHW"]):
        offhw = WeaponDB[player["offHW"]]["name"]
    text=str('<b>🎫 Traveller Card</b>'
        +"\n\nName: {name}".format(name=user.first_name)
        +"\nExp: {exp}".format(exp=str(player["exp"]))
        +"\nMoney: {money}💰".format(money=player["money"])
        +"\nRank: {rank}".format(rank=rank(player["rank"]))
        +"\n\n🎒 Equipment:\n"
        +"\t"*4+"► Main: {main}\n".format(main=WeaponDB[player["mainW"]]["name"])
        +"\t"*4+"► Offhand: {offh}".format(offh=offhw)
        +"\n\nCard no. <code>{id}</code>".format(id=user.id)
        )
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("🗡 Weapons"),
                IKB("↩️ Go Back")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return ME

def beer(update: Update, context: CallbackContext):
    text="You sat and enjoyed a cold and frothy beer... Unfortunately, the tabern seems empty by now.\nMaybe later more people will come.\n\nBut don't worry, the house invites this round! 🍻🍻🍻"
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("👥 Talk"),
                IKB("↩️ Go Back")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return

def duellingcourt(update: Update, context: CallbackContext):
    text='The duelling court seems empty by now... \nMaybe if you brought a friend, you both could practice a while!'
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("↩️ Leave")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return DC

def blacksmith(update: Update, context: CallbackContext):
    text=str("Heya! Good day, adventurer! I'm {name}, the blacksmith. I sell the best weapons you'll be able to find this side of the sea!".format(name="Pyot'r")
        +"\nYou see... Right now I don't have my hammer, my anvil nor my press, which I use to forge new weapons, so, I'm not taking orders right now..."
        +"\nFortunately, I have a stash of weapons on my depot. So, if you want, you can take a look at them, I have weapons for all tastes, as you'll see.")
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("📦 Shop"),
                IKB("♨️ Forge"),
            ],
            [
                IKB("↩️ Go Back")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return BS

def shop(update: Update, context: CallbackContext):
    text=str("Look at this, man! Here we've got enough weapons to hunt a dragon, or to raid a cursed temple!"
        +"\nCheck out whatever you like, and if something interests you, don't hesitate to ask!")
    reply_markup = InlineKeyboardMarkup(kb.kb("wtypes",("bsmith|na","null")))
    update.message.reply_text(
                                text=text,
                                reply_markup = reply_markup,
                                parse_mode=ParseMode.HTML
                            )
    return

def shopcat(update: Update, context: CallbackContext):
    global WeaponDB
    user = update.callback_query.from_user
    data = json.loads(update.callback_query.data)
    player = PlayerDB[str(user.id)]
    weapons = False
    text="<b>Available {type} type weapons:</b>\n".format(type=data["d1"])
    for w in list(set(WeaponDB.keys()) - set(player["weapons"])):
        if(int(w) < 100):
            if(WeaponDB[w]["g_type"] == data["d1"]):
                text+="\n\n"+"\t"*4+"► {name} /info_{id}".format(name=WeaponDB[w]["name"],id=w)
                text+="\n"+"\t"*6+"Price: {price}💰 /buy_{id}".format(price=WeaponDB[w]["price"],id=w)
                weapons = True

    if(weapons == False):
        text += "\n"+"\t"*4+"<b>((None))</b>"
    reply_markup = InlineKeyboardMarkup(kb.kb("wtypes",("bsmith|na","null")))
    context.bot.edit_message_text(
                            text=text,
                            chat_id=user.id,
                            message_id=update.callback_query.message.message_id,
                            reply_markup = reply_markup,
                            parse_mode=ParseMode.HTML
                        )
    return

def buy(update: Update, context: CallbackContext):
    global PlayerDB
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    weapon = update.message.text.replace("/buy_","")
    if(weapon not in player["weapons"]):
        if(int(player["money"]) >= int(WeaponDB[weapon]["price"])):
            PlayerDB[str[user.id]]["weapons"].append(weapon)
            wps = PlayerDB[str[user.id]]["weapons"]
            money = str(int(PlayerDB[str(user.id)]["money"]) - int(WeaponDB[weapon]["price"]))
            upload(player=str(user.id),concept=("weapons","money"),value=(wps,money))
            text = "Ha ha! This <b>{weapon}</b> suits you pretty fine, pal! \nUse it wisely!".format(weapon = WeaponDB[weapon]["name"])
        else:
            text = "Sorry mate, but it seems you can't afford this ware."
        update.message.reply_text(
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                )
    else:
        return
    return

def winfo(update: Update, context: CallbackContext):
    global WeaponDB
    weapon = WeaponDB[update.message.text.replace("/info_","")]
    #print(str(weapon))
    text = str(
        "<b>⚜️ {name} ⚜️</b>".format(name=weapon["name"])
        +"\n\n<i>“{lore}”</i>\n".format(lore = weapon["lore"])
        +"\n"+"\t"*4+" Attack: <code>{atk}</code>".format(atk = str(int(float(weapon["atk"])*100)))
        +"\n"+"\t"*4+" Defense: <code>{df}</code>".format(df = str(int(float(weapon["def"])*100)))
        +"\n"+"\t"*4+" Critical: <code>{crit}</code>".format(crit=str(int(float(weapon["crit"])*100)))
        +"\n"+"\t"*4+" Speed: <code>{spe}</code>".format(spe=str(int(float(weapon["spe"])*100)))
        +"\n"+"\t"*4+" Dual Hand: <code>{dual}</code>".format(dual= ("Yes" if(weapon["dual"] == True) else "No"))
        +"\n"+"\t"*4+" Type: <code>{g_type}</code>".format(g_type=weapon["g_type"].title())
        +"\n"+"\t"*4+" Class: <code>{type}</code>".format(type=weapon["type"].title())
    )
    update.message.reply_text(
                                text=text,
                                parse_mode=ParseMode.HTML
                            )

    return

def forge(update: Update, context: CallbackContext):
    text='Sorry pal, I can do nothing without my tools... At least that you want to use a toothpick as a rapier, ha ha!'
    update.message.reply_text(text=text)
    return

def luckyseven(update: Update, context: CallbackContext):
    text='Gambling tables are empty, no one wants to try luck by now... \nTry coming back another time.'
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("↩️ Leave")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return L7

def help(update: Update, context: CallbackContext):
    text='How may I help you, traveller?'
    IKB = InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        [
            [
                IKB("📝🎫 T. Card"),
                IKB("📝🍻 Beer"),
            ],
            [
                IKB("📝⚔️ Duelling"),
                IKB("📝🎲 Lucky7")
            ],
            [
                IKB("📝⚒ Blacksmith"),
                IKB("↩️ Go Back")
            ]
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return HELP

def helpinfo(update: Update, context: CallbackContext):
    choice = update.message.text
    if(choice == "📝🎫 T. Card"):
        text = str("<i>Well, every traveller has a 🎫Traveller Card, there's where you'll "
            +"keep a record of all your progress and your basic information. There you "
            +"can also see all your owned equipment, and from there you can manage it and "
            +"change it in a way it better suits your combat style.</i>")
    elif(choice == "📝🍻 Beer"):
        text = str("<i>Tell me, traveller, what do you think a Tavern would be without a good 🍻Beer to serve?\n"
            +"Yeah, that is what this is all about, drinking beer, making friends and such... When you drink, "
            +"you get the chance to meet new people, well, only if you want to talk to them... "
            +"Travellers usually like to see known faces wherever they go, and what a better way to make that "
            +"possible, if not making new friend first?"
            +"\nSo, if you want to, don't hesitate on talking to someone new... Who knows? Maybe your next adventure is waiting along with a new face?</i>"
            +"\n\n<code>WARNING: By pressing on </code>🍻 Beer<code> you'll be offered to talk to someone else, if the matchmaking finds someone."
            +" If you both accept, your username will be shared with someone else. Have that in mind!</code>")
    elif(choice == "📝⚔️ Duelling"):
        text = str("<i>Aha! So, you are interested on combat, eh?... If is that so, you're free to use the ⚔️ Duelling Court."
            +" As I said before, you can challenge a random stranger from here, or you can challenge a friend via inline message on any chat window."
            +"\nAll you have to do is to write:</i>\n\n@WanderersTavernBot + <code>space</code>\n\n <i>and you'll be given the option to ⚔️Duel with any friend."
            +" Just keep in mind that, playing with anyone not registered has no effect on any of your character stats, such as money, experience or glory</i>")
    elif(choice == "📝⚒ Blacksmith"):
        text = str("<i>Who? Ah, yes! The guy who sells and forges weapons next to the duelling court! He's a ⚒ Blacksmith."
            +"\nIf you need some equipment, he's the man! He has many weapons on his stock, also, he forges custom weapons, "
            +"perfect for those who want a signature weapon from which bards can tell about on the epic tales!</i>")
    elif(choice == "📝🎲 Lucky7"):
        text = str("<i>Feeling lucky? try having a round on the gambling tables. You pay 10, and get 20 in return, easy, isn't it?"
            +"\nYou just have to get a higher number than your opponent on the dices, and you'll win the match. But if the dices add up to 7, "
            +"you'll automatically win the match! Simple. \nWell... Unless there's a tie. In that case only the highest dice will be counted."
            +"\n\nYou can also play with friends, or give the dices any other use you want. Same as the duels, you can call the dices via inline message:"
            +"</i>\n\n@WanderersTavernBot + <code>space</code>\n\n<i>Just as easy as that!"
            +"</i>")

    update.message.reply_text(text=text,parse_mode=ParseMode.HTML)
    return

def owned(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        data = {"op":"owned|na","d1":"sword","d2":"null"}
    except:
        user = update.callback_query.from_user
        data = json.loads(update.callback_query.data)

    player = PlayerDB[str(user.id)]
    text = "<b>{name}'s {type} type weapons:</b>\n".format(name=user.first_name,type=data["d1"])
    weapons = False
    for w in [*player["weapons"]]:
        try:
            if(WeaponDB[w]["g_type"] == data["d1"]):
                text+="\n"+"\t"*4+"► {name} /info_{id} \n\t\t\t\t\t\t\t\tEquip: /on_{id}".format(name=WeaponDB[w]["name"],id=w)
                weapons = True
        except:
            player["weapons"].remove(None)
            continue

    if(weapons == False):
        text += "\n"+"\t"*4+"<b>((None))</b>"
    reply_markup = InlineKeyboardMarkup(kb.kb(op="wtypes",args=("owned|na","null")))
    try:
        update.message.reply_text(
                                    text,
                                    reply_markup = reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
    except Exception as e:
        context.bot.edit_message_text(
                                text=text,
                                chat_id=user.id,
                                message_id=update.callback_query.message.message_id,
                                reply_markup = reply_markup,
                                parse_mode=ParseMode.HTML
                            )
    return

def equip(update: Update, context: CallbackContext):
    user = update.message.from_user
    player = PlayerDB[str(user.id)]
    weapon = update.message.text.replace("/on_","")
    if(weapon not in WeaponDB.keys()):
        return
    else:
        if(weapon not in player["weapons"]):
            text = "You do not own this weapon!"
        else:
            wpassign(weapon,user)
            text = "<b>{weapon}</b> equipped successfully!".format(weapon = WeaponDB[weapon]["name"])
        update.message.reply_text(
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                )
    return

def wpassign(weapon,user):
    slot = ""
    if(WeaponDB[weapon]["type"] in ["dagger","shield"]):
        slot = "offHW"
    else:
        slot = "mainW"

    if(slot == "mainW"):
        if(WeaponDB[weapon]["dual"] == True):
            """Cambian ambos slots"""
            upload(player=str(user.id),concept=("mainW","offHW"),value=(weapon,"999"))
        else:
            if(WeaponDB[PlayerDB[str(user.id)]["mainW"]]["dual"] == True):
                """Asigna el arma, y Wooden Shield, respectivamente"""
                upload(player=str(user.id),concept=("mainW","offHW"),value=(weapon,"02"))
            else:
                """Cambia normalmente"""
                upload(player=str(user.id),concept=("mainW"),value=(weapon))
    else:
        if(WeaponDB[PlayerDB[str(user.id)]["mainW"]]["dual"] == True):
            """Asigna Iron Sword como principal y la secundaria normalmente"""
            upload(player=str(user.id),concept=("mainW","offHW"),value=("01",weapon))
        else:
            """Asigna secundaria normalmente"""
            upload(player=str(user.id),concept=("offHW"),value=(weapon))
    return


def main():#if __name__ == '__main__':
    global updater
    conv_handler = ConversationHandler(
        entry_points=[
            #CommandHandler('start', start),
            CommandHandler('start', register),
            MessageHandler(Filters.regex("^(🎫 Traveller Card)$"), me),#Returns ME
            MessageHandler(Filters.regex("^(🍻 Beer)$"), beer),#Returns BR
            MessageHandler(Filters.regex("^(⚔️ Duelling Court)$"), duellingcourt),#Returns DC
            MessageHandler(Filters.regex("^(⚒ Blacksmith)$"), blacksmith),#Returns BS
            MessageHandler(Filters.regex("^(🎲 Lucky Seven)$"), luckyseven),#returns L7
            MessageHandler(Filters.regex("^(📝 Help)$"), help),
            CommandHandler('reload', reload),
            MessageHandler(Filters.text,register)
            ],

        states={
            ME: [MessageHandler(Filters.regex("^(🗡 Weapons)$"), owned),
                MessageHandler(Filters.regex(r"^\/on_\d+$"), equip),
                MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo)],

            #BR: [MessageHandler(Filters.regex("^(👥 Talk)$"), connect)],

            DC: [MessageHandler(Filters.regex("^(↩️ Leave)$"), register)],

            BS: [MessageHandler(Filters.regex("^(📦 Shop)$"), shop),
                MessageHandler(Filters.regex(r"^\/info_\d+$"), winfo),
                MessageHandler(Filters.regex(r"^\/buy_\d+$"), buy),#
                MessageHandler(Filters.regex("^(♨️ Forge)$"), forge)],

            L7: [MessageHandler(Filters.regex("^(↩️ Leave)$"), register)],

            HELP: [MessageHandler(Filters.regex("^(📝🎫 T. Card)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝🍻 Beer)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝⚔️ Duelling)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝⚒ Blacksmith)$"), helpinfo),
                MessageHandler(Filters.regex("^(📝🎲 Lucky7)$"), helpinfo)],
            },

        fallbacks=[MessageHandler(Filters.regex("^(❌ Cancel)$"), register),
            MessageHandler(Filters.regex("^(↩️ Go Back)$"), register),
            CommandHandler("reload", reload)]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(queryHandler))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery,pass_user_data=True, pass_chat_data=True))
    # Start the Bot
    updater.start_polling(poll_interval = 0.1,clean = True,read_latency=1.0)
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    # No substitutions, exchanges or refunds.
    updater.idle()
    return

if __name__ == '__main__':
    main()
