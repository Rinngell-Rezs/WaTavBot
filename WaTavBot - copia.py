#!/usr/bin/env python
# -*- coding: utf-8 -*-

#C:\Users\micke\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\pyrogram

#Librerías para interactuar con la API de Telegram
from telegram import *
from telegram.ext import *
TOKEN = "688638504:AAEInD-EFrYbKkw6tlJBIIpRmQsBJRbpTio" #TavernKeeperBot
#TOKEN = "786177048:AAFkRsFe2a4cIjrj_b7AvxY8o4i0agrsnrA" #WaTavBot

#Librerías de utilidades
from random import randint as rng
from time import sleep
import json
import miscellaneous as misc
import rooms as r
import Braile as br

#Manejo de Base de Datos
from firebase import firebase
fire = firebase.FirebaseApplication("https://watavbot.firebaseio.com",None)

#Otras librerías para el desarrollo
from uuid import uuid4
from sys import stdout
import logging
import threading



TOURNAMENT = range(1)

class kb:
    def kb(op = None, args = None):
        if op == 'data':
            keyboard = [[InlineKeyboardButton("Join", callback_data = args)]]
        elif op == 'dice':
            keyboard = [[InlineKeyboardButton("Roll", callback_data = args)]]
        elif op == 'start':
            keyboard = [["🎖Tournament🏅"]]
        if op == None:
            keyboard = [
                         [
                          InlineKeyboardButton("🗡Head", callback_data="{\"op\":\"batt\",\"next\":\"ah\",\"room\":\"%s\"}"%(args)),
                          InlineKeyboardButton("🛡Head", callback_data="{\"op\":\"batt\",\"next\":\"dh\",\"room\":\"%s\"}"%(args))
                         ],

                         [
                          InlineKeyboardButton("🗡Body", callback_data="{\"op\":\"batt\",\"next\":\"ab\",\"room\":\"%s\"}"%(args)),
                          InlineKeyboardButton("🛡Body", callback_data="{\"op\":\"batt\",\"next\":\"db\",\"room\":\"%s\"}"%(args))
                         ],

                         [
                          InlineKeyboardButton("🗡Legs", callback_data="{\"op\":\"batt\",\"next\":\"af\",\"room\":\"%s\"}"%(args)),
                          InlineKeyboardButton("🛡Legs", callback_data="{\"op\":\"batt\",\"next\":\"df\",\"room\":\"%s\"}"%(args))
                         ],
                        ]
        return keyboard
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)
logger = logging.getLogger(__name__)

def register(id,customer_data):
    fire.put("/customers",id,customer_data)

def start(bot, update):
    query = update.message.from_user
    text = """You approach and see a sign at the door:\n
_Excuse us, by the moment we\'re under maintenance...
However you can always use our dueling court that is in the back. Just write \"@WanderersTavernBot\" and press \"⚔Duel\" on any chat window to access to it.
We\'ll be on business earlier than later..._
\n"""
    reply_markup = ReplyKeyboardMarkup(kb.kb("start"),resize_keyboard = True)
    update.message.reply_text(
                                text,
                                reply_markup = reply_markup,
                                parse_mode=ParseMode.MARKDOWN
                            )
    if((query.id in fire.get("/customers",None)) == False):
        customer_data = {
                        'first_name':query.first_name,
                        'last_name':query.last_name,
                        'username':query.username,
                        'activity':""
                        }
        threading.Thread(target = register, args = (query.id,customer_data)).start()

    return TOURNAMENT


def tournament(bot,update):
    print(str(bot))
    print(str(update))
    #print("Here goes the tournament stuff")
    return#Yet to implement

def queryHandler(bot, update):
    query = update.callback_query
    data = json.loads(query.data)
    ##print("Acá elijo qué se va a hacer :9")
    if(data["op"] == "batt"):
        threading.Thread(target = battle, args = (bot,update,)).start()
        ##print("Acá fue battle!")
    if(data["op"] == "dice"):
        threading.Thread(target = dice, args = (bot,update,)).start()
        ##print("Acá fue dado!")
    return

def battle(bot,update):
    ###Getting important information, some redundant but assigned for easier use
    query = update.callback_query
    ##print(str(query.inline_message_id))
    data = json.loads(query.data)
    rooms = "/arena/Rooms/"
    this_room = fire.get(rooms,query.inline_message_id)#
    this_room_route = rooms+query.inline_message_id+"/"
    players_route = "/arena/Rooms/"+query.inline_message_id+"/players/"
    plr_data_route = players_route+query.from_user.username
    ###players won't be there at the begining, and therefore will cause errors
    try:
        players = this_room["players"]#"/arena/Rooms/"+query.inline_message_id+"/players/"#AQAAAH7AAAB4Z6wjQMSBTx_Wspk
        plr_data = players[query.from_user.username]#players+query.from_user.username
    except Exception as e:
        None
    #castles and classes are here just for the lols. Could be taken from other script but meh
    castles = "/utils/castles/"
    classes = "/utils/classes/"
    customers = "/customers/"
    plr = []
    plr_usrN = []

    ######################################################################################################################################################## Creates players
    if((data["next"] == "p1") or (data["next"] == "p2")):
        ##print("Ahora crearé a los jugadores...")
        reply_markup = None
        text = ""
        if(query.from_user.username == None):
            bot.answerCallbackQuery(query.id,"Sorry, no name, no service!",True)
            return
        """cust = fire.get(customers,None)
        if(str(query.from_user.id) in cust):
            if(cust[str(query.from_user.id)]["activity"] == "arena"):
                bot.answerCallbackQuery(query.id,"Pardon me, but you cannot start two fights at once!",True)
                return"""

        f_name = misc.nameFormat(
                                r.classes,
                                r.castles,
                                query.from_user
                               )
        player =    {
                        'f_name':f_name,
                        'name':query.from_user.first_name,
                        'username':query.from_user.username,
                        'hp':100,
                        'atk':"",
                        'def':"",
                        'ready':False
                    }
        if(data["next"] == "p1"):
            ##print("Este es el jugador 1:")
            ##print(str(fire.get(rooms+"/"+query.from_user.username+"/players/",query.from_user.username)))
            p1 = "%s(@%s)"%(query.from_user.first_name,query.from_user.username)
            text = "<b>⚔Duel</b>\nChallenger %s is ready!\nWaiting for an opponent..."%p1
            reply_markup = InlineKeyboardMarkup (
                                                    [
                                                        [
                                                            InlineKeyboardButton(
                                                                text = "Join",
                                                                callback_data = "{\"op\":\"batt\",\"next\":\"p2\",\"room\":\"%s\"}"%(query.from_user.username)
                                                            )
                                                        ]
                                                    ]
                                                )
        else:
            if(query.from_user.username in players):
                bot.answerCallbackQuery(query.id,"You cannot play with yourself, duh!",True)
                return
            ##print("Este es el jugador 2:")
            ##print(str(fire.get(players,query.from_user.username)))
            for p in players:
                plr.append("%s(@%s)"%(players[p]["name"],players[p]["username"]))
                plr_usrN.append(p)
            p2 = "%s(@%s)"%(query.from_user.first_name,query.from_user.username)
            text = "<b>⚔Duel</b>\n%s will face %s on the arena!\nWaiting for the host to start the match..."%(plr[0],p2)
            reply_markup = InlineKeyboardMarkup (
                                                    [
                                                        [
                                                            InlineKeyboardButton(
                                                                text = "Start the match!",
                                                                callback_data = "{\"op\":\"batt\",\"next\":\"ready\",\"room\":\"%s\"}"%(data["room"])
                                                            )
                                                        ]
                                                    ]
                                                )
        bot.edit_message_text(text=text,
                              inline_message_id=query.inline_message_id,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML
                              )
        if(data["next"] == "p1"):
            fire.put(rooms+"/"+query.inline_message_id+"/players/",query.from_user.username,player)
            #fire.put()
        else:
            fire.put(players_route,query.from_user.username,player)
            fire.put(this_room_route,"round",0)
            fire.put(this_room_route,"turn",["",""])
            misc.turns[query.inline_message_id] = ["",""]
            fire.put(this_room_route,"text","")
            fire.put(this_room_route,"end",False)
        return
    ######################################################################################################################################################## creates player names
    #For fast execution reasons and to prevent host clonning
    #I'll leave plr variables assignation after match creation
    if(players != None):
        for p in players:
            plr.append("%s(@%s)"%(players[p]["name"],players[p]["username"]))
            plr_usrN.append(p)



    ######################################################################################################################################################## <<<<<<<<<<<<<<<<<<<<<<<<<<<
    #Checks if the user exist in the match, then sets attack and defense points
    ######################################################################################################################################################## <<<<<<<<<<<<<<<<<<<<<<<<<<<

    if((query.from_user.username in players) == False):
        bot.answerCallbackQuery(query.id,"What are you doing? You're not part of this fight!",False)
        return
    elif(data["next"][0] in misc.sign):
        ##############################
        #print(query.from_user.username+": "+"Setting {}".format(misc.sign[data["next"][0]].capitalize(),misc.sign[data["next"][1]].capitalize()))
        ##############################
        if(plr_data[misc.sign[data["next"][0]]] == ""):#fire.get(plr_data,misc.sign[data["next"][0]]) == ""):
            fire.put(plr_data_route,misc.sign[data["next"][0]],data["next"][1])
            players[query.from_user.username][misc.sign[data["next"][0]]] = data["next"][1]
            ######################
            #print(query.from_user.username+": "+"{} Set!".format(misc.sign[data["next"][0]].capitalize()))
            ######################
            bot.answerCallbackQuery(query.id,"Chosen: %s %s"%(misc.sign[data["next"][0]].upper(),misc.sign[data["next"][1]]),False)
        else:
            bot.answerCallbackQuery(query.id,"No substitutions, exchanges or refunds!",True)
            ######################
            #print(query.from_user.username+": "+"Tried to Re-set")
            ######################

    ######################################################################################################################################################## checks if the players are ready
    r_pass = (players[query.from_user.username]["atk"] != "") and (players[query.from_user.username]["def"] != "") and (players[query.from_user.username]["ready"] != True)
    ######################
    ##print(query.from_user.username+": "+"r_pass = "+str(r_pass))
    ######################
    if(r_pass):
        ######################
        #print(query.from_user.username+": "+"Is ready!")
        ######################
        fire.put(players_route+query.from_user.username,"ready",True)
        players[query.from_user.username]["ready"] = True
        ######################
        #print(query.from_user.username+": "+"Ready set!")
        ######################
        if(fire.get(this_room_route+"turn/","0") == ""):
            misc.turns[query.inline_message_id][0] = query.from_user.username
            fire.put(this_room_route,"turn",misc.turns[query.inline_message_id])
            ######################
            #print(query.from_user.username+": "+"Player set into turn 0!")
            ######################
        else:
            misc.turns[query.inline_message_id][1] = query.from_user.username
            fire.put(this_room_route,"turn",misc.turns[query.inline_message_id])
            ######################
            #print(query.from_user.username+": "+"Player set into turn 1!")
            ######################
        this_room = fire.get(rooms,query.inline_message_id)#
    else:
        bot.answerCallbackQuery(query.id,"Please, excuse us fot the issues, the dev is not doing his job properly.",False)
        print("")

    ######################################################################################################################################################## <<<<<<<<<<<<<<<<<<<<<<<<<<<
    #If all players are ready, calculates damage and resets attack and defense
    ######################################################################################################################################################## <<<<<<<<<<<<<<<<<<<<<<<<<<<
    try:
        #if("turn" in this_room):
        if(not "" in misc.turns[query.inline_message_id]):
            ctr = 0
            hitpoint = ""
            full_text = ""
            damage = 0
            for t in misc.turns[query.inline_message_id]:
                if ctr == 0:
                    ctr = 1
                else:
                    ctr = 0
                if(players[t]["hp"] > 0):
                    if(players[t]["atk"] == 'h'):
                        hitpoint = "head"
                        if(players[misc.turns[query.inline_message_id][ctr]]["def"] == "h"):
                            damage = 0#rng(21,29)+1
                        elif(players[misc.turns[query.inline_message_id][ctr]]["def"] == "b"):
                            damage = rng(16,24)+1
                        else:
                            damage = rng(11,19)+1
                    elif(players[t]["atk"] == 'b'):
                        hitpoint = "body"
                        if(players[misc.turns[query.inline_message_id][ctr]]["def"] == "h"):
                            damage = rng(21,29)+1
                        elif(players[misc.turns[query.inline_message_id][ctr]]["def"] == "b"):
                            damage = 0#rng(16,24)+1
                        else:
                            damage = rng(11,19)+1
                    else:
                        hitpoint = "legs"
                        if(players[misc.turns[query.inline_message_id][ctr]]["def"] == "h"):
                            damage = rng(21,29)+1
                        elif(players[misc.turns[query.inline_message_id][ctr]]["def"] == "b"):
                            damage = rng(16,24)+1
                        else:
                            damage = 0#rng(11,19)+1
                    full_text += "\n{} charged at {}\'s {} dealing {} damage!".format(
                                                                                players[t]["name"],
                                                                                players[misc.turns[query.inline_message_id][ctr]]["name"],
                                                                                hitpoint,
                                                                                damage,)
                    players[misc.turns[query.inline_message_id][ctr]]["hp"] -= int(damage)

            full_text += "\n<b>First Strike:</b> {}\n".format(misc.turns[query.inline_message_id][0])
            full_text = "\n<b>Round {}!</b>".format(this_room["round"]) + full_text
            this_room["text"] += full_text
            data["next"] = "nround"
    except KeyError:
        misc.turns[query.inline_message_id] = fire.get(this_room_route,"turn")

    ######################################################################################################################################################## Checks if lives < 0
    try:
        if(not "" in misc.turns[query.inline_message_id]):
            if((players[misc.turns[query.inline_message_id][0]]["hp"] <= 0) or (players[misc.turns[query.inline_message_id][1]]["hp"] <= 0)):
                if(this_room["end"] == False):
                    if(players[misc.turns[query.inline_message_id][0]]["hp"] > players[misc.turns[query.inline_message_id][1]]["hp"]):
                        winner = players[misc.turns[query.inline_message_id][0]]["username"]
                        noWinner = players[misc.turns[query.inline_message_id][1]]["username"]
                        players[misc.turns[query.inline_message_id][1]]["hp"] = 0
                    else:
                        winner = players[misc.turns[query.inline_message_id][1]]["username"]
                        noWinner = players[misc.turns[query.inline_message_id][0]]["username"]
                        players[misc.turns[query.inline_message_id][0]]["hp"] = 0
                    status = ""
                    if(players[winner]["hp"] > 100):
                        status = ["One can feel heavy nausea from what just hapened here...",", just like a vampire just sucked dry ","'s life... May the gods save us from such an abomination!"]
                    elif(players[winner]["hp"] == 100):
                        status = ["This is not seen very often. the player","got a flawless victory against",". Sir, you're a true champion!!!"]
                    elif(players[winner]["hp"] > 66):
                        status = ["Like it was a child's play,","easely vanquished","in combat."]
                    elif(players[winner]["hp"] > 33):
                        if(this_room["round"] > 5):
                            length = "long"
                        else:
                            lenght = "short"
                        status = ["After a {} heated battle,".format(length),"was able to overtake","in what it seemed a paired match."]
                    else:
                        status = ["The fight was bloody and brutal, but in the end","could barely surpass its opponent","in the last second."]
                    this_room["text"] += "\n{}❤️{}\n\t\t\tVS\n{}❤️{}".format(
                                                                            players[misc.turns[query.inline_message_id][0]]["hp"],
                                                                            players[misc.turns[query.inline_message_id][0]]["f_name"],
                                                                            players[misc.turns[query.inline_message_id][1]]["hp"],
                                                                            players[misc.turns[query.inline_message_id][1]]["f_name"])
                    this_room["text"] += "\n\n{} {} {} {} {}. \n<b>Congrajulashions {}!!!</b>".format(
                                                    status[0],
                                                    players[winner]["name"],
                                                    status[1],
                                                    players[noWinner]["name"],
                                                    status[2],
                                                    players[winner]["f_name"])
                    bot.edit_message_text(text=this_room["text"],
                                          inline_message_id=query.inline_message_id,
                                          #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start the match!", callback_data = "{\"next\":\"ready\",\"room\":\"%s\"}"%(data["room"]))]]),
                                          parse_mode=ParseMode.HTML
                                          )
                    fire.put(rooms,query.inline_message_id,None)
                    misc.turns.pop(query.inline_message_id)
                    return
    except KeyError:
        misc.turns[query.inline_message_id] = fire.get(this_room_route,"turn")



    ######################################################################################################################################################## Generates each round info
    #Triggers each time a new round starts
    if((data["next"] == "ready") or (data["next"] == "nround")):
        if((query.from_user.username != data["room"]) and data["next"] == "ready"):
            bot.answerCallbackQuery(query.id,"You cannot start the match, you're not the host!",True)
            return
        fire.put(this_room_route, "round", this_room["round"]+1)
        text = ""
        final_text = ""
        if(data["next"] == "ready"):
            final_text = """Embrace yourselves, mighty warriors!
The duel between {} \nand {} has started!""".format(plr[0],plr[1])
        else:
            final_text = text = this_room["text"]+"\n<b>__________________________________________</b>"
            #fire.put(this_room,"text",text+add)
        final_text += """\n<b>Round {}!</b>
{}❤️{}
\t\t\t   VS
{}❤️{}""".format(
                                                    this_room["round"]+1,
                                                    players[plr_usrN[0]]["hp"],#fire.get(players+plr_usrN[0],"hp"),
                                                    players[plr_usrN[0]]["f_name"],#fire.get(players+plr_usrN[0],"f_name"),
                                                    players[plr_usrN[1]]["hp"],#fire.get(players+plr_usrN[1],"hp"),
                                                    players[plr_usrN[1]]["f_name"]#fire.get(players+plr_usrN[1],"f_name"),
                                                    )

        fire.put(this_room_route,"text",text)
        final_text += "\n\nChoose point of attack and point of block.\nBe fast, the first to choose will be the first to attack!"
        reply_markup = InlineKeyboardMarkup(kb.kb(args = data["room"]))
        bot.edit_message_text(text=final_text,
                              inline_message_id=query.inline_message_id,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML
                              )
        if(not "" in misc.turns[query.inline_message_id]):
            for t in misc.turns[query.inline_message_id]:
                players[t]["atk"] = ""
                players[t]["def"] = ""
                players[t]["ready"] = False
            fire.put(this_room_route,"players",players)
            misc.turns[query.inline_message_id] = ["",""]
            fire.put(this_room_route,"turn",misc.turns[query.inline_message_id])
        return




def dice(bot,update):
    query = update.callback_query
    data = json.loads(query.data)
    d1 = rng(1,6)
    d2 = rng(1,6)
    dir = "/utils/dice"
    D1 = fire.get(dir,d1)
    D2 = fire.get(dir,d2)
    add = ""
    if(d1+d2 == 7):
        add = " Lucky Seven!!"
    text = "{} threw the dice, and...\nThe dices show {}({}) and {}({})...\n<b>{} got {}{}!</b>\n\n".format(
                                    query.from_user.full_name,
                                    D1,d1,
                                    D2,d2,
                                    query.from_user.full_name,
                                    d1+d2,
                                    add
                                    )
    ##print(text)
    bot.edit_message_text(
                            text=text,
                            inline_message_id=query.inline_message_id,
                            parse_mode=ParseMode.HTML
                        )
    customer_data = {
                    'first_name':query.from_user.first_name,
                    'last_name':query.from_user.last_name,
                    'username':query.from_user.username,
                    #'activity':"arena"
                    }
    threading.Thread(target = register, args = (query.from_user.id,customer_data)).start()
    #bot.answerCallbackQuery(query.id,"Oh no my brother, you got to get your own!",True)
    return

def inlinequery(bot, update, user_data, chat_data):
    #Handle the inline query.
    query = update.inline_query
    ##print(query.query)
    ##print(str(user_data))
    ##print(str(chat_data))
    reply_markup = None
    results = [
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="⚔Duel",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "data",args = "{\"op\":\"batt\",\"next\":\"p1\",\"room\":\"None\"}")),
                                            input_message_content= InputTextMessageContent(
                                                                                            message_text = "<b>⚔Duel</b>\nWaiting for combatants...",
                                                                                            parse_mode=ParseMode.HTML,
                                                                                            reply_markup = reply_markup,
                                                                                         )
                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🎲Dice",
                                            reply_markup = InlineKeyboardMarkup(kb.kb(op = "dice",args = "{\"op\":\"dice\",\"next\":\"dice\",\"room\":\"%s\"}"%(query.from_user.username))),
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "Press \"Roll\" to roll the dices...",
                                                                                            parse_mode=ParseMode.MARKDOWN,
                                                                                            reply_markup = reply_markup
                                                                                        ),

                                        ),
                InlineQueryResultArticle(
                                            id=uuid4(),
                                            title="🍺Beer",
                                            input_message_content=InputTextMessageContent(
                                                                                            message_text = "You are given a jar full frothy beer🍺.\n_Let's toast for the pleasure of being here and now!_",
                                                                                            parse_mode=ParseMode.MARKDOWN
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
    if(query.query in fire.get("/arena/tournament/",None)):
        results.append(
                        InlineQueryResultArticle(
                                                    id=uuid4(),
                                                    title="🎖{} Tournament🏅".format(query.query.capitalize()),
                                                    input_message_content= InputTextMessageContent(
                                                                                                    message_text = "<b>Join the {} Tournament!</b>\n\nPlayers:\n".format(query.query.capitalize()),
                                                                                                    parse_mode=ParseMode.HTML
                                                                                                    #reply_markup = reply_markup,
                                                                                                 )
                                                )
                        )
    update.inline_query.answer(results)
    return



def error(bot, update, error):
    """Log Errors caused by Updates."""
    message = str(logger.warning('Update "%s" caused error "%s"', update, error))
    ##print(message)
    bot.send_message(184075777,message)

def main():#if __name__ == '__main__':
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                     CommandHandler('dice', start),
                     CommandHandler('beer', start),
                     CommandHandler('help', start),
                     CommandHandler('tournament',tournament)
                    ],

        states={
                TOURNAMENT: [RegexHandler('^(🎖Tournament🏅)$', tournament)]#,

                #PHOTO: [MessageHandler(Filters.photo, photo),
                #        CommandHandler('skip', skip_photo)],

                #LOCATION: [MessageHandler(Filters.location, location),
                #           CommandHandler('skip', skip_location)],

                #BIO: [MessageHandler(Filters.text, bio)]
              },

        fallbacks=[CommandHandler('cancel', start)]
    )
    updater.dispatcher.add_handler(conv_handler)
    #updater.dispatcher.add_handler(CommandHandler('start', start))
    #updater.dispatcher.add_handler(CommandHandler('dice', start))
    #updater.dispatcher.add_handler(CommandHandler('beer', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(queryHandler))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery,pass_user_data=True, pass_chat_data=True))
    #updater.dispatcher.add_handler(CommandHandler('help', start))
    #updater.dispatcher.add_handler(CommandHandler('tournament',tournament))
    #updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling(poll_interval = 0.1,clean = True,read_latency=1.0)
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    # No substitutions, exchanges or refunds.
    updater.idle()

if __name__ == '__main__':
    #import NOPESmartKnight as SM
    #threading.Thread(target = SM.main).start()
    main()
